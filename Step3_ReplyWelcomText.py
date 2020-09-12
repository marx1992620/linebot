#!/usr/bin/env python
# coding: utf-8

"""

當用戶想要重新觀看歡迎訊息時，可輸入特定文字，Server會重新寄發歡迎訊息

當用戶發送指定文字消息時，會發送相應的圖片消息給用戶

"""

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
secretFileContentJson=json.load(open("E:\line_chat_bot_tutorial-master\material/line_secret_key",'r',encoding="utf-8"))
server_url=secretFileContentJson.get("server_url")

# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "E:\line_chat_bot_tutorial-master\material/images/")

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

製作文字與圖片發送消息

'''

# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage)

# 設定消息素材
text_reply_message1 = TextSendMessage(text="關注區塊鏈技術，掌握市場脈動。")
text_reply_message2 = TextSendMessage(text="人類所以充滿驚奇，在於人體那一精密又不可探究的系統。佈滿神經元的大腦，而後延展遍歷人體。\n\n區塊鏈就好比是人體那驚奇的神經系統，社會是我們的人身，在全身佈滿了神經後，造就了不可思量的奧妙生命。\n\n點選菜單，了解區塊鏈前世今生，以文字輸入 more，得到更多資訊。")
image_reply_message1 = ImageSendMessage(
                                        original_content_url='https://%s/images/003.jpeg' %server_url ,
                                        preview_image_url='https://%s/images/001.jpg' %server_url)
image_reply_message2 = ImageSendMessage(
                                        original_content_url='https://%s/images/004.png' %server_url,
                                        preview_image_url='https://%s/images/005.jpg' %server_url)


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

'''

設計一個字典
    當用戶輸入相應文字消息時，系統會從此挑揀消息

'''

# 根據自定義菜單四張故事線的圖，設定相對應image
template_message_dict = {
    "[::text:]傳統交易":image_message,
    "[::text:]第三方公證人":image_message2,
    "[::text:]多位公證人":image_message3,
    "[::text:]多組織多位公證人":image_message4,
    "[::text:]教學訊息":[text_reply_message1,text_reply_message2,image_reply_message1,image_reply_message2]
}

'''

當用戶發出文字消息時，判斷文字內容是否包含[::text:]，
    若有，則從template_message_dict 內找出相關訊息
    若無，則回傳預設訊息。

'''

# 用戶發出文字消息時， 按條件內容, 回傳文字消息
# 當用戶收到訊息事件 且訊息為文字訊息 執行下面方法
@handler.add(MessageEvent, message=TextMessage)
#message={Textmessage,Videomessage,Audiomessage,Locationmessage定位,Stickermessage貼圖}
def handle_message(event):
    #未來可以放文字分析程式碼
    #當用戶內容有::text:時 會去找字典的消息做回覆
    #::text:為規則型符號，為了區隔規則式回復或AI式回復
    if(event.message.text.find('::text:')!= -1):
        line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text)
        )
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="請點擊菜單上圖面，或輸入[::text:]more，取得更多幫助")
        )

'''

執行此句，啟動Server，觀察後，按左上方塊，停用Server

'''

if __name__ == "__main__":
    app.run(host='0.0.0.0')


