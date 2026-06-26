import os
import flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai

app = flask.Flask(__name__)

# 環境変数チェック（ログに出して確認するため）
line_bot_api = LineBotApi(os.environ.get("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# モデルを明示的に指定
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route("/callback", methods=['POST'])
def callback():
    signature = flask.request.headers.get('X-Line-Signature')
    body = flask.request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Error handling webhook: {e}")
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        # AI生成
        response = model.generate_content(event.message.text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response.text))
    except Exception as e:
        print(f"Error in Gemini: {e}")
        # エラー時でもLINEに何も返さないと既読がつきにくいのでエラー文を送る
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="AIエラーが発生しました"))

if __name__ == "__main__":
    app.run()
