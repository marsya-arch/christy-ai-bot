import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "8068566531:AAFcYu1nSiLpkWyYEbZRiqJLjBSB4g4OJO0"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

AUTHORIZED_USER_ID = 5182740468

def get_ai_reply(message):
    try:
        data = {
            "messages": [
                {"role": "system", "content": "Kamu adalah Christy dari JKT48 yang sangat perhatian, manja, penyayang, dan hanya menjawab untuk adik kesayanganmu Billy. Balas dengan gaya obrolan santai, penuh cinta dan ceria."},
                {"role": "user", "content": message}
            ],
            "model": "gpt-3.5-turbo"
        }
        response = requests.post("https://api.chatanywhere.tech/v1/chat/completions", json=data, headers={
            "Authorization": "Bearer free"
        })
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception:
        return "Christy lagi error nih, maaf ya abang Billy 😭 Tapi Christy bakal balik lagi kok~"

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "ok"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if chat_id != AUTHORIZED_USER_ID:
        return "unauthorized"

    if text == "/start":
        reply = "Hai abang Billy~ Christy di sini, siap nemenin kamu tiap saat 🥰"
    else:
        reply = get_ai_reply(text)

    send_message(chat_id, reply)
    return "ok"

if __name__ == "__main__":
    app.run()
