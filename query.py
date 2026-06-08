"""
Query System for UIC Restaurant Reviews
Milestone 5: Grounded Response Generation with Groq LLM
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb

# Load environment variables
load_dotenv()

# Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "restaurant_reviews"

# Global variables (loaded once)
_model = None
_collection = None
_client = None

def load_models():
    """Load embedding model and ChromaDB collection (lazy loading)."""
    global _model, _collection, _client
    
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = _client.get_collection(COLLECTION_NAME)
        print("Loaded ChromaDB collection")
    
    return _model, _collection

def retrieve(query, top_k=TOP_K):
    """Retrieve top-k relevant chunks for a query."""
    model, collection = load_models()
    
    # Embed the query
    query_embedding = model.encode([query])
    
    # Search in ChromaDB
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    # Format results
    retrieved_chunks = []
    for i in range(len(results["documents"][0])):
        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_id": results["metadatas"][0][i]["chunk_id"],
            "distance": results["distances"][0][i]
        })
    
    return retrieved_chunks

def build_prompt(query, retrieved_chunks):
    """
    Build a grounded prompt for the LLM.
    Instructs the model to ONLY use the provided context.
    """
    # Combine chunks into context
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        context_parts.append(f"[Document {i}] Source: {chunk['source']}\n{chunk['text']}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Build the prompt with grounding instructions
    prompt = f"""You are RulesBot, a helpful assistant that answers questions about UIC restaurants using ONLY the provided documents.

IMPORTANT RULES:
1. ONLY use information from the documents below to answer
2. If the documents don't contain enough information, say "I don't have enough information to answer that question"
3. Do NOT use your general knowledge about restaurants
4. Cite which document(s) your answer comes from

DOCUMENTS:
{context}

USER QUESTION: {query}

YOUR ANSWER (with source citations):"""
    
    return prompt

def generate_answer(query, retrieved_chunks):
    """
    Generate a grounded answer using Groq LLM.
    """
    # Initialize Groq client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    client = Groq(api_key=api_key)
    
    # Build the prompt
    prompt = build_prompt(query, retrieved_chunks)
    
    # Call the LLM
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions strictly from provided documents. Never use external knowledge. Always cite your sources."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,  # Lower temperature = more focused, less creative
        max_tokens=500
    )
    
    answer = completion.choices[0].message.content
    return answer

def extract_sources(retrieved_chunks):
    """Extract unique source names from retrieved chunks."""
    sources = list(set([chunk["source"] for chunk in retrieved_chunks]))
    return sources

def ask(question):
    """
    Main function: retrieve, generate, and return answer with sources.
    """
    print(f"\nQuestion: {question}")
    
    # Step 1: Retrieve relevant chunks
    print("Retrieving relevant chunks...")
    retrieved_chunks = retrieve(question)
    
    # Step 2: Check if we have any chunks
    if not retrieved_chunks:
        return {
            "answer": "I couldn't find any relevant documents to answer your question.",
            "sources": [],
            "retrieved_chunks": []
        }
    
    # Step 3: Generate grounded answer
    print("Generating answer with Groq LLM...")
    answer = generate_answer(question, retrieved_chunks)
    
    # Step 4: Extract sources
    sources = extract_sources(retrieved_chunks)
    
    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks
    }

# Test function for command line
if __name__ == "__main__":
    print("="*60)
    print("RULESBOT - UIC RESTAURANT GUIDE")
    print("="*60)
    
    # Load models once
    load_models()
    
    while True:
        print("\n" + "-"*40)
        question = input("Enter your question (or 'exit' to quit): ")
        
        if question.lower() == 'exit':
            break
        
        result = ask(question)
        
        print("\n" + "="*40)
        print("ANSWER:")
        print("="*40)
        print(result["answer"])
        
        print("\n" + "="*40)
        print("SOURCES:")
        print("="*40)
        for source in result["sources"]:
            print(f"  • {source}")
        
        print("\n" + "="*40)
        print("RETRIEVED CHUNKS (for debugging):")
        print("="*40)
        for i, chunk in enumerate(result["retrieved_chunks"][:3], 1):
            print(f"\nChunk {i} (from {chunk['source']}):")
            print(f"{chunk['text'][:200]}...")