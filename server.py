"""**************************************************************
*   Desciribe:                                                  *
*       The line-bot server.                                    *
*                                                               *
*   Date    : 2023/07/29                                        *
*   Author  : YongHong, Liu                                     *
*                                                               *
**************************************************************"""
#======import part=================================================================================
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from dotenv import load_dotenv
from db.DBAccess import DataBase
import os


#==================================================================================================
#======variable declare============================================================================

#==================================================================================================
#======function declare============================================================================
class linebotServer():
    def __init__(self):
        load_dotenv()
        self.server = Flask(__name__)

        self.linebotApi = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
        self.handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

        #Add EndPoint; same as @self.server.route("/callback", methods=['POST'])
        self.server.add_url_rule('/callback', 'callback', self.callback, methods=['POST']) 

        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
           self.processMessage(event)
    #-----------------------------------------------------------------------------
    
    def callback(self):
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        self.server.logger.info("Request body: " + body)
        try:
            self.handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        return 'OK'

    #-----------------------------------------------------------------------------
    def start(self, host, port):
        self.server.run(host, port)

    #-----------------------------------------------------------------------------
    def processMessage(self, event):
        print(event)
        print("==========================================================================================")

        message=""
        try:
            db = DataBase()
            command = event.message.text.split(' ')
            ret=""
            
            if command[0] == "註冊":
                if len(command) == 3 and command[2]== "Iam管理者" :
                    ret = db.addPermissions(event.source.user_id, "管理員")
                elif len(command) == 2:
                    ret = db.addPermissions(event.source.user_id,"一般")
                else:
                    ret="指令錯誤，請檢查!"
                message = TextSendMessage(text = ret)
            elif command[0] == "權限":
                tempstr="查無資料! 請先註冊"
                
                ret = db.queryPermissions(event.source.user_id)
                if ret is not None:
                    tempstr= "名稱: %s, 權限: %s".format(ret[0], ret[1])        
                else:
                    message = TextSendMessage(text = tempstr)     
            else:
                # Error command said same text
                message = TextSendMessage(text=event.message.text)
                

            self.linebotApi.reply_message(event.reply_token, message)     
        except Exception as e:
                    print(e)


        #------reply message-------
        # message = TextSendMessage(text=event.message.text)
        # linebotApi.reply_message(event.reply_token, message) 
        #--------------------------
#==================================================================================================
#==================================================================================================