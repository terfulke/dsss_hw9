from langchain_ollama import OllamaLLM
import requests
from datetime import datetime

bot_token = "......"    # here is my bot_token
base_url = f"https://api.telegram.org/bot{bot_token}"
log_file = "messages.log"

model = OllamaLLM(model="llama3")

def query_ollama(prompt):
    response = model.invoke(input=prompt)
    return response

def get_updates(offset=None):
    url = f"{base_url}/getUpdates"
    params = {"offset": offset, "timeout": 10}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = f"{base_url}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    return response.json()

def log_message(message):
    with open(log_file, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {message}\n")

def main():
    print("Bot is running...")
    offset = None
    while True:
        updates = get_updates(offset)
        if updates.get("ok") and "result" in updates:
            for update in updates["result"]:
                message_text = update["message"]["text"]
                chat_id = update["message"]["chat"]["id"]

                log_message(message_text)
                if message_text == "\start":
                    response = "Hi, I am your bot, how can I help you?"
                    send_message(chat_id, response)
                else:
                    response = query_ollama(message_text)
                    send_message(chat_id, response)
                
                offset = update["update_id"] + 1

if __name__ == "__main__":
    main()
