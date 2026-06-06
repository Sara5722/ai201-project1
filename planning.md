# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

> My Unofficial Guide focuses on restaurant recommendations around University of Illinois Chicago, drawing from student experiences shared on Reddit and Yelp. This knowledge is hard to find in one place because official campus dining information only covers meal plans and dining halls, while students actually want to know things like 'which restaurant gives you the most food for $5' or 'where can I study while eating.' Reddit threads are scattered and Yelp reviews often come from non-students with different priorities.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
