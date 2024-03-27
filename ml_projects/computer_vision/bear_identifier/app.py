from src.pipeline.predict_pipeline import classify_bear
import gradio as gr

# Create Gradio interface components
image_input = gr.components.Image()
label = gr.components.Label()

# Create interface
iface = gr.Interface(fn=classify_bear, inputs=image_input, outputs=label, title="Bear Identifier")
iface.launch(inline=False)