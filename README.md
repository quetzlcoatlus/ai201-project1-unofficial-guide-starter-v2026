# The Unofficial Guide

Allie Lane, campus_life

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

This repository looks at a set of documents in /corpora, specifically campus_life, and answers questions that the documents answer. Running `python app.py ask` prompts the user for questions in the CLI. When the question has an answer in the documents, it returns an answer and the sources that it pulled from. When the question doesn't have an answer, it returns "I don't have enough information about that."

## Chunking Strategy

Headers are prepended to each chunk.
The whitespace and newlines are trimmed so they're one line chunks.
Chunks that are less than 40 characters are merged-forward or backward to create a larger chunk. Doesn't merge across paragraph breaks.

**Chunk size:** Segmented by terminal punctuation, excluding periods used within numbers, times, decimals, or abbreviations.
**Overlap:** No overlap

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

Sentence-esque chunks seem likely to provide relevant context without including too much additional information. The campus_life corpus is mainly fragmented sentences with a header and a few sentences.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: admin_add_drop_deadline.txt#0 `` — produced by: chunker.py::split_documents``

```
On the add/drop deadline: You can add a course through the end of the second week.
```

**Chunk 2** — source: course_cs_340.txt#1 `` — produced by: chunker.py::split_documents``

```
CS 340 Databases: Format is lecture twice a week plus a project that runs the whole term.
```

**Chunk 3** — source: course_stat_150.txt#5 `` — produced by: chunker.py::split_documents``

```
STAT 150 Applied Statistics: The one piece of advice: the dropped midterm makes the first one low-stakes; use it to learn the format.
```

**Chunk 4** — source: dining_verrill_street_grill.txt#2 `` — produced by: chunker.py::split_documents``

```
Verrill Street Grill: The thing worth going for is the burger, which is the only late-night hot food on campus.
```

**Chunk 5** — source: housing_morrow_house.txt#1 `` — produced by: chunker.py::split_documents``

```
Morrow House — what it's actually like: Rooms are singles and doubles, hall bathrooms.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** During winter, when does it get cold? Answer using only the information in the documents below. If they don't cover it, say you don't have enough information.

**Answer:** Based on the provided documents, it is cold from mid-November to early March (winter_gear.txt).

Sources retrieved: transit_walking.txt, winter_gear.txt

```
According to winter_gear.txt, it is cold from mid-November to early March.
```

**My relevance cutoff:** 0.6, kept the default because 0.52 at the middle of the distributions from the responses might fail on near-miss questions.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| During winter, when does it get cold? | Yes | 0.336 |
| What is the rough time that it takes to go from Aldridge Hall to the science quad? | Yes | 0.280 |
| How long after the term starts can you add a course? | Yes | 0.270 |
| What are the walk-in hours for the health center? | Yes | 0.138 |
| Does the campus bookstore price-match? | Yes | 0.228 |
| What is the capital of Mongolia? | No | 0.787 |
| How do I change the oil in a diesel engine? | No | 0.866 |
| Who won the 1994 World Cup? | No | 0.819 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.840 |
| How do I write a for loop in Rust? | No | 0.837 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to write the chunking function from my notes and had it ask clarifying questions wherever there was ambiguity. It added sentence level chunking with the heading attached. No overlap was implemented in this case.

**2.** I asked Claude about the best distances for the 10 questions in `questions.py` and it explained why my initial adjustment to 0.5 might fail on near-miss questions that don't exist in OUT_OF_SCOPE so I adjusted it back to 0.6.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Criteria 1

scorer.py::judge

During winter, when does it get cold?
- run 1: pass  (best distance 0.336)
- run 2: pass  (best distance 0.336)
- run 3: pass  (best distance 0.336)

What is the rough time that it takes to go from Aldridge Hall to the science quad?
- run 1: pass  (best distance 0.280)
- run 2: pass  (best distance 0.280)
- run 3: pass  (best distance 0.280)

How long after the term starts can you add a course?
- run 1: pass  (best distance 0.270)
- run 2: pass  (best distance 0.270)
- run 3: pass  (best distance 0.270)

What are the walk-in hours for the health center?
- run 1: pass  (best distance 0.138)
- run 2: pass  (best distance 0.138)
- run 3: pass  (best distance 0.138)

Does the campus bookstore price-match?
- run 1: pass  (best distance 0.228)
- run 2: pass  (best distance 0.228)
- run 3: pass  (best distance 0.228)

### Criteria 2

generate.py::answer_from_chunks

Based on the documents, it is cold from mid-November to early March. 

Source: winter_gear.txt

According to winter_gear.txt, it is cold from mid-November to early March.

It gets cold from mid-November to early March (winter_gear.txt).

It takes four minutes to go from Aldridge Hall to the science quad (housing_aldridge_hall.txt, transit_walking.txt).

It takes four minutes to go from Aldridge Hall to the science quad (housing_aldridge_hall.txt and transit_walking.txt).

It takes four minutes to go from Aldridge Hall to the science quad (housing_aldridge_hall.txt and transit_walking.txt).

You can add a course through the end of the second week (admin_add_drop_deadline.txt).

You can add a course through the end of the second week (admin_add_drop_deadline.txt).

You can add a course through the end of the second week (admin_add_drop_deadline.txt).

The walk-in hours for the health centre are 8am to 11am (health_center.txt).

The walk-in hours for the health centre are from 8am to 11am (health_center.txt).

The walk-in hours for the health centre are from 8am to 11am (health_center.txt).

Yes, the campus store price-matches, though it is not advertised and you have to ask at the counter with the other listing on your phone (money_textbooks.txt).

Yes, the campus store price-matches, though it is not advertised and requires you to ask at the counter with the other listing on your phone (money_textbooks.txt).

Yes, the campus store price-matches, though it is not advertised and you have to ask at the counter with the other listing on your phone (money_textbooks.txt).

### Criteria 3

run_eval.py::check_out_of_scope

Out-of-scope questions (the gate should refuse these):
- refused  (best distance 0.787)  What is the capital of Mongolia?
- refused  (best distance 0.866)  How do I change the oil in a diesel engine?
- refused  (best distance 0.819)  Who won the 1994 World Cup?
- refused  (best distance 0.840)  What is the recommended dosage of ibuprofen for a headache?
- refused  (best distance 0.837)  How do I write a for loop in Rust?
     -> gate refused 5 of 5

### Criteria 4

chunker.py::split_documents

Print output generated by commented code in scorer.py::judge

During winter, when does it get cold?
- What winter is actually like here: Cold from mid-November to early March, with about three weeks in January where it stays below freezing all day.
- What winter is actually like here: The paths get cleared by 7am on weekdays and considerably later on weekends.
- Walking times across campus: Add four minutes in winter. The path past the pond genuinely ices over and people take the long way round.
  run 1: pass  (best distance 0.336)
- What winter is actually like here: Cold from mid-November to early March, with about three weeks in January where it stays below freezing all day.
- What winter is actually like here: The paths get cleared by 7am on weekdays and considerably later on weekends.
- Walking times across campus: Add four minutes in winter. The path past the pond genuinely ices over and people take the long way round.
  run 2: pass  (best distance 0.336)
- What winter is actually like here: Cold from mid-November to early March, with about three weeks in January where it stays below freezing all day.
- What winter is actually like here: The paths get cleared by 7am on weekdays and considerably later on weekends.
- Walking times across campus: Add four minutes in winter. The path past the pond genuinely ices over and people take the long way round.
  run 3: pass  (best distance 0.336)

What is the rough time that it takes to go from Aldridge Hall to the science quad?
- Aldridge Hall — what it's actually like: The good: closest building to the science quad, four minutes to a 9am lab.
- Walking times across campus: Aldridge Hall to the science quad: 4 minutes.
- Aldridge Hall — what it's actually like: The bad: the elevator is out roughly one week per semester.
  run 1: pass  (best distance 0.280)
- Aldridge Hall — what it's actually like: The good: closest building to the science quad, four minutes to a 9am lab.
- Walking times across campus: Aldridge Hall to the science quad: 4 minutes.
- Aldridge Hall — what it's actually like: The bad: the elevator is out roughly one week per semester.
  run 2: pass  (best distance 0.280)
- Aldridge Hall — what it's actually like: The good: closest building to the science quad, four minutes to a 9am lab.
- Walking times across campus: Aldridge Hall to the science quad: 4 minutes.
- Aldridge Hall — what it's actually like: The bad: the elevator is out roughly one week per semester.
  run 3: pass  (best distance 0.280)

How long after the term starts can you add a course?
- On the add/drop deadline: You can add a course through the end of the second week.
- Registration and your adviser: Popular courses fill in the first two days.
- On the declaring a major: You declare at the end of your second semester, or later if you need to.
  run 1: pass  (best distance 0.270)
- On the add/drop deadline: You can add a course through the end of the second week.
- Registration and your adviser: Popular courses fill in the first two days.
- On the declaring a major: You declare at the end of your second semester, or later if you need to.
  run 2: pass  (best distance 0.270)
- On the add/drop deadline: You can add a course through the end of the second week.
- Registration and your adviser: Popular courses fill in the first two days.
- On the declaring a major: You declare at the end of your second semester, or later if you need to.
  run 3: pass  (best distance 0.270)

What are the walk-in hours for the health center?
- The health centre: Walk-in hours are 8am to 11am; everything after that is by appointment and appointments run about a week out.
- The health centre: If something is urgent, go at 8am and wait rather than booking.
- The health centre: Counselling is separate, in the same building, and has its own intake process with a shorter wait than people expect — usuallythree or four days for a first session.
  run 1: pass  (best distance 0.138)
- The health centre: Walk-in hours are 8am to 11am; everything after that is by appointment and appointments run about a week out.
- The health centre: If something is urgent, go at 8am and wait rather than booking.
- The health centre: Counselling is separate, in the same building, and has its own intake process with a shorter wait than people expect — usuallythree or four days for a first session.
  run 2: pass  (best distance 0.138)
- The health centre: Walk-in hours are 8am to 11am; everything after that is by appointment and appointments run about a week out.
- The health centre: If something is urgent, go at 8am and wait rather than booking.
- The health centre: Counselling is separate, in the same building, and has its own intake process with a shorter wait than people expect — usuallythree or four days for a first session.
  run 3: pass  (best distance 0.138)

Does the campus bookstore price-match?
- Textbooks without paying full price: The campus store price-matches, which is not advertised anywhere and you have to ask at the counter with the other listing on your phone.
- On the printing quota: Every student gets $30 of printing per semester, which is roughly 600 black-and-white pages.
- Textbooks without paying full price: The library holds one copy of most required texts on two-hour reserve.
  run 1: pass  (best distance 0.228)
- Textbooks without paying full price: The campus store price-matches, which is not advertised anywhere and you have to ask at the counter with the other listing on your phone.
- On the printing quota: Every student gets $30 of printing per semester, which is roughly 600 black-and-white pages.
- Textbooks without paying full price: The library holds one copy of most required texts on two-hour reserve.
  run 2: pass  (best distance 0.228)
- Textbooks without paying full price: The campus store price-matches, which is not advertised anywhere and you have to ask at the counter with the other listing on your phone.
- On the printing quota: Every student gets $30 of printing per semester, which is roughly 600 black-and-white pages.
- Textbooks without paying full price: The library holds one copy of most required texts on two-hour reserve.
  run 3: pass  (best distance 0.228)

### Criteria 5

Enough to miss the original criteria definition:

What are the walk-in hours for the health center?
  [rate limit] service pushed back. Retrying in 1s (attempt 1 of 50).
  [rate limit] service pushed back. Retrying in 2s (attempt 2 of 50).
  [rate limit] service pushed back. Retrying in 4s (attempt 3 of 50).
  [rate limit] service pushed back. Retrying in 8s (attempt 4 of 50).

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | LLM Judge responses showed all chunks met the expectations |
| 2 | Every answer names a valid source | MET | Checked a source with a valid filename was returned in the response from the run log |
| 3 | Gate stops out-of-corpus questions | MET | Checked if the responses was "I don't have enough information" for each out-of-corpus question |
| 4 | Chunks are formatted correctly as sentences with document headers prepended and bounded by one terminal punctuation mark | MISSED | Printed all chunks for the evaluation and validated their formatting. Some had strange missing spaces in the header. |
| 5 | Responses are provided within 10 seconds | MISSED | Mentally noted time before and after responses. API limits blocked a few of the responses. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:** Added hybrid search that does keyword matching on top of semantic search.

- **Keyword search (`bm25.py`):** a BM25 index (`rank-bm25`) built from the chunks already stored in Chroma. It's rebuilt at query time instead of saved to disk, so it can never fall out of sync with the semantic index.
- **Tokenizer (`bm25.py::tokenize`):** used on both chunks and questions. It lowercases the text, strips punctuation and removes NLTK's English stopwords. It also keeps course codes as a single token ("CS 340" → `cs340`) using the regex `[A-Z]{2,5} ?\d{2,4}`, which only matches capital letters. Case-insensitive, the same pattern also matched phrases like "about 40" throughout the corpus. BM25 runs on the whole chunk, header included, because building and course names like "Aldridge Hall" and "CS 340" only appear in the headers.
- **Fusion (`bm25.py::hybrid_search`, called from `store.py::search`):** takes the top 10 chunks from each method and gives every candidate both scores. A chunk only BM25 found gets its real cosine distance, computed from its stored embedding. The two scores are then blended into one lower-is-better number:
  `fused_distance = 1 − [0.7 · (1 − semantic_distance) + 0.3 · bm25 / (bm25 + 11.16)]`
  Keywords get less weight than meaning (α = 0.7). The BM25 score is squashed with a fixed constant rather than min-max normalized per query. With min-max, the top keyword hit would always score 1.0, even for "What is the capital of Mongolia?". `11.16` is the median top BM25 score of my five in-scope questions (`python bm25.py`), so a typical good keyword match counts for about half.
- **Gate:** now checks the fused distance. I re-ran the 10 Unit 1 questions: in-scope questions scored 0.246–0.404 and out-of-scope questions 0.798–0.888, so the 0.6 cutoff still sits in the gap and I kept it.
- **Settings:** `config.py` has `HYBRID`, `ALPHA`, `BM25_C` and `CANDIDATES`. Setting `AI201_HYBRID=0` restores the original semantic-only search.
- **Debugging:** `python app.py retrieve` now prints the fused, semantic and BM25 scores for each chunk. Installed NLTK for stopword removal. Indexes BM25 every query so that the 

**Why I picked it:** Retrieval already passed all criteria, so this doesn't fix a miss. It improves ranking: for the Aldridge Hall question, the chunk with the direct answer ('Aldridge Hall to the science quad: 4 minutes') moved from rank 2 to rank 1.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4 of 5 | 4 of 5 | 4 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks are formatted correctly | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. E2E time is 10 seconds or less | 10 seconds | Rate limit but yes otherwise | | | MISSED |

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| During winter, when does it get cold? | pass | pass | pass |
| What is the rough time that it takes to go from Aldridge Hall to the science quad? | pass | pass | pass |
| How long after the term starts can you add a course? | pass | pass | pass |
| What are the walk-in hours for the health center? | pass | pass | pass |
| Does the campus bookstore price-match? | fail | fail | fail |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

The change helped but presumably it was marginal with the rank increase of the Aldrich Hall question. After changes the LLM judge started reporting a miss on the last question so there was some regression.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

I ran out of time overall to work on this. E2E time would be fixed with a more capable API setup. Nothing else was tightened but I tried my best to add hybrid search to the project to get some exposure. I'm not sure exactly how effective the approach is currently since I didn't get around to testing the system independently. There was a rank improvement in the chunks before and after.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I think I would possibly keep the criteria similar. I might add more questions so the data is more reliable. I might also add more total questions because I used exact language in a lot of the tests so rewordings might be useful to add. Near misses also use up the API so I think tuning and getting more test metrics might mitigate some of the cost using the model.
