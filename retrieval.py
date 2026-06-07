"""
Retrieval Pipeline for UIC Restaurant Reviews
Milestone 4: Embedding, Vector Store, and Semantic Search
"""

import json
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Configuration from planning.md
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

def load_chunks_from_json(chunks_file="chunks.json"):
    """
    Load chunks and metadata from the JSON file created in Milestone 3.
    """
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunk_data = json.load(f)
    
    print(f"Loaded {len(chunk_data)} chunks from {chunks_file}")
    return chunk_data

def setup_embedding_model():
    """
    Load the sentence transformer model for embeddings.
    """
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    print("(This may take 20-30 seconds on first run - the model downloads)")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("Model loaded successfully")
    return model

def setup_chromadb():
    """
    Set up ChromaDB persistent client.
    """
    # Create a persistent ChromaDB client (saves to disk)
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if it exists (for fresh start)
    try:
        client.delete_collection("restaurant_reviews")
        print("Deleted existing collection")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection(
        name="restaurant_reviews",
        metadata={"description": "UIC restaurant reviews and recommendations"}
    )
    
    print("Created ChromaDB collection: restaurant_reviews")
    return collection

def embed_and_store(chunk_data, model, collection):
    """
    Generate embeddings for all chunks and store in ChromaDB with metadata.
    """
    chunks_text = []
    chunks_ids = []
    chunks_metadata = []
    
    for chunk in chunk_data:
        chunks_text.append(chunk["text"])
        chunks_ids.append(str(chunk["chunk_id"]))
        chunks_metadata.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "chunk_length": chunk["chunk_length"]
        })
    
    print(f"\nGenerating embeddings for {len(chunks_text)} chunks...")
    embeddings = model.encode(chunks_text)
    print(f"Embeddings shape: {embeddings.shape}")
    
    print("\nStoring chunks in ChromaDB...")
    collection.add(
        documents=chunks_text,
        embeddings=embeddings.tolist(),
        ids=chunks_ids,
        metadatas=chunks_metadata
    )
    
    print(f"Successfully stored {collection.count()} chunks")
    return collection

def retrieve(query, collection, model, top_k=TOP_K):
    """
    Retrieve top-k most relevant chunks for a query.
    Returns list of (chunk_text, metadata, distance_score) tuples.
    """
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

def test_retrieval(collection, model, test_queries):
    """
    Test retrieval with evaluation queries and print results.
    """
    print("\n" + "="*60)
    print("RETRIEVAL TESTING")
    print("="*60)
    
    for query in test_queries:
        print(f"\n\nQuery: {query}")
        print("-"*40)
        
        results = retrieve(query, collection, model)
        
        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (distance: {result['distance']:.4f})")
            print(f"Source: {result['source']}")
            print(f"Text: {result['text'][:300]}...")
            
            # Highlight if distance is high (bad match)
            if result['distance'] > 0.6:
                print("[WARNING: High distance score - weak match]")
        
        print("\n" + "="*40)

def run_retrieval_pipeline():
    """
    Main pipeline: load chunks, embed, store, and test retrieval.
    """
    print("="*60)
    print("RETRIEVAL PIPELINE - MILESTONE 4")
    print("="*60)
    
    # Step 1: Load chunks from Milestone 3
    print("\n[1] Loading chunks from chunks.json...")
    chunk_data = load_chunks_from_json()
    
    # Step 2: Set up embedding model
    print("\n[2] Setting up embedding model...")
    model = setup_embedding_model()
    
    # Step 3: Set up ChromaDB
    print("\n[3] Setting up ChromaDB...")
    collection = setup_chromadb()
    
    # Step 4: Embed and store
    print("\n[4] Generating embeddings and storing in ChromaDB...")
    embed_and_store(chunk_data, model, collection)
    
    # Step 5: Test retrieval with evaluation queries
    print("\n[5] Testing retrieval...")
    
    # Your 5 evaluation questions from planning.md
    test_queries = [
        "What do students say about the price at Ghareeb Nawaz?",
        "Which coffee shop near UIC is good for studying?",
        "What restaurant do students recommend avoiding near UIC?",
        "Is Noodles Etc walkable from UIC campus?",
        "What's a cheap late-night food option near UIC?"
    ]
    
    test_retrieval(collection, model, test_queries)
    
    # Summary
    print("\n" + "="*60)
    print("PIPELINE SUMMARY")
    print("="*60)
    print(f"Total chunks embedded: {collection.count()}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print(f"Top-k setting: {TOP_K}")
    print("\nRetrieval pipeline complete!")
    print("You can now query the system with: retrieve('your question', collection, model)")
    
    return collection, model

def interactive_query(collection, model):
    """
    Optional: Interactive query mode for testing.
    """
    print("\n" + "="*60)
    print("INTERACTIVE QUERY MODE")
    print("Type 'exit' to quit")
    print("="*60)
    
    while True:
        query = input("\nEnter your question: ")
        if query.lower() == 'exit':
            break
        
        results = retrieve(query, collection, model)
        
        print(f"\nTop {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n[{i}] (distance: {result['distance']:.4f})")
            print(f"Source: {result['source']}")
            print(f"Text: {result['text'][:250]}...")

if __name__ == "__main__":
    collection, model = run_retrieval_pipeline()
    
    # Ask if user wants interactive mode
    print("\n")
    response = input("Enter interactive query mode? (y/n): ")
    if response.lower() == 'y':
        interactive_query(collection, model)