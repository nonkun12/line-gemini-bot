import os
<<<<<<< HEAD
import google.generativeai as genai
from flask import Flask, request

app = Flask(__name__)

# APIキーの設定
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def index():
    # 起動時に一度だけモデル一覧をログに出力する
    model_list = []
    print("--- 利用可能なモデル一覧 ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"モデル名: {m.name}")
            model_list.append(m.name)
    print("--------------------------")
    return f"Available models: {', '.join(model_list)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
=======
import certifi
import google.generativeai as genai
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

# 設定の読み込み
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

configuration = Configuration(access_token=os.environ.get("LINE_ACCESS_TOKEN"))
configuration.ssl_ca_cert = certifi.where()
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

# --- ここが最も重要です ---
@app.route("/", methods=['GET'])
def index():
    return "Bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature error")
        abort(400)
    return 'OK'
# --------------------------

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        try:
            response = model.generate_content(event.message.text)
            reply_text = response.text
        except Exception as e:
            print(f"Gemini Error: {e}")
            reply_text = "AIの回答生成中にエラーが発生しました。"
            
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 10000)))
>>>>>>> fix route
