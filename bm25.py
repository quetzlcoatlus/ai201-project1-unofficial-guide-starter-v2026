"""
Keyword search for hybrid retrieval.

The semantic side (store.py) finds chunks that mean the same thing as the
question. This side finds chunks that share its exact words — course codes,
building names, "walk-in" — which embeddings can blur together.

The BM25 index is rebuilt from the Chroma collection on every call rather than
saved to disk. It reads the same stored chunks the semantic side searches, so
the two can never drift apart, and at this corpus size it takes milliseconds.

`hybrid_search` does the fusion; `store.search` hands off to it
when config.HYBRID is on.

Run `python bm25.py` to print the top BM25 score for each test question and
their median — that median is how config.BM25_C gets picked.
"""

import re
import statistics
from dataclasses import dataclass

import numpy as np
from rank_bm25 import BM25Okapi

import config

# A course code: 2-5 capital letters, an optional space, then 2-4 digits
# ("CS 340", "STAT 150", "CS340"). Capitals only, and matched before
# lowercasing: case-insensitive, the same pattern also catches "about 40" and
# "to 30" all over the corpus. The cost is that a query typed "cs 340" in
# lowercase splits into two tokens; "cs340" and "CS 340" both still match.
COURSE_CODE = re.compile(r"\b([A-Z]{2,5}) ?(\d{2,4})\b")

WORD = re.compile(r"[a-z0-9]+")

_stopwords = None


def _stopword_set() -> set[str]:
    global _stopwords
    if _stopwords is None:
        try:
            from nltk.corpus import stopwords

            _stopwords = set(stopwords.words("english"))
        except LookupError as exc:
            raise RuntimeError(
                "NLTK's stopword list isn't downloaded. "
                "Run `python -m nltk.downloader stopwords` once."
            ) from exc
    return _stopwords


def tokenize(text: str) -> list[str]:
    """
    Turn text into BM25 tokens. Chunks and questions both go through here —
    if they were tokenized differently, nothing would match.

    Course codes become one token ("CS 340" -> "cs340"), then everything is
    lowercased, split on anything that isn't a letter or digit, and stripped
    of stopwords.
    """
    text = COURSE_CODE.sub(r"\1\2", text).lower()
    stop = _stopword_set()
    return [w for w in WORD.findall(text) if w not in stop]


@dataclass
class KeywordIndex:
    ids: list[str]     # Chroma ids, "source#index" — the join key with store.py
    bm25: BM25Okapi

    def scores(self, question: str) -> dict[str, float]:
        """
        BM25 score for every chunk, keyed by id. Higher is better.

        Negative scores are clamped to 0: BM25Okapi can push a term that
        appears in most chunks below zero, and the squash in fusion assumes
        s >= 0. A question that is all stopwords scores 0 everywhere.
        """
        tokens = tokenize(question)
        if not tokens:
            return {i: 0.0 for i in self.ids}
        raw = self.bm25.get_scores(tokens)
        return {i: max(0.0, float(s)) for i, s in zip(self.ids, raw)}

    def top(self, question: str, n: int) -> list[tuple[str, float]]:
        """The n best (id, score) pairs, highest first."""
        ranked = sorted(self.scores(question).items(), key=lambda p: p[1], reverse=True)
        return ranked[:n]


def _collection(corpus: str | None, variant: str):
    from store import _client

    name = config.collection_name(corpus, variant)
    try:
        return _client().get_collection(name)
    except Exception as exc:
        raise RuntimeError(
            f"No index called '{name}'. Run `python app.py index` first."
        ) from exc


def _build(collection) -> KeywordIndex:
    stored = collection.get(include=["documents"])
    corpus_tokens = [tokenize(text) for text in stored["documents"]]
    return KeywordIndex(ids=list(stored["ids"]), bm25=BM25Okapi(corpus_tokens))


def load(corpus: str | None = None, variant: str = "default") -> KeywordIndex:
    """Build the BM25 index from the chunks already stored in Chroma."""
    return _build(_collection(corpus, variant))


def _cosine_distance(a, b) -> float:
    """Same measure Chroma uses for the collection: 1 - cosine similarity."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return float(1.0 - a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def fused_distance(semantic_distance: float, bm25_score: float) -> float:
    """
    Blend the two signals into one lower-is-better number.

    Semantic similarity (1 - distance) and the squashed BM25 score
    s / (s + BM25_C) are both absolute, not rescaled per query — so a question
    with no real match still comes out far away, and the gate can refuse it.
    """
    semantic = 1.0 - semantic_distance
    keyword = bm25_score / (bm25_score + config.BM25_C)
    return 1.0 - (config.ALPHA * semantic + (1.0 - config.ALPHA) * keyword)


def hybrid_search(
    question: str,
    top_k: int,
    corpus: str | None = None,
    variant: str = "default",
):
    """
    Semantic + keyword retrieval, fused. Called by `store.search` when
    config.HYBRID is on.

    Takes the top CANDIDATES from each method, gives every candidate both
    scores, and keeps the top_k by fused distance. A chunk only BM25 found gets
    its real semantic distance computed from its stored embedding, so a keyword
    hit with unrelated meaning ranks low on its own — no special case needed.
    """
    from store import Result, embed

    collection = _collection(corpus, variant)
    count = collection.count()
    if count == 0:
        return []

    query_embedding = embed([question])[0]
    semantic = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(config.CANDIDATES, count),
        include=["documents", "metadatas", "distances"],
    )

    # id -> (text, metadata, semantic distance)
    candidates = {
        cid: (text, meta, float(dist))
        for cid, text, meta, dist in zip(
            semantic["ids"][0],
            semantic["documents"][0],
            semantic["metadatas"][0],
            semantic["distances"][0],
        )
    }

    keyword_scores = _build(collection).scores(question)
    keyword_top = sorted(keyword_scores.items(), key=lambda p: p[1], reverse=True)
    # Zero-score chunks aren't keyword matches, just the tail of an arbitrary
    # sort — adding them would pad the pool with noise.
    keyword_ids = [cid for cid, s in keyword_top[: config.CANDIDATES] if s > 0]

    missing = [cid for cid in keyword_ids if cid not in candidates]
    if missing:
        fetched = collection.get(
            ids=missing, include=["documents", "metadatas", "embeddings"]
        )
        for cid, text, meta, emb in zip(
            fetched["ids"], fetched["documents"], fetched["metadatas"], fetched["embeddings"]
        ):
            candidates[cid] = (text, meta, _cosine_distance(query_embedding, emb))

    results = []
    for cid, (text, meta, dist) in candidates.items():
        score = keyword_scores.get(cid, 0.0)
        results.append(
            Result(
                text=text,
                source=str(meta.get("source", "unknown")),
                label=f"{meta.get('source', 'unknown')}#{meta.get('index', 0)}",
                distance=fused_distance(dist, score),
                produced_by=str(meta.get("produced_by", "unknown")),
                semantic_distance=dist,
                bm25_score=score,
            )
        )

    results.sort(key=lambda r: r.distance)
    return results[:top_k]


def median_top_score(
    questions: list[str] | None = None,
    corpus: str | None = None,
    variant: str = "default",
) -> tuple[float, list[tuple[str, str, float]]]:
    """
    Median of each question's best BM25 score, for picking config.BM25_C.

    Fusion squashes a raw score s into s / (s + c), so a chunk scoring exactly
    c lands at 0.5. Setting c to the median top score of questions the corpus
    *does* answer means a typical good keyword match counts for about half.

    Returns the median and, per question, (question, best chunk id, score).
    """
    if questions is None:
        from questions import answered

        questions = [q["question"] for q in answered()]

    index = load(corpus, variant)
    rows = []
    for q in questions:
        best_id, best = index.top(q, 1)[0]
        rows.append((q, best_id, best))
    return statistics.median(r[2] for r in rows), rows


if __name__ == "__main__":
    from questions import OUT_OF_SCOPE

    median, rows = median_top_score()
    print("In-scope questions (top BM25 score):")
    for q, best_id, score in rows:
        print(f"  {score:6.3f}  {best_id:<38} {q}  {tokenize(q)}")
    print(f"\nMedian top score -> suggested BM25_C = {median:.3f}")

    _, oos_rows = median_top_score(OUT_OF_SCOPE)
    print("\nOut-of-scope questions, for reference (should be low):")
    for q, best_id, score in oos_rows:
        print(f"  {score:6.3f}  {best_id:<38} {q}  {tokenize(q)}")
