#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''

啟動伺服器基本樣版

設定業務功能
    當用戶關注時
        記錄個資，綁定菜單，回傳文字消息與圖片消息，介紹功能與使用方法
    當用戶點擊自定義菜單或輸入文字消息時
        傳送圖片消息或相應文字消息。
    當用戶點擊按鈕消息的時候
        會將用戶個資紀錄回檔案內，以供未來聯繫用

'''


# In[ ]:


"""

啟用伺服器基本樣板

"""

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

# 載入基礎設定檔
secretFileContentJson=json.load(open("./line_secret_key",'r',encoding="utf-8"))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/")

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


# In[ ]:


"""


當用戶關注Line@後，Line會發一個FollowEvent，

我們接受到之後，取得用戶個資，對用戶綁定自定義菜單，會回傳四個消息給用戶


"""


# In[ ]:


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
    preview_image_url='https://%s/images/005.jpg' %server_url)
]


# In[ ]:


'''

建立圖片消息素材

'''

# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    ImageSendMessage
)

# 圖片消息的基本建構特徵
image_message = ImageSendMessage(
    original_content_url='https://%s/images/preview1.png' % server_url,
    preview_image_url='https://%s/images/preview1.png' % server_url
)
image_message2 = ImageSendMessage(
    original_content_url='https://%s/images/preview.png' % server_url,
    preview_image_url='https://%s/images/preview.png' % server_url
)
image_message3 = ImageSendMessage(
    original_content_url='https://%s/images/preview3.png' % server_url,
    preview_image_url='https://%s/images/preview3.png' % server_url
)

image_message4 = ImageSendMessage(
    original_content_url='https://%s/images/preview4.png' % server_url,
    preview_image_url='https://%s/images/preview4.png' % server_url
)


# In[ ]:


'''
Button篇
    設定模板消息，指定其參數細節。

'''


#引入所需要的消息與模板消息
from linebot.models import (
    MessageEvent, TemplateSendMessage , PostbackEvent
)

#引入按鍵模板
from linebot.models.template import(
    ButtonsTemplate
)

# #引入模板消息的可用行為
# from linebot.models.template import(
#     PostbackTemplateAction,
#     MessageTemplateAction,
#     URITemplateAction,
#     DatetimePickerTemplateAction
# )


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
            "type": "postback",
            "label": "企業，查找商業結合方案",
            "text": "[::text:]尋找BD",
            "data": "Data1"
          },
          {
            "type": "postback",
            "label": "開發者，尋求教學",
            "text": "[::text:]求助專家",
            "data": "Data2"
          }
        ],
)
)


# In[ ]:


'''
將素材消息做成一本字典，當用戶發出相應消息時，可從此進行查找動作。
'''
template_message_dict = {
    "[::text:]教學訊息": reply_message_list,
    "[::text:]傳統交易":image_message,
    "[::text:]第三方公證人":image_message2,
    "[::text:]多位公證人":image_message3,
    "[::text:]多組織多位公證人":image_message4,
    "[::text:]more":buttons_template_message
}


# In[ ]:


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
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
        
     # 將用戶資訊存在檔案內
    with open("./users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile),sort_keys=True))
        myfile.write('\r\n')
        
        
    # 將菜單綁定在用戶身上
    linkRichMenuId=secretFileContentJson.get("rich_menu_id")
    linkResult=line_bot_api.link_rich_menu_to_user(event.source.user_id, linkRichMenuId)
    
    # 回覆文字消息與圖片消息
    line_bot_api.reply_message(
        event.reply_token,
        reply_message_list
    )


# In[ ]:


'''

當用戶發出文字消息時，判斷文字內容是否包含[::text:]，
    若有，則從template_message_dict 內找出相關訊息
    若無，則回傳預設訊息。

'''

# 用戶發出文字消息時， 按條件內容, 回傳文字消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    if(event.message.text.find('::text:')!= -1):
        line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text))
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="請點擊菜單上圖面，或輸入[::text:]more，取得更多幫助"))


# In[ ]:


#用戶點擊button後，觸發postback event，對其回傳做相對應處理
@handler.add(PostbackEvent)
def handle_post_message(event):
    user_profile = line_bot_api.get_profile(event.source.user_id)
    if (event.postback.data.find('Data1')== 0):
        with open("./user_profile_business.txt", "a") as myfile:
            myfile.write(json.dumps(vars(user_profile),sort_keys=True))
            myfile.write('\r\n')
            line_bot_api.reply_message(
            event.reply_token,
                TextMessage(
                    text='請稍待，會有專人與您聯繫'
                )
            )
    elif (event.postback.data.find('Data2') == 0):
        with open("./user_profile_tutorial.txt", "a") as myfile:
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


# In[ ]:


'''

執行此句，啟動Server，觀察後，按左上方塊，停用Server

'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')


# In[ ]:




