# Milestone 1

python app.py --corpus advice_threads chunks -n 1 returns 26 chunks total

# Milestone 2

Acceptance Criteria: For at least 4 of my 5 test questions, the top results include a chunk containing the answer

Sample Questions:
1. During winter, when does it get cold?
2. What is the rough time that it takes to go from Aldridge Hall to the science quad?
3. How long after the term starts can you add a course?
4. What are the walk-in hours for the health center?
5. Does the campus bookstore price-match?

# Milestone 3

Considering paragraph chunking instead.

Every campus_life doc is: header line, blank line, then paragraphs. No !/?, no ellipses, no bullets, no real abbreviations — the only non-terminal periods are decimals like $1.75, and times are written 7:00pm / 2am. Every body already ends in a period.

# Milestone 4

Best cutoffs for questions
1. 0.336
2. 0.280
3. 0.270
4. 0.138
5. 0.228

1. 0.787
2. 0.866
3. 0.819
4. 0.840
5. 0.837