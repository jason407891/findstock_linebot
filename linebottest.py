# 載入需要的模組
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot import LineBotApi, WebhookHandler
import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://root:12root28@cluster0.r39qy0s.mongodb.net/?retryWrites=true&w=majority")

app = Flask(__name__)

# LINE 聊天機器人的基本資料

line_bot_api = LineBotApi('xNFz7l4M6QzcPwGqP83/0WZc+Luri3gPVUS73Rt6SpI8O6gpfOhLelI6X/4F3crEpvRIVxu4QxIp6JPTUVbkTrEg5eezB3yMYPpas/3uhJqyYPd1d4JVhCfvt0neul8PUPjqv9dXw7ZdR1lWD4KcfAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ca02a3700ac05d6d9565e0a365498c95')


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def quote(event):
    if event.source.user_id != "U22283dfd5892369dfc699645887e3407":
        text = event.message.text
        app.logger.info("This is an info message")
        if text:
            itemlist = list(text)
            db = client["pteam"]
            collection = db['linestock']
            app.logger.info("This is an info messagessssssss")
            for item in itemlist:
                sendmsg="價格資訊\n"
                results = collection.find({"pn": item})
                for result in results:
                    pn=result['pn']
                    mfr=result['mfr']
                    stock=result['qty']
                    sendmsg += f"產品編號:{pn}\n製造商:{mfr}\n庫存數量:{stock}\n"
                    price_list = json.loads(result['price'])
                    for price in price_list:
                        num = price['goods_num']
                        p = price['goods_price']
                        sendmsg += f"數量:{num} 價格:{p}"

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)