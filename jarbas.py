import os
import gradio as gr
from google import genai
from dotenv import load_dotenv
from google.genai import types
import json


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client()

with open('codeman.json', 'r', encoding='utf-8') as f:
    system_instruction = json.load(f)


system_instruction = json.dumps(system_instruction, indent=2, ensure_ascii=False)


chat = client.chats.create(
    model="gemini-2.5-flash",
    config= types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=1.7,
        top_p=0.9,
        top_k=50,
        max_output_tokens=2048,
    )
)

def gerar_resposta(user_message, chat_history):
    try:
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"


demo = gr.ChatInterface(
    fn=gerar_resposta,
    title="Atlas - Assistente Virtual",
    description="Submeta seu raciocínio. Atlas identifica falhas, confronta desculpas e exige precisão.",
)

if __name__ == "__main__":
    demo.launch(share=True)