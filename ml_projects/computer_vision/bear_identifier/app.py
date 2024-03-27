from src.pipeline.predict_pipeline import classify_bear
import gradio as gr
# Create Gradio interface
image_input = gr.components.Image()
label = gr.components.Label()
# Create interface
iface = gr.Interface(fn=classify_bear, inputs=image_input, outputs=label, title="Bear Identifier")
iface.launch(inline=False)
# prediction = PredictPipeline()
# print(prediction.predict('black_bear.jpg'))