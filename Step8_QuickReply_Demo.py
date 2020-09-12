#!/usr/bin/env python
# coding: utf-8

'''

當用戶輸入特定文字消息時，會啟用快速回覆功能。

此功能，可讓用戶直接透過點擊按鈕的方式，對問題進行多種既定答案的回覆。

'''

"""

啟用伺服器基本樣板

"""
# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 
from linebot.exceptions import (
    InvalidSignatureError
)

# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# 載入設定檔

import json
secretFileContentJson=json.load(open("./line_secret_key",'r',encoding="utf-8"))
server_url=secretFileContentJson.get("server_url")


# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/" )

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

'''
QuickReply篇

使用流程

準備QuickReply的Button

以QuickReply封裝該些QuickReply Button

製作TextSendMessage，並將剛封裝的QuickReply放入

'''

'''

準備QuickReply的Button


'''

# 引入相關套件
from linebot.models import (
    MessageAction, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    QuickReply, QuickReplyButton)

# 創建QuickReplyButton 

## 點擊後，以用戶身份發送文字消息
## MessageAction
textQuickReplyButton = QuickReplyButton(
    action=MessageAction(
        label="發送文字消息", 
        text="text2"))

## 點擊後，彈跳出選擇時間之視窗
## DatetimePickerAction
dateQuickReplyButton = QuickReplyButton(
    action=DatetimePickerAction(
        label="時間選擇",
        data="data3",                       
        mode="date"))


## 點擊後，開啟相機
## CameraAction
cameraQuickReplyButton = QuickReplyButton(
    action=CameraAction(label="拍照"))

## 點擊後，切換至照片相簿選擇
cameraRollQRB = QuickReplyButton(
    action=CameraRollAction(label="選擇照片"))

## 點擊後，跳出地理位置
locationQRB = QuickReplyButton(
    action=LocationAction(label="地理位置"))

## 點擊後，以Postback事件回應Server 
postbackQRB = QuickReplyButton(
    action=PostbackAction(label="我是PostbackEvent", data="data1"))

'''

以QuickReply封裝該些QuickReply Button

'''
## 設計QuickReplyButton的List
quickReplyList = QuickReply(
    items = [textQuickReplyButton, dateQuickReplyButton, cameraQuickReplyButton,
             cameraRollQRB, locationQRB,postbackQRB])

'''

製作TextSendMessage，並將剛封裝的QuickReply放入

'''
## 將quickReplyList 塞入TextSendMessage 中 
from linebot.models import (
    TextSendMessage,
)
quickReplyTextSendMessage = TextSendMessage(text='發送問題給用戶，請用戶回答', quick_reply=quickReplyList)

'''

設計一個字典

'''
template_message_dict = {
    "[::text:]reply":quickReplyTextSendMessage}

'''

用戶發送文字消息時，會按此進行消息處理

'''

# 用戶發出文字消息時， 按條件內容, 回傳合適消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text))

'''

啟動Server

'''
if __name__ == "__main__":
    app.run(host='0.0.0.0')

