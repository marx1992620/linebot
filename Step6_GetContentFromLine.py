#!/usr/bin/env python
# coding: utf-8

'''

用戶傳照片消息給Line

我方使用 消息的id 向Line 索取照片

'''

"""

啟用伺服器基本樣板

"""
# 引用Web Server套件
from flask import Flask, request, abort
from confluent_kafka import Producer
import sys
import time
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
    MessageEvent, TextMessage, TextSendMessage,ImageMessage
)
import json

# 載入設定檔

secretFileContentJson=json.load(open("E:\line_chat_bot_tutorial-master\material/line_secret_key",'r',encoding="utf-8"))
server_url=secretFileContentJson.get("server_url")

def error_cb(err):
    print('Error: %s' % err)

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "E:\line_chat_bot_tutorial-master\material/images/" )

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

若收到圖片消息時，

先回覆用戶文字消息，並從Line上將照片拿回。

'''


# handler收到消息事件 而且是影片消息的話 做下面方法
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Message has Upload'+ ' ' + event.message.text))
    # 請line bot api 跟line 用消息id拿文字回來
    user_data = line_bot_api.get_profile(event.source.user_id)
    user_data = str(user_data)
    pos = user_data.find("userId")

    user_id = user_data[pos+10:-2].encode() # kafka只吃binary資料，建議encode()使文字轉binary
    content=event.message.text.encode() # 如果使用confluent kafka便不需encode()轉binary
    produce(user_id,content)
    print(content)
    print(user_id)
    # 存成檔案
    # with open('E:\line_chat_bot_tutorial-master\material/images/'+event.message.id+'.txt', 'w') as fd:
    #     for chunk in message_content.iter_content():
    #         fd.write(chunk)

# handler收到消息事件 而且是圖片消息的話 做下面方法
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Image has Upload'+ ' ' + event.message.id))
    # 請line bot api 跟line 用消息id拿圖片回來
    message_content = line_bot_api.get_message_content(event.message.id)
    # 存成檔案
    with open(r"E:\line_chat_bot_tutorial-master\material/images/"+ event.message.id+'.jpg', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

from linebot.models import VideoMessage

# handler收到消息事件 而且是影片消息的話 做下面方法
@handler.add(MessageEvent, message=VideoMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Video has Upload'+ ' ' + event.message.id))
    # 請line bot api 跟line 用消息id拿影音回來
    message_content = line_bot_api.get_message_content(event.message.id)

    # 存成檔案
    with open('E:\line_chat_bot_tutorial-master\material/images/'+event.message.id+'.mp4', 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)


# from linebot.models import VideoMessage

# #handler收到消息事件 而且是音訊消息的話 做下面方法
# @handler.add(MessageEvent, message=AudioMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text='Image has Upload'+ ' ' + event.message.id))
#     #請line bot api 跟line 用消息id拿音訊回來
#     message_content = line_bot_api.get_message_content(event.message.id)
#     #分析邏輯
#     #存成檔案
    
#     with open('../images/'+event.message.id+'.mp3', 'wb') as fd:
#         for chunk in message_content.iter_content():
#             fd.write(chunk)

# linebot資料丟kafka
def produce(user_id,content):
    # 步驟1. 設定要連線到Kafka集群的相關設定
    props = {
        # Kafka集群位置
        'bootstrap.servers': '10.120.26.15:9092',  # <-- 置換成要連接的Kafka集群
        'error_cb': error_cb  # 設定接收error訊息的callback函數
    }
    # 步驟2. 產生一個Kafka的Producer的實例
    producer = Producer(props)
    # 步驟3. 指定想要發佈訊息的topic名稱
    topicName = 'par12345'
    try:
        # produce(topic, [value], [key], [partition], [on_delivery], [timestamp], [headers])
        producer.produce(topicName, key= user_id, value= content)
        producer.flush()
        print('Send messages to Kafka')

    except Exception as e:
        print(e)
    # 步驟4. 確認所在Buffer的訊息都己經送出去給Kafka了
    producer.flush()

'''

啟動Server

'''
if __name__ == "__main__":
    app.run(host='0.0.0.0')


