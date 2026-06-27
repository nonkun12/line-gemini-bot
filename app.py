import os
import flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from google import genai

app = flask.Flask(__name__)

# ★ここが重要：ルート（/）へのアクセスに反応するようにする
@app.route("/", methods=['GET'])
def home():
    return "Bot is running", 200

line_bot_api = LineBotApi(os.environ.get("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = flask.request.headers.get('X-Line-Signature')
    body = flask.request.get_data(as_text=True)
    handler.handle(body, signature)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=event.message.text,
    )
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response.text)
    )

if __name__ == "__main__":
    app.run()
