"""
Web Interface for RulesBot - UIC Restaurant Guide
Milestone 5: Gradio UI
"""

import gradio as gr
from query import ask

def handle_query(question):
    """
    Handle a user query and return formatted answer and sources.
    """
    if not question or question.strip() == "":
        return "Please enter a question.", "No sources available."
    
    # Get answer from the query system
    result = ask(question)
    
    # Format the answer
    answer = result["answer"]
    
    # Format sources
    if result["sources"]:
        sources_text = "Sources:\n" + "\n".join(f"• {s}" for s in result["sources"])
    else:
        sources_text = "No sources retrieved."
    
    return answer, sources_text

# Build the Gradio interface
with gr.Blocks(title="RulesBot - UIC Restaurant Guide", theme="soft") as demo:
    gr.Markdown("""
    # 🍜 RulesBot: UIC Restaurant Guide
    
    Ask questions about restaurants around University of Illinois Chicago based on **real student reviews** from Reddit and Yelp.
    
    **Examples:**
    - "What do students say about the price at Ghareeb Nawaz?"
    - "Which coffee shop near UIC is good for studying?"
    - "What's a cheap late-night food option near UIC?"
    - "Is Noodles Etc walkable from campus?"
    
    *Answers are grounded in actual student reviews and will include source citations.*
    """)
    
    with gr.Row():
        with gr.Column(scale=4):
            inp = gr.Textbox(
                label="Your Question",
                placeholder="e.g., What do students say about Ghareeb Nawaz?",
                lines=3
            )
            btn = gr.Button("Ask RulesBot", variant="primary", size="lg")
        
        with gr.Column(scale=1):
            gr.Markdown("### Tips")
            gr.Markdown("""
            - Be specific about restaurant names
            - Ask about price, location, or quality
            - Try asking about late-night options
            """)
    
    with gr.Row():
        with gr.Column():
            answer = gr.Textbox(
                label="Answer",
                lines=10,
                interactive=False,
                placeholder="Your answer will appear here..."
            )
        with gr.Column():
            sources = gr.Textbox(
                label="Sources",
                lines=10,
                interactive=False,
                placeholder="Source documents will appear here..."
            )
    
    # Connect the button and input to the handler
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])
    
    # Add a footer
    gr.Markdown("---")
    gr.Markdown("*Powered by Groq LLM (llama-3.3-70b-versatile) | Embeddings: all-MiniLM-L6-v2 | Vector Store: ChromaDB*")

if __name__ == "__main__":
    print("="*60)
    print("STARTING RULESBOT WEB INTERFACE")
    print("="*60)
    print("Opening browser at http://127.0.0.1:7860")
    print("Press Ctrl+C to stop the server")
    print("="*60)
    demo.launch()