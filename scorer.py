def judge(question, expects, answer, results) -> bool:
    return expects.lower().strip() in answer.lower()

    """
    LLM as judge, can get expensive
    rapidfuzz
    """


# def retrieval_hits(expects, results) -> bool:
#     """
#     Any part of my expect in the results
#     """

#     return any(expects.strip().lower() for chunk in results)

"""
Criteria for evaluation:
1. Check if chunks have the correct answer, LLM judge
2. Every answer names a source filename
3. Relevance gate stops out-of-corpus questions
4. Chunk format is correct
5. Questions asked are returned within 10 seconds
"""

def answer_in_chunks(expects, results) -> bool:
    """
    Check if the expected answer is present in any of the result chunks
    Uses LLM judge to determine if the expected answer is present in any of the result chunks
    """
    return any(expects.strip().lower() in chunk.lower() for chunk in results)


def answer_names_source(answer) -> bool:
    """
    Check if the answer names a source filename
    """
    pass


def gate_stops_out_of_corpus_questions(questions, results) -> bool:
    """
    Check if the questions that are out of corpus are stopped by the relevance gate
    """
    pass


def validate_chunk_format(chunks) -> bool:
    """
    Check if the chunk format is correct
    """
    pass


def questions_returned_within_10_seconds(questions, results) -> bool:
    """
    Check if the questions asked are returned responses within 10 seconds
    """
    pass