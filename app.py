@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        # AIに応答生成
        response = model.generate_content(event.message.text)
        # 返信実行
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response.text)
        )
    except Exception as e:
        # ここが重要！エラーが出たらログに詳細を出す
        print(f"!!! エラー発生: {e} !!!")
