#!/usr/bin/env python
# coding: utf-8

'''

當用戶輸入特定文字消息時，會啟用Flex Message功能。

此功能可讓開發者製作多樣化的版面消息，滿足多變商業需求。

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
secretFileContentJson=json.load(open("./line_secret_key",'r'))
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
Flex Message製作流程篇

使用 Flex Message Simulator 進行消息製作
https://developers.line.me/console/fx/

將json貼回下方準備好的框框

封裝成FlexMessage

放入消息回傳字典中

'''

'''

Flex Message 

Bubble的原稿Json

開發者以後可將Bubble類型的Flex消息Json，對此處進行更換。

'''

flexBubbleContainerJsonString ="""
{
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "text",
        "text": "NEWS DIGEST",
        "weight": "bold",
        "color": "#aaaaaa",
        "size": "sm"
      }
    ]
  },
  "hero": {
    "type": "image",
    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_4_news.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "horizontal",
    "spacing": "md",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "flex": 1,
        "contents": [
          {
            "type": "image",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/02_1_news_thumbnail_1.png",
            "aspectMode": "cover",
            "aspectRatio": "4:3",
            "size": "sm",
            "gravity": "bottom"
          },
          {
            "type": "image",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/02_1_news_thumbnail_2.png",
            "aspectMode": "cover",
            "aspectRatio": "4:3",
            "margin": "md",
            "size": "sm"
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "flex": 2,
        "contents": [
          {
            "type": "text",
            "text": "7 Things to Know for Today",
            "gravity": "top",
            "size": "xs",
            "flex": 1
          },
          {
            "type": "separator"
          },
          {
            "type": "text",
            "text": "Hay fever goes wild",
            "gravity": "center",
            "size": "xs",
            "flex": 2
          },
          {
            "type": "separator"
          },
          {
            "type": "text",
            "text": "LINE Pay Begins Barcode Payment Service",
            "gravity": "center",
            "size": "xs",
            "flex": 2
          },
          {
            "type": "separator"
          },
          {
            "type": "text",
            "text": "LINE Adds LINE Wallet",
            "gravity": "bottom",
            "size": "xs",
            "flex": 1
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "More",
          "uri": "https://linecorp.com"
        }
      }
    ]
  }
}"""

'''

將bubble類型的json 進行轉換變成 Python可理解之類型物件

將該物件封裝進 Flex Message中

'''

from linebot.models import(
    FlexSendMessage,BubbleContainer)

import json

bubbleContainer= BubbleContainer.new_from_json_dict(json.loads(flexBubbleContainerJsonString))
flexBubbleSendMessage =  FlexSendMessage(alt_text="hello", contents=bubbleContainer)

'''

設計一個Carousel Flex

'''

flexCarouselContainerJsonDict = """
{
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "Arm Chair, White",
            "wrap": true,
            "weight": "bold",
            "size": "xl"
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": "$49",
                "wrap": true,
                "weight": "bold",
                "size": "xl",
                "flex": 0
              },
              {
                "type": "text",
                "text": ".99",
                "wrap": true,
                "weight": "bold",
                "size": "sm",
                "flex": 0
              }
            ]
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "action": {
              "type": "uri",
              "label": "Add to Cart",
              "uri": "https://linecorp.com"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "Add to wishlist",
              "uri": "https://linecorp.com"
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_6_carousel.png"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "Metal Desk Lamp",
            "wrap": true,
            "weight": "bold",
            "size": "xl"
          },
          {
            "type": "box",
            "layout": "baseline",
            "flex": 1,
            "contents": [
              {
                "type": "text",
                "text": "$11",
                "wrap": true,
                "weight": "bold",
                "size": "xl",
                "flex": 0
              },
              {
                "type": "text",
                "text": ".99",
                "wrap": true,
                "weight": "bold",
                "size": "sm",
                "flex": 0
              }
            ]
          },
          {
            "type": "text",
            "text": "Temporarily out of stock",
            "wrap": true,
            "size": "xxs",
            "margin": "md",
            "color": "#ff5551",
            "flex": 0
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "flex": 2,
            "style": "primary",
            "color": "#aaaaaa",
            "action": {
              "type": "uri",
              "label": "Add to Cart",
              "uri": "https://linecorp.com"
            }
          },
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "Add to wish list",
              "uri": "https://linecorp.com"
            }
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "flex": 1,
            "gravity": "center",
            "action": {
              "type": "uri",
              "label": "See more",
              "uri": "https://linecorp.com"
            }
          }
        ]
      }
    }
  ]
}

"""

'''

將carousel類型的json 進行轉換變成 Python可理解之類型物件

將該物件封裝進 Flex Message中


'''

from linebot.models import(
    FlexSendMessage,CarouselContainer)

import json

carouselContent = CarouselContainer.new_from_json_dict(json.loads(flexCarouselContainerJsonDict))
flexCarouselSendMeesage =  FlexSendMessage(alt_text="hello", contents=carouselContent)

'''
設計一個字典

當用戶輸入 [::flex:]carousel ，回傳 旋轉類型的Flex消息

當用戶輸入 [::flex:]bubble ， 回傳 泡泡堆疊類型的Flex消息

'''
import json
template_message_dict = {
    "[::flex:]carousel": flexCarouselSendMeesage,
    "[::flex:]bubble" : flexBubbleSendMessage}

'''

用戶發送文字消息時，會按此進行消息處理

'''

# 用戶發出文字消息時， 按條件內容, 回傳合適消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        template_message_dict.get(event.message.text)
    )

'''

啟動Server

'''
if __name__ == "__main__":
    app.run(host='0.0.0.0')

