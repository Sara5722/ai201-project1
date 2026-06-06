# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->


>  My Unofficial Guide focuses on restaurant recommendations around University of Illinois Chicago, drawing from student experiences shared on Reddit and Yelp. This knowledge is hard to find in one place because official campus dining information only covers meal plans and dining halls, while students actually want to know things like 'which restaurant gives you the most food for $5' or 'where can I study while eating.' Reddit threads are scattered and Yelp reviews often come from non-students with different priorities.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/uichicago - "Best food near UIC" thread|Reddit post | https://www.reddit.com/r/uichicago/comments/wr4a2v/food_around_uic/|
| 2 | r/uichicago - "Cheap eats around campus" thread| Reddit post | https://www.reddit.com/r/uichicago/comments/1njnktc/lunch_are_there_cheap_and_tasty_lunch_spots/|
| 3 | r/uichicago - "Restaurants to avoid near UIC" thread| Reddit post| https://www.reddit.com/r/uichicago/comments/13z4vuz/favorite_and_least_favorite_places_for_food/|
| 4 | r/uichicago - "Dining hall vs eating out" discussion | Reddit post| https://www.reddit.com/r/uichicago/comments/vpdzh1/how_is_the_dining_hall_food/|
| 5 | r/uichicago - "Late night food options UIC" thread| Reddit post| https://www.reddit.com/r/uichicago/comments/1g5d3dk/looking_for_great_lunch_and_dining_spots_near_uic/|
| 6 | Noodles Etc - Student reviews | Yelp/Wanderlog| https://wanderlog.com/place/details/2642678/noodles-etc-chicago|
| 7 | Ghareeb Nawaz - UIC student reviews| Sluurpy | https://www.sluurpy.us/chicago/restaurant/3809723/ghareeb-nawaz-uic/reviews|
| 8 | Ground Up Coffee - Campus coffee shop| SageMenu | https://sagemenu.com/chicago/ground-up-chicago/|
| 9 | Ghareeb Nawaz - Budget eats (second source)| MenuPix | https://www.menupix.com/chicago/restaurants/380211311/Ghareeb-Nawaz-Chicago-IL|
| 10 |Ground Up Coffee - Study spot reviews | MapQuest | https://www.mapquest.com/us/illinois/ground-up-377251653|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
