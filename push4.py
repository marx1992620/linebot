#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
主動推播四種方式

創建line_bot_api
1.把消息交給line
'''

from linebot import LineBotApi
#只有linebotapi可以跟line互動
import json
secretFileContentJson=json.load(open("../line_secret_key",'r',encoding="utf-8"))



# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))



# In[ ]:


'''

一對一回復

'''

from linebot.models import TextSendMessage
line_bot_api.push_message("Uc050e87fc6f7a09d6c9b00b977930fc0",TextSendMessage(text="一對一推播"))
line_bot_api.push_message("Uc050e87fc6f7a09d6c9b00b977930fc0",TextSendMessage(text="一對一推播"))
# line_bot_api.push_message(user_id,TextSendMessage(text="收到消息班代請喝飲料3"))


# In[ ]:


'''

全部回復

'''

line_bot_api.broadcast(TextSendMessage(text="全部推播"))


# In[ ]:


'''

line提供的分眾推播
line_bot_api.narrowcast()

'''
line_bot_api.narrowcast(TextSendMessage(text="全部推播"))


# In[ ]:


'''

自定義的分眾推播

'''

line_bot_api.multicast([user_id1,user_id2],TextSendMessage(text="分眾推播"))

