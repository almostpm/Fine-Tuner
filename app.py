import gradio as gr
from linter import grade_prompt
from optimizer import optimize_prompt

# Custom CSS to keep the dark, developer-friendly aesthetic
custom_css = """
body { background-color: #1e1e1e; }
.gradio-container { background-color: #1e1e1e; color: #d4d4d4; }
#header { text-align: center; color: #4CAF50; }
#status-box { font-weight: bold; }
"""

def process_prompt(prompt):
    """
    Core function that connects the Gradio UI to the Fine Tuner engine.
    It takes a raw prompt, grades it, and returns the optimized version.
    """
    if not prompt.strip():
        return "⚠️ Please enter a prompt first.", "", ""

    lint_result = grade_prompt(prompt)
    opt_result = optimize_prompt(prompt)

    # Format the grade and feedback for display
    status_text = f"Grade: {lint_result['grade']} | {lint_result['feedback']}"
    
    return status_text, opt_result["optimized"], ""

# Build the Gradio interface
with gr.Blocks(css=custom_css, title="Fine Tuner") as demo:
    gr.Markdown("# 🛠️ Fine Tuner Studio", elem_id="header")
    gr.Markdown("Optimize your prompts for better AI results.")
    
    with gr.Row():
        with gr.Column():
            raw_input = gr.Textbox(
                label="Raw Prompt", 
                placeholder="Paste your weak prompt here...", 
                lines=8
            )
            process_btn = gr.Button("Lint & Optimize", variant="primary")
            status_output = gr.Textbox(
                label="Lint Result", 
                interactive=False, 
                elem_id="status-box"
            )
        
        with gr.Column():
            optimized_output = gr.Textbox(
                label="Optimized Output", 
                lines=12, 
                interactive=False
            )
    
    # Connect the button click to the processing function
    process_btn.click(
        fn=process_prompt,
        inputs=raw_input,
        outputs=[status_output, optimized_output, raw_input]
    )

if __name__ == "__main__":
    # Allow Render to inject the PORT environment variable
    import os
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)