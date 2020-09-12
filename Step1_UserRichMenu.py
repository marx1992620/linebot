#!/usr/bin/env python
# coding: utf-8

'''

用戶菜單功能介紹
用戶能透過點擊菜單，進行我方設計之業務功能。
    
流程
    準備菜單的圖面設定檔
    讀取安全設定檔上的參數
    將菜單設定檔傳給Line
    對Line上傳菜單照片
    檢視現有的菜單
    將菜單與用戶做綁定
    將菜單與用戶解除綁定
    刪除菜單

'''

'''
菜單設定檔

    設定圖面大小、按鍵名與功能
    
'''

menuRawData="""
{
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": true,
  "name": "區塊鏈自定義菜單",
  "chatBarText": "查看更多資訊",
  "areas": [
    {
      "bounds": {
        "x": 5,
        "y": 0,
        "width": 824,
        "height": 850
      },
      "action": {
        "type": "message",
        "text": "[::text:]傳統交易"
      }
    },
    {
      "bounds": {
        "x": 0,
        "y": 850,
        "width": 825,
        "height": 818
      },
      "action": {
        "type": "message",
        "text": "[::text:]第三方公證人"
      }
    },
    {
      "bounds": {
        "x": 829,
        "y": 5,
        "width": 871,
        "height": 849
      },
      "action": {
        "type": "message",
        "text": "[::text:]多位公證人"
      }
    },
    {
      "bounds": {
        "x": 825,
        "y": 854,
        "width": 875,
        "height": 814
      },
      "action": {
        "type": "message",
        "text": "[::text:]多組織多位公證人"
      }
    },
    {
      "bounds": {
        "x": 1700,
        "y": 0,
        "width": 800,
        "height": 858
      },
      "action": {
        "type": "message",
        "text": "[::text:]教學訊息"
      }
    },
    {
      "bounds": {
        "x": 1700,
        "y": 858,
        "width": 800,
        "height": 810
      },
      "action": {
        "type": "message",
        "text": "[::text:]more"
      }
    }
  ]
}
"""

'''

讀取安全檔案內的字串，以供後續程式碼調用

'''
import json
secretFileContentJson=json.load(open("E:\line_chat_bot_tutorial-master\material\line_secret_key",'r',encoding="utf-8"))

print(secretFileContentJson.get("channel_access_token"))
print(secretFileContentJson.get("secret_key"))
print(secretFileContentJson.get("self_user_id"))


'''

用channel_access_token創建line_bot_api，預備用來跟Line進行溝通

'''

from linebot import (
    LineBotApi, WebhookHandler
)
# 用channel access token 建一個line bot api
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))

'''

載入前面的圖文選單設定，

並要求line_bot_api將圖文選單上傳至Line
    
'''

from linebot.models import RichMenu
import requests
#讀取圖文選單設定檔
menuJson=json.loads(menuRawData)
#請line bot api 把圖文選單設定檔 上傳給line line回傳圖文選單id給我們
#存到變數以及line secret key檔案內
lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(menuJson))
print(lineRichMenuId)

'''

將先前準備的菜單照片，以Post消息寄發給Line

    載入照片
    要求line_bot_api，將圖片傳到先前的圖文選單id

'''

#讀取圖片
uploadImageFile=open("E:\line_chat_bot_tutorial-master\material\images/blockchain_demo.jpg",'rb')
#請line bot api上傳圖片到指定id位置
setImageResponse = line_bot_api.set_rich_menu_image(lineRichMenuId,'image/jpeg',uploadImageFile)

print(setImageResponse)

'''

將選單綁定到特定用戶身上
    取出上面得到的菜單Id及用戶id
    要求line_bot_api告知Line，將用戶與圖文選單做綁定

'''

# https://api.line.me/v2/bot/user/{userId}/richmenu/{richMenuId}

#請line bot api綁定圖文選單至指定的用戶身上
#link rich menu to user（user_id,圖文選單id）
linkResult=line_bot_api.link_rich_menu_to_user(secretFileContentJson["self_user_id"], lineRichMenuId)

print(linkResult)

'''

檢視用戶目前所綁定的菜單
    取出用戶id，並告知line_bot_api，
    line_bot_api傳回用戶所綁定的菜單
    印出

'''

#  https://api.line.me/v2/bot/user/{userId}/richmenu
#請line bot api 調閱指定用戶目前綁定的圖文選單
#get rich menu id of user (用戶id) 

rich_menu_id = line_bot_api.get_rich_menu_id_of_user(secretFileContentJson["self_user_id"])
print(rich_menu_id)

'''

解除選單與特定用戶的綁定
    取出用戶id，並告知line_bot_api，
    line_bot_api解除用戶所綁定的菜單
'''
#請line bot api
#unlink rich menu from user(user id)
lineUnregisterUserMenuResponse=line_bot_api.unlink_rich_menu_from_user(secretFileContentJson["self_user_id"])
print(lineUnregisterUserMenuResponse)

'''

檢視帳號內，有哪些選單
    要求line_bot_api，向line查詢我方的圖文選單列表
    打印

'''

rich_menu_list = line_bot_api.get_rich_menu_list()
for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)

