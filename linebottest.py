# 載入需要的模組
from flask import Flask, request, abort, session
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FileMessage
from linebot import LineBotApi, WebhookHandler
import pymongo
import json
import openpyxl
import os
import mouser
import time
from flask_session import Session

client = pymongo.MongoClient("mongodb+srv://root:12root28@cluster0.r39qy0s.mongodb.net/?retryWrites=true&w=majority")

app = Flask(__name__)
app.secret_key="jasonkey"
# LINE 聊天機器人的基本資料


# 配置 Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # 使用文件系统存储会话数据
Session(app)


line_bot_api = LineBotApi('xNFz7l4M6QzcPwGqP83/0WZc+Luri3gPVUS73Rt6SpI8O6gpfOhLelI6X/4F3crEpvRIVxu4QxIp6JPTUVbkTrEg5eezB3yMYPpas/3uhJqyYPd1d4JVhCfvt0neul8PUPjqv9dXw7ZdR1lWD4KcfAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ca02a3700ac05d6d9565e0a365498c95')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    if "handle_mode" not in session:
        session["handle_mode"] = 0
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    text = event.message.text
    if text=="聯繫客服":
        session["handle_mode"]=1
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="已切換至客服模式")
            )
    elif text=="詢價模式":
        session["handle_mode"]=0
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="已切換至詢價模式")
            )
    
    else:
        if session["handle_mode"]==0:
            itemlist = text.splitlines()
            #控制查詢的筆數一次不能超過20筆!
            if len(itemlist)>20:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="查詢上限為20筆")
                )   
            db = client["pteam"]
            collection = db['linestock']
            sendmsg="價格資訊\n\n"

            for item in itemlist:
                results = collection.find({"pn": item})
                if results.count() !=0:
                    for result in results:
                        pn = result['pn']
                        mfr = result['mfr']
                        stock = result['qty']
                        sendmsg += "產品編號:"+str(pn)+"\n製造商:"+str(mfr)+"\n庫存數量:"+str(stock)+"\n"
                        
                        price_list = json.loads(result['price'])
                        for price in price_list:
                            num = price['goods_num']
                            p = price['goods_price']
                            sendmsg += "數量:"+str(num)+"價格:"+str(p)+"\n"
                        sendmsg+="\n"
                else:
                    sendmsg+="未找到產品編號"+str(item)+"\n"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=sendmsg)
            )
                


@handler.add(MessageEvent, message=FileMessage)
def handle_mouser_file(event):
    if event.message.type == "file":
        message_content = line_bot_api.get_message_content(event.message.id)
        temp_file_path = f"uploads/temp_{event.message.id}.xlsx"  # 暫存檔案的路徑
        with open(temp_file_path, "wb") as f:
            for chunk in message_content.iter_content():
                f.write(chunk)

        # 讀取Excel檔案內容
        wb = openpyxl.load_workbook(temp_file_path)
        ws = wb['工作表1']
        items = []
        qtys=[]
        for row in ws.iter_rows(min_row=2, values_only=True):  # 從第二行開始讀取
            if row[0]:  # 如果該行的第一個欄位不為空
                items.append(row[0])
                qtys.append(row[1])


        output_text = ""
        qtyposition=0
        # 在新的 Excel 檔案中寫入資料
        for item in items:
            #qty對應的位子
            qtyvalue=qtys[qtyposition]
            print(item)
            result = mouser.getdata(item)
            if result != {"nodata"} and result:
                for part_number, part_info in result.items():
                    price_breaks = part_info['PriceBreaks']
                    breakprice=mouser.getbreak(price_breaks,qtyvalue)
                    output_text += f"{part_info['Availability']}/{part_info['Manufacturer']}/{part_info['ManufacturerPartNumber']}/{breakprice[0]}/{breakprice[1]}\n"
            else:
                output_text += f"{item}/NA\n"
            qtyposition+=1
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=output_text))

        os.remove(temp_file_path)  # 刪除上傳的暫存檔案s


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)