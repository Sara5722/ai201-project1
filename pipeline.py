"""
Document Pipeline for UIC Restaurant Reviews
Milestone 3: Ingestion, Cleaning, and Chunking
"""

import os
import re
from pathlib import Path

# Configuration from planning.md
CHUNK_SIZE = 400  # characters
CHUNK_OVERLAP = 50  # characters

def load_documents(data_folder="data"):
    """
    Load all .txt files from the data folder.
    Returns a list of (filename, content) tuples.
    """
    documents = []
    data_path = Path(data_folder)
    
    if not data_path.exists():
        print(f"Error: {data_folder} folder not found!")
        print("   Create a 'data' folder and add your .txt files.")
        return documents
    
    txt_files = list(data_path.glob("*.txt"))
    
    if not txt_files:
        print(f"Error: No .txt files found in {data_folder}/")
        print("   Add your document .txt files to the data folder.")
        return documents
    
    print(f"Found {len(txt_files)} text files")
    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    documents.append((file_path.name, content))
                    print(f"   Loaded: {file_path.name} ({len(content)} chars)")
                else:
                    print(f"   Skipped empty file: {file_path.name}")
        except Exception as e:
            print(f"   Error loading {file_path.name}: {e}")
    
    print(f"\nTotal documents loaded: {len(documents)}")
    return documents

def clean_document(text, filename):
    """
    Clean the document text by removing ONLY ads and UI elements.
    Keep prices, numbers, and original text structure.
    """
    original_length = len(text)
    
    # Remove the source URL line
    text = re.sub(r'^Source: https?://[^\s]+', '', text, flags=re.MULTILINE)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove markdown links but keep link text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove Reddit ads and promoted content (but NOT regular numbers)
    patterns_to_remove = [
        r'u/EverPassMedia avatar',
        r'u/Typeform avatar',
        r'•\s*Promoted',
        r'NFL Sunday Ticket for Business[^\n]*',
        r'EverPassMedia[^\n]*',
        r'everpass\.com[^\n]*',
        r'Thumbnail image:[^\n]*',
        r'promoted[^\n]*',
        r'advertisement[^\n]*',
        r'Subscribe[^\n]*',
        r'Sign Up[^\n]*',
        r'Read More\s*',
        r'View More\s*',
        r'Comments Section',
        r'chatgpt\.com[^\n]*',
        r'typeform\.com[^\n]*',
        r'meticulous\.ai[^\n]*',
    ]
    
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove Reddit usernames but KEEP the comment text
    text = re.sub(r'u/\w+\s+', '', text)
    
    # Clean up whitespace (but don't remove line structure)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    text = text.strip()
    
    cleaned_length = len(text)
    removed = original_length - cleaned_length
    
    if removed > 0:
        print(f"   Cleaned {filename}: removed {removed} chars ({removed/original_length*100:.1f}%)")
    
    return text

def chunk_text(text, filename, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Split text into chunks of specified size with overlap.
    Tries to break at sentence boundaries when possible.
    """
    chunks = []
    
    if not text:
        return chunks
    
    # Simple sentence boundary detection (period, exclamation, question mark followed by space)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence exceeds chunk size, save current chunk and start new
        if len(current_chunk) + len(sentence) + 1 > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap from the end of previous chunk
            overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
            current_chunk = overlap_text + " " + sentence if overlap_text else sentence
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # Filter out any chunks that are too small (less than 20 chars) - probably noise
    chunks = [c for c in chunks if len(c) >= 20]

    # Cap chunks at 800 characters (if too long, split again)
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > 800:
            # Force split long chunks
            sub_chunks = [chunk[i:i+500] for i in range(0, len(chunk), 400)]
            final_chunks.extend(sub_chunks)
        else:
            final_chunks.append(chunk)

    return final_chunks
    
    

def inspect_chunks(chunks, num_samples=5):
    """
    Print sample chunks for inspection.
    """
    if not chunks:
        print("No chunks to inspect!")
        return
    
    print("\n" + "="*60)
    print("CHUNK INSPECTION")
    print("="*60)
    
    # Get random samples if we have enough
    import random
    sample_indices = random.sample(range(len(chunks)), min(num_samples, len(chunks)))
    
    for i, idx in enumerate(sample_indices, 1):
        chunk = chunks[idx]
        print(f"\n[Sample {i}] (Length: {len(chunk)} chars)")
        print("-" * 40)
        print(chunk[:400])  # Show first 400 chars
        if len(chunk) > 400:
            print("... (truncated)")
        print("-" * 40)

def save_chunks(chunks, metadata_list, output_file="chunks.json"):
    """
    Save chunks with metadata to a JSON file for later use.
    """
    import json
    
    chunk_data = []
    for i, (chunk, metadata) in enumerate(zip(chunks, metadata_list)):
        chunk_data.append({
            "chunk_id": i,
            "text": chunk,
            "source": metadata.get("source", "unknown"),
            "chunk_length": len(chunk)
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunk_data, f, indent=2)
    
    print(f"\nSaved {len(chunk_data)} chunks to {output_file}")
    return chunk_data

def run_pipeline():
    """
    Main pipeline function: load, clean, chunk, and inspect.
    """
    print("="*60)
    print("DOCUMENT PIPELINE - MILESTONE 3")
    print("="*60)
    print()
    
    # Step 1: Load documents
    print("[1] Loading documents...")
    documents = load_documents()
    
    if not documents:
        print("Pipeline stopped: No documents loaded.")
        return None, None
    
    print()
    
    # Step 2: Clean each document
    print("[2] Cleaning documents...")
    cleaned_docs = []
    for filename, content in documents:
        cleaned = clean_document(content, filename)
        cleaned_docs.append((filename, cleaned))
    
    print()
    
    # Step 3: Chunk each document
    print("[3] Chunking documents...")
    all_chunks = []
    chunk_metadata = []
    
    for filename, content in cleaned_docs:
        chunks = chunk_text(content, filename)
        for chunk in chunks:
            all_chunks.append(chunk)
            chunk_metadata.append({"source": filename})
    
    print()
    print(f"Total chunks created: {len(all_chunks)}")
    
    # Step 4: Inspect chunks
    print("[4] Inspecting chunks...")
    inspect_chunks(all_chunks)
    
    # Step 5: Save chunks for next milestone
    print("\n[5] Saving chunks...")
    save_chunks(all_chunks, chunk_metadata)
    
    # Summary
    print("\n" + "="*60)
    print("PIPELINE SUMMARY")
    print("="*60)
    print(f"Documents processed: {len(documents)}")
    print(f"Total chunks created: {len(all_chunks)}")
    print(f"Average chunk size: {sum(len(c) for c in all_chunks)/len(all_chunks):.0f} chars")
    print(f"Chunk size range: {min(len(c) for c in all_chunks)} - {max(len(c) for c in all_chunks)} chars")
    
    # Validation check from planning.md
    if len(all_chunks) < 50:
        print("\nWarning: Fewer than 50 chunks created.")
        print("Your chunks may be too large. Consider reducing chunk size.")
    elif len(all_chunks) > 2000:
        print("\nWarning: More than 2000 chunks created.")
        print("Your chunks may be too small. Consider increasing chunk size.")
    else:
        print("\nChunk count is within recommended range (50-2000).")
    
    return all_chunks, chunk_metadata

if __name__ == "__main__":
    chunks, metadata = run_pipeline()