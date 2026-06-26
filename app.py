import os
import flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = flask.Flask(__name__)

# 環境変数の取得
line_bot_api = LineBotApi(os.environ.get("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# モデル名をフルパスで指定
model = genai.GenerativeModel('models/gemini-1.5-flash')

@app.route("/callback", methods=['POST'])
def callback():
    signature = flask.request.headers.get('X-Line-Signature')
    body = flask.request.get_data(as_text=True)
    handler.handle(body, signature)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    # 生成処理
    response = model.generate_content(user_message)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response.text)
    )

if __name__ == "__main__":
    app.run()
