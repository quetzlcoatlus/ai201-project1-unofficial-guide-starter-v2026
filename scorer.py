from generate import generate

def judge(question, expects, answer, results) -> bool:
    """
    Question is the question asked
    Expects is the expected answer
    Answer is the actual answer provided
    Results are the chunks of text returned by the retrieval system
    """
    
    """
    Criteria for evaluation:
    Check if chunks have the correct answer, LLM judge
    Rest of criteria are by hand or in run_eval (i.e. criteria 3)
    """

    """
    Check if the expected answer is present in any of the result chunks
    Uses LLM judge to determine if the expected answer is present in any of the result chunks
    """

    prompt = f"Expected answer: {expects}\nResult chunks: {results}"

    system_prompt = """\
    You are an AI assistant that judges whether the expected answer \
    is present in the result chunks. The expected answer counts as \
    PRESENT if a chunk states the same fact, even in different words \
    or with extra detail around it. It is NOT present if a chunk merely \
    discusses the same topic, or if you have to combine outside \
    to determine the presence of the expected answer. \
    Respond with exactly two lines:
    REASON: <one sentence citing the chunk text that does or doesn't contain the expected answer>
    VERDICT: <PASS or FAIL>
    """

    # Considered adding a three-way verdit over binary i.e. PRESENT, ABSENT, UNCLEAR
    # For now, we stick to a binary verdict (PASS or FAIL)

    response = generate(prompt, system_prompt, False)
    # print("LLM response:", response)
    # print(f"Chunks for question - {question}:", results)
    # return True

    # If I wasn't time constrained, I'd test the LLM judge's accuracy against a set of known cases

    verdict = ""
    for line in response.splitlines():
        if line.startswith("VERDICT:"):
            verdict = line.split(":", 1)[1].strip()

    return verdict == "PASS"