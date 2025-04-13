import gradio as gr
import os
import requests
import json

# API Key from Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def chat_with_ai(history, user_input):
    """Sends user input to the Gemini API and returns AI response."""
    try:
        payload = {
            "contents": [{"role": "user", "parts": [{"text": user_input}]}],
            "generationConfig": {
                "temperature": 1,
                "topP": 0.95,
                "topK": 40,
                "maxOutputTokens": 1024
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            ai_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            history.append((user_input, f"🤖 {ai_response}"))  # Bot reply starts with 🤖 emoji
        else:
            history.append(("Error:", f"API Error {response.status_code}: {response.text}"))

        return history
    except Exception as e:
        return history + [("Error:", str(e))]

# Gradio Chat Interface
with gr.Blocks() as chat_interface:
    gr.Markdown("## <span style='color:yellow;'>AI Chat Assistant</span>", elem_id="ai-title")

    chatbot = gr.Chatbot(label="Chat with AI", height=500)
    user_input = gr.Textbox(placeholder="Type your message...", show_label=False)
    send_button = gr.Button("Send")

    gr.Markdown("""
    ## <span style='color:blue;'>Free AI Chat on Telegram 🚀</span>
    If you prefer to chat with AI on Telegram for **free**, try these bots:  
    - [**Gemini Chatbot**](http://t.me/gemini_chatbotbot) (`@gemini_chatbotbot`)  
    - [**Best Friend AI Bot**](http://t.me/bestfriend_aibot) (`@bestfriend_aibot`)  

    No API key needed, just start chatting instantly!  
    """, elem_id="telegram-info")

    gr.Markdown("""
    ## <span style='color:blue;'>Using Your Own API Key (Optional)</span>
    - If you want to use your own API key, **duplicate this Space or repo**.
    - Store your `GEMINI_API_KEY` in **Secrets** (Hugging Face Spaces) or as an **environment variable**.
    """, elem_id="api-info")

    def handle_user_input(history, user_message):
        return chat_with_ai(history, user_message), ""

    send_button.click(handle_user_input, inputs=[chatbot, user_input], outputs=[chatbot, user_input])

chat_interface.launch()