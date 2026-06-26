import os
import flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = flask.Flask(__name__)

# 環境変数から取得
line_bot_api = LineBotApi(os.environ.get("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# モデル名をシンプルに指定
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/callback", methods=['POST'])
def callback():
    signature = flask.request.headers.get('X-Line-Signature')
    body = flask.request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Webhookエラー: {e}")
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_message = event.message.text
        # ここで発生するエラーを特定するためにプリント
        print(f"DEBUG: 受信メッセージ: {user_message}")
        
        response = model.generate_content(user_message)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response.text)
        )
    except Exception as e:
        print(f"Gemini APIエラー詳細: {str(e)}")

if __name__ == "__main__":
    app.run()
