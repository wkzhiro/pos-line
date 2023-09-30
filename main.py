import os
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Request, HTTPException
from typing import List
from linebot import (LineBotApi, WebhookHandler, WebhookParser)
from linebot.models import (MessageEvent, ImageMessage, TextMessage, TextSendMessage,ImageSendMessage,)
from linebot.exceptions import (InvalidSignatureError)

# FastAPIをインスタンス化
app = FastAPI()
#初期化
product_info = None
global_stock = 0

class LineWebhook(BaseModel):
    destination: str
    events: List[dict]

# LINE Botのシークレットとアクセストークン
# LINE Bot APIとWebhookHandlerをインスタンス化します。
# LINE Bot APIは、LINEのメッセージを送受信するためのAPIを提供します。
# WebhookHandlerは、Webhookからのイベントを処理するためのクラスです。
# 環境変数から設定を読み込む
CHANNEL_SECRET = os.environ.get("CHA_SECRET", "default_secret")
CHANNEL_ACCESS_TOKEN = os.environ.get("CHA_ACCESS", "default_access")

# LINE Bot APIを使うためのクライアントのインスタンス化
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# テキストメッセージのハンドリング
def handle_text_message(event):
    global global_stock
    text = event["message"]["text"]

    # ユーザーIDの取得
    user_id = event["source"]["userId"]
    #group_id = event["source"]["groupId"]
    reply_message = "ユウヒビールいかがですか？ " + "\n Message: " + text # + "Group ID: " + group_id

    # 応答メッセージ
    line_bot_api.reply_message(
        event["replyToken"],
        TextSendMessage(text=reply_message))
        

# /callbackへのPOSTリクエストを処理するルートを定義
@app.post("/callback/")
async def callback(webhook_data: LineWebhook):
    for event in webhook_data.events:
        if event["message"]["type"] == "text":
            #text = event["message"]["text"]
            handle_text_message(event)

    return {"status": "OK"}
