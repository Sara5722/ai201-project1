# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

My Unofficial Guide focuses on restaurant recommendations around University of Illinois Chicago, drawing from student experiences shared on Reddit and Yelp. This knowledge is hard to find in one place because official campus dining information only covers meal plans and dining halls, while students actually want to know things like 'which restaurant gives you the most food for $5' or 'where can I study while eating.' Reddit threads are scattered and Yelp reviews often come from non-students with different priorities.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/uichicago - "Food around UIC" | Reddit post | https://www.reddit.com/r/uichicago/comments/wr4a2v/food_around_uic/ |
| 2 | r/uichicago - "Cheap and tasty lunch spots" | Reddit post | https://www.reddit.com/r/uichicago/comments/1njnktc/lunch_are_there_cheap_and_tasty_lunch_spots/ |
| 3 | r/uichicago - "Favorite and least favorite places" | Reddit post | https://www.reddit.com/r/uichicago/comments/13z4vuz/favorite_and_least_favorite_places_for_food/ |
| 4 | r/uichicago - "How is the dining hall food?" | Reddit post | https://www.reddit.com/r/uichicago/comments/vpdzh1/how_is_the_dining_hall_food/ |
| 5 | r/uichicago - "Great lunch and dining spots" | Reddit post | https://www.reddit.com/r/uichicago/comments/1g5d3dk/looking_for_great_lunch_and_dining_spots_near_uic/ |
| 6 | Noodles Etc - Student reviews | Wanderlog | https://wanderlog.com/place/details/2642678/noodles-etc-chicago |
| 7 | Ghareeb Nawaz - UIC student reviews | Sluurpy | https://www.sluurpy.us/chicago/restaurant/3809723/ghareeb-nawaz-uic/reviews |
| 8 | Ground Up Coffee - Campus coffee shop | SageMenu | https://sagemenu.com/chicago/ground-up-chicago/ |
| 9 | Ghareeb Nawaz - Budget eats (second source) | MenuPix | https://www.menupix.com/chicago/restaurants/380211311/Ghareeb-Nawaz-Chicago-IL |
| 10 | Ground Up Coffee - Study spot reviews | MapQuest | https://www.mapquest.com/us/illinois/ground-up-377251653 |

---

## Chunking Strategy

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** My documents are primarily short student reviews (2-5 sentences) from Reddit and review sites. A 400-character chunk captures 1 complete review without mixing unrelated opinions about different restaurants. For example, a typical Yelp review for Ghareeb Nawaz is 300-400 characters, so each chunk contains one full review. The 50-character overlap ensures that if a sentence straddles a chunk boundary, no information is lost. I started with 500-character chunks but reduced to 400 after testing, as smaller chunks produced more focused retrieval for specific restaurant mentions.

**Final chunk count:** 142 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (384-dimensional embeddings)

**Production tradeoff reflection:** If I were deploying this system for real users with no cost constraints, I would weigh several tradeoffs. For context length, a model like all-mpnet-base-v2 (768 dimensions) captures more semantic nuance but is 2-3x slower and requires more RAM. For multilingual support, if UIC has international students asking in Spanish or Chinese, I would need a model like paraphrase-multilingual-MiniLM-L12-v2. For domain-specific accuracy on restaurant reviews with slang ("fire," "mid," "bussin"), a larger model or fine-tuned model would perform better. For latency, my current model is fast (<100ms per embedding) while OpenAI's text-embedding-3-small would add network latency and API costs. Since this is a prototype, local embeddings with no API key requirement is the right choice.

---

## Grounded Generation

**System prompt grounding instruction:** 
The system prompt used is: "You are a helpful assistant that answers questions strictly from provided documents. Never use external knowledge. Always cite your sources."

Additionally, the user prompt template explicitly instructs: "IMPORTANT RULES: 1. ONLY use information from the documents below to answer. 2. If the documents don't contain enough information, say 'I don't have enough information to answer that question.' 3. Do NOT use your general knowledge about restaurants. 4. Cite which document(s) your answer comes from."

**How source attribution is surfaced in the response:** The LLM is instructed to cite sources inline with document numbers (e.g., "According to Document 2 (Source: filename.txt)..."). The system also separately returns a list of unique source filenames displayed in the interface's "Sources" box. This dual attribution ensures transparency even if the LLM forgets to cite.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about the price at Ghareeb Nawaz? | Students mention it's very cheap/affordable, with $5-7 lunch specials. | According to documents, students say Ghareeb Nawaz has "inexpensive menu items" and is "super cheap" and "affordable," with meals available for "$5-$7". | Relevant | Accurate |
| 2 | Which coffee shop near UIC is good for studying? | Ground Up Coffee - close to east campus, good atmosphere for studying. | Ground Up coffee shop is "really close to UIC campus" and has a "great environment for studying" with polite staff. | Relevant | Accurate |
| 3 | What restaurant do students recommend avoiding near UIC? | Students say to avoid Joy Yee because of bland/poor quality food. | Students recommend avoiding a restaurant serving dry, bland Pad Thai with subpar boba tea, but the restaurant name isn't mentioned. Also mentions dissatisfaction with dining hall and United Table. | Partially Relevant | Partially Accurate |
| 4 | Is Noodles Etc walkable from UIC campus? | Yes, it's located within/near campus. | Noodles Etc is located "in the heart of Chicago's UIC campus," suggesting it is walkable. | Partially Relevant | Partially Accurate |
| 5 | What's a cheap late-night food option near UIC? | Ghareeb Nawaz - open late, affordable options. | System couldn't find specific late-night mentions but suggested Volcano for cheap sushi and ML Kitchen with student discount. None specifically mention late-night hours. | Partially Relevant | Partially Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** "What's a cheap late-night food option near UIC?"

**What the system returned:** "I don't have enough information to answer that question specifically about late-night options. However, I can suggest some affordable food options... Volcano... ML Kitchen... Neither of these documents specifically mentions late-night options..."

**Root cause (tied to a specific pipeline stage):** This is a **document collection failure**, not a retrieval or generation failure. My documents include discussions about cheap food and about late-night food separately, but none of the 10 sources explicitly mention a restaurant that is BOTH cheap AND open late. The Reddit thread about late-night food (source_5) focused on general lunch/dinner spots rather than actual late-night hours. The chunking and retrieval worked correctly - the system accurately reported that the information wasn't in the documents.

**What you would change to fix it:** I would add a dedicated source specifically about late-night dining, such as a Reddit thread asking "What restaurants near UIC are open after midnight?" or collect reviews from places known to stay open late (like Jim's Original or Taco Bell on Taylor Street). Alternatively, I could add metadata tags for "hours" to each chunk to enable filtering.

---

## Spec Reflection

**One way the spec helped you during implementation:** The planning.md forced me to think about chunk size before writing code. By explicitly stating 500 characters with 50 overlap, I had a concrete target to validate against. When retrieval initially performed poorly, I could trace the issue back to chunk size and adjust from 500 to 400 characters, updating the spec accordingly.

**One way your implementation diverged from the spec, and why:** I originally planned for 500-character chunks but changed to 400 characters during Milestone 4 after noticing that retrieval was returning chunks that mixed multiple restaurant reviews. The smaller chunk size produced more focused, single-restaurant chunks that improved semantic search accuracy. I updated planning.md to reflect this change.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My chunking strategy section from planning.md (500 characters, 50 overlap) and asked it to implement the `chunk_text()` function with sentence-boundary awareness.
- *What it produced:* A function using regex `r'(?<=[.!?])\s+'` to split on sentences, then building chunks with overlap.
- *What I changed or overrode:* I added a filter to remove chunks smaller than 20 characters (which were just whitespace or artifacts) and added a maximum chunk size cap of 800 characters to prevent runaway chunks.

**Instance 2**

- *What I gave the AI:* My retrieval approach section (all-MiniLM-L6-v2, ChromaDB, top-k=5) and asked for a complete retrieval pipeline.
- *What it produced:* Code for embedding generation, ChromaDB setup, and a `retrieve()` function returning chunks with distances.
- *What I changed or overrode:* I modified the cleaning function significantly, adding 20+ regex patterns to remove Reddit ads, promoted content, usernames, and timestamps. The original cleaning was too aggressive and removed price information (like $5-$7). I had to iterate on the patterns to preserve actual content while removing UI garbage.