#!/usr/bin/env python
# coding: utf-8

"""

當用戶關注Line@後，Line會發一個FollowEvent，
我們接受到之後，取得用戶個資，對用戶綁定自定義菜單，會回傳四個消息給用戶

"""

"""

啟用伺服器基本樣板

"""
# step1 引用套件

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json

# step2 應用入口準備

# 載入基礎設定檔
secretFileContentJson=json.load(open("E:\line_chat_bot_tutorial-master\material\line_secret_key",'r',encoding="utf-8"))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/")

# 人員準備 收發小妹
# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
# 人員準備 總機
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# 公司大門準備
# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
# 把消息的內容及簽章拿出來 交給handler做處理 驗證 交給後面的業務方法
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

製作文字與圖片的教學訊息

'''
# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

# 消息清單
reply_message_list = [
    TextSendMessage(text="關注區塊鏈技術，掌握市場脈動。"),
    
    TextSendMessage(text="人類所以充滿驚奇，在於人體那一精密又不可探究的系統。佈滿神經元的大腦，而後延展遍歷人體。\n\n區塊鏈就好比是人體那驚奇的神經系統，社會是我們的人身，在全身佈滿了神經後，造就了不可思量的奧妙生命。\n\n點選菜單，了解區塊鏈前世今生，以文字輸入 more，得到更多資訊。"),
    
    ImageSendMessage(original_content_url='https://%s/images/003.jpeg' %server_url ,
    
    preview_image_url='https://%s/images/001.jpg' %server_url),
    
    ImageSendMessage(original_content_url='https://%s/images/004.png' %server_url,
    
    preview_image_url='https://%s/images/005.jpg' %server_url)]

'''

撰寫用戶關注時，我們要處理的商業邏輯

1. 取得用戶個資，並存回伺服器
2. 把先前製作好的自定義菜單，與用戶做綁定
3. 回應用戶，歡迎用的文字消息與圖片消息

'''

# 載入Follow事件
from linebot.models.events import (
    FollowEvent
)

# 載入requests套件
import requests

# 告知handler，如果收到FollowEvent，則做下面的方法處理
# handler 收到關注事件時 做下面方法
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    
    # 取出消息內User的資料
    # get profile 取得用戶個資
    user_profile = line_bot_api.get_profile(event.source.user_id)
        
    # 將用戶資訊存在檔案內
    # save file by python
    with open("./users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile),sort_keys=True))
        myfile.write('\r\n')
        
        
    # 將菜單綁定在用戶身上
    linkRichMenuId=secretFileContentJson.get("rich_menu_id")
    linkResult=line_bot_api.link_rich_menu_to_user(event.source.user_id, linkRichMenuId)
    
    # 回覆文字消息與圖片消息
    # 請line bot api回復用戶
    line_bot_api.reply_message(
        event.reply_token,
        reply_message_list
    )

'''
當用戶封鎖我們
取他個資 存到unfollow_user.txt檔案內
告知handler收到unfollowEvent 
請line bot api取個資 存到指定檔案內
'''
from linebot.models import(
UnfollowEvent
)
# 告知handler收到unfollow時
@handler.add(UnfollowEvent)
def handle_unfollow_event(event):
    # 取出消息內User的資料
    # get profile 取得用戶個資
    user_profile = line_bot_api.get_profile(event.source.user_id)
    
    # 將用戶資訊存在檔案內
    # save file by python
    with open("E:\line_chat_bot_tutorial-master\material/users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile),sort_keys=True))
        myfile.write('\r\n')

'''

執行此句，啟動Server，觀察後，按左上方塊，停用Server

'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')

