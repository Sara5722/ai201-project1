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

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Reasoning:** My documents are primarily short student reviews (2-5 sentences) from Reddit and review sites. A 500-character chunk captures 1-2 complete reviews without mixing unrelated opinions about different restaurants. For example, a typical Yelp review for Ghareeb Nawaz is 300-400 characters, so each chunk will contain one full review. The 50-character overlap ensures that if a sentence straddles a chunk boundary (possible with longer Reddit comments), no information is lost. If I used 200-character chunks, important context like "the service is slow but the food is cheap and worth it" would be split apart. If I used 1000-character chunks, I might combine reviews about different restaurants that don't relate to each other, causing retrieval to return irrelevant information.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 5

**Production tradeoff reflection:** If I were deploying to real users with no cost constraints, I would weigh several tradeoffs. For context length, a model like all-mpnet-base-v2 (768 dimensions) captures more semantic nuance but is slower and requires more RAM. For multilingual support, if UIC has many international students asking in Spanish or Chinese, I would need a model like paraphrase-multilingual-MiniLM-L12-v2. For domain-specific accuracy on restaurant reviews with slang ("fire," "mid," "bussin"), a larger model or fine-tuned model would perform better. For latency, my current model is fast (<100ms per embedding) while OpenAI's text-embedding-3-small would add network latency and API costs. Since this is a prototype, local embeddings with no API key requirement is the right choice.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about the price at Ghareeb Nawaz? | Students mention it's very cheap/affordable, with $5-7 lunch specials and meals under $10. Reviews emphasize "cheap" and "budget-friendly." |
| 2 | Which coffee shop near UIC is good for studying? | Ground Up Coffee - reviews mention it's close to east campus, has a good atmosphere for studying, and is frequently visited by students. |
| 3 | What restaurant do students recommend avoiding near UIC? | Students say to avoid Joy Yee because of bland and not good food. |
| 4 | Is Noodles Etc walkable from UIC campus? | Yes, reviews specifically mention it's "walkable from the university" and conveniently located for students. |
| 5 | What's a cheap late-night food option near UIC? | Ghareeb Nawaz - multiple reviews mention it's open late (sometimes until midnight or later) and has affordable options for students after evening classes. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Noisy/inconsistent data:** Yelp reviews sometimes come from non-students (tourists, delivery drivers, locals) whose priorities differ from students. My retrieval might return a review complaining about parking availability when a student only cares about price, walkability, and speed of service. I'll need to carefully craft my LLM prompt to prioritize student-relevant criteria.

2. **Chunk boundary splitting information:** A long Reddit comment comparing three different restaurants (e.g., "Ghareeb Nawaz has cheap Indian food, Noodles Etc has good Thai, but Ground Up has the best study atmosphere") could get split across chunk boundaries. This might cause one restaurant's pros to be retrieved without the comparison context from another restaurant. My 50-character overlap helps but doesn't fully solve this for very long comments.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     ┌─────────────────┐
│ DOCUMENTS │
│ (URLs above) │
└────────┬────────┘
│
▼
┌─────────────────┐
│ INGESTION │
│ (read from │
│ URLs/files) │
└────────┬────────┘
│
▼
┌─────────────────┐
│ CHUNKING │
│ 500 chars, │
│ 50 char overlap│
└────────┬────────┘
│
▼
┌─────────────────┐
│ EMBEDDING │
│ all-MiniLM- │
│ L6-v2 │
└────────┬────────┘
│
▼
┌─────────────────┐
│ VECTOR STORE │
│ ChromaDB │
└────────┬────────┘
│
▼
┌─────────────────┐
│ RETRIEVAL │
│ top-k = 5 │
│ semantic search│
└────────┬────────┘
│
▼
┌─────────────────┐
│ GENERATION │
│ Groq LLM │
│ (llama-3.3- │
│ 70b-versatile) │
└────────┬────────┘
│
▼
┌─────────────────┐
│ OUTPUT │
│ Grounded answer│
│ + citations │
└─────────────────┘

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

**Milestone 3 — Ingestion and chunking:** I will use Claude/ChatGPT to implement the document ingestion and chunking functions. I'll provide my Chunking Strategy section (500 characters, 50 overlap) and ask it to write a `chunk_text()` function that respects these parameters. I'll also ask for a `load_documents()` function that can read from the URLs in my planning.md. I'll verify the output by running the function on a sample review and checking that chunks are the correct size and overlap correctly.

**Milestone 4 — Embedding and retrieval:**
I will use Claude/ChatGPT to implement the embedding pipeline and vector store setup. I'll provide my Retrieval Approach section (all-MiniLM-L6-v2 model, ChromaDB, top-k=5) and ask it to write code that generates embeddings for all chunks, stores them in ChromaDB, and implements a `retrieve(query)` function that returns the top-5 most semantically similar chunks. I'll verify by testing with a simple query like "cheap food" and checking that relevant chunks about Ghareeb Nawaz are returned.

**Milestone 5 — Generation and interface:**
I will use Claude/ChatGPT to implement the grounded response generation. I'll provide my evaluation questions as example prompts and ask it to write an LLM prompt template that: (1) uses ONLY the retrieved chunks as context, (2) includes source attribution/citations, (3) refuses to answer if the context doesn't contain relevant info. I'll also ask for a simple Gradio or command-line interface. I'll verify by running my 5 evaluation questions and checking that responses are grounded in the actual retrieved chunks (not hallucinated).
