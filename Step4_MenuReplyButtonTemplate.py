#!/usr/bin/env python
# coding: utf-8

'''

當用戶輸入特定文字消息時，會回傳按鍵模板消息。

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

Button篇 
設定模板消息，指定其參數細節

'''

#引入所需要的消息與模板消息
from linebot.models import (MessageEvent, TemplateSendMessage , PostbackEvent)

#引入按鍵模板
from linebot.models.template import(ButtonsTemplate)

'''
alt_text: Line簡覽視窗所出現的說明文字
template: 所使用的模板
ButtonsTemplate: 按鍵模板
    thumbnail_image_url: 展示圖片
    title: 標題
    text: 說明文字
    actions: 模板行為所使用的行為
    data: 觸發postback後用戶回傳值，可以對其做商業邏輯處理

'''
buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='更多幫助',
        text='請點擊下方按鈕獲得更多幫助',
        actions=[
             {
        "type": "uri",
        "label": "用URI打電話",
        "uri": "tel://0934138995"
      },
      {
        "type": "uri",
        "label": "用URI拍張照",
        "uri": "https://line.me/R/nv/camera/"
      },
      {
        "type": "uri",
        "label": "用URI傳送地理位置",
        "uri": "https://line.me/R/nv/location/"
      }
#           {
#             "type": "postback",
#             "label": "企業，查找商業結合方案",
#             "text": "[::text:]尋找BD",
#             "data": "field1=value1&field2=value2&tag=高管"
#           },
#           {
#             "type": "postback",
#             "label": "開發者，尋求教學",
#             "text": "[::text:]求助專家",
#             "data": "Data2"
#           }
        ],
)
)
#URI功能
#https://developers.line.biz/en/docs/messaging-api/using-line-url-scheme/#if-the-user-hasn-t-installed-line

'''

設計一個字典

'''
template_message_dict = {
    "[::text:]more":buttons_template_message
}

# 用戶發出文字消息時， 按條件內容, 回傳照片地圖
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text)
    )

#用戶點擊button後，觸發postback event，對其回傳做相對應處理
#從點擊行為貼標用戶
@handler.add(PostbackEvent)
def handle_post_message(event):
    user_profile = line_bot_api.get_profile(event.source.user_id)
    if (event.postback.data.find('Data1')== 0):
        with open("../user_profile_business.txt", "a") as myfile:
            myfile.write(json.dumps(vars(user_profile),sort_keys=True))
            myfile.write('\r\n')
            line_bot_api.reply_message(
            event.reply_token,
                TextMessage(
                    text='請稍待，會有專人與您聯繫'
                )
            )
    elif (event.postback.data.find('Data2') == 0):
        with open("../user_profile_tutorial.txt", "a") as myfile:
            myfile.write(json.dumps(vars(user_profile),sort_keys=True))
            myfile.write('\r\n')
            line_bot_api.reply_message(
            event.reply_token,
                TextMessage(
                    text='請稍待，我們會派專家與您聯繫'
                )
            )
    else:
        pass

'''

啟動Server

'''
if __name__ == "__main__":
    app.run(host='0.0.0.0')




