import os
from flask import Flask, request, jsonify
import requests
import libsql_client

app = Flask(__name__)

# خواندن اطلاعات از محیط سرور
BALE_TOKEN = os.environ.get("BALE_TOKEN")
TURSO_URL = os.environ.get("TURSO_URL")
TURSO_TOKEN = os.environ.get("TURSO_TOKEN")

# اتصال به دیتابیس Turso
url = TURSO_URL.replace("libsql://", "https://") if TURSO_URL else ""
client = libsql_client.create_client(url=url, auth_token=TURSO_TOKEN)

def send_message(chat_id, text):
    url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

# صفحه تست برای اینکه ببینیم سرور زنده است یا نه
@app.route('/', methods=['GET'])
def index():
    return "Bot server is running successfully!"

# آدرسی که بله پیام‌ها را به آن می‌فرستد
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    
    # بررسی اینکه پیام متنی باشد
    if update and "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        
        if text == "/start":
            send_message(chat_id, "سرور با موفقیت متصل شد! ✅\nربات آماده است.")
            
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
