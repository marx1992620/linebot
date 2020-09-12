#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''

展示 

對用戶進行消息推播

推播消息為 Line火紅的照片地圖功能

當用戶點擊照片地圖時，會跳轉到Line的特殊功能，撥號與定位

'''


# In[2]:


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


# In[3]:


'''

新增照片地圖素材

並融合先前所教的 進階撥號與地理定位功能

'''

from linebot.models import ImagemapSendMessage

from linebot.models import (
    ImagemapArea, BaseSize, URIImagemapAction, MessageImagemapAction
)

imagemap_message = ImagemapSendMessage(
    base_url='https://%s/images/blockchain'%server_url,
    alt_text='區塊鏈照片地圖',
    base_size=BaseSize(height=1040, width=1040),
    actions=[
        URIImagemapAction(
            link_uri='line://calls',
            area=ImagemapArea(
                x=0, y=0, width=520, height=1040
            )
        ),
        URIImagemapAction(
            link_uri='line://nv/location',
            area=ImagemapArea(
                x=520, y=0, width=520, height=1040
            )
        )
    ]
)    


# In[4]:


'''

設定一個Server入口，

當有人訪問此入口，會對用戶進行消息推播

將上面設計的imagemap消息，推播給用戶

'''
@app.route("/pushMessage", methods=['GET'])
def push_message():
    #取個資
    json_object_strings = open("./users.txt",'r')
    json_array = []
    user_id_array = []
    
    for json_object_string in json_object_strings:
        json_object = json.loads(json_object_string)
        json_array.append(json_object)
    
    for user_record in json_array:
        user_id_array.append(user_record.get("user_id"))
    
    #廣播
    line_bot_api.multicast(
        user_id_array,
        imagemap_message
    )

    return 'OK'


# In[5]:


'''

執行此句，啟動Server，觀察後，按左上方塊，停用Server

'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')

