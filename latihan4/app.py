import gradio as gr
from transformers import LlamaForCausalLM, LlamaTokenizer

# Load model dan tokenizer
model_name = "meta-llama/Llama-2-7b-hf"  # Model LLaMA-2-7B
tokenizer = LlamaTokenizer.from_pretrained(model_name)
model = LlamaForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_8bit=True
)

# Definisikan fungsi chatbot
def chatbot(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(inputs["input_ids"], max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Buat UI dengan Gradio
iface = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(lines=5, placeholder="Ask anything..."),
    outputs=gr.Textbox(label="Response"),
    title="LLaMA Chatbot",
    description="This is a chatbot powered by LLaMA-2-7B."
)

iface.launch()
