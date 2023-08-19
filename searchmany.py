import pymongo
import json

pn_list=["39-00-0038","39-00-0040"]

# 建立与MongoDB的连接

def returndata(pn_list):
    client = pymongo.MongoClient("mongodb+srv://root:12root28@cluster0.r39qy0s.mongodb.net/?retryWrites=true&w=majority")
    db = client["pteam"]
    collection=db['linestock']

    for part in pn_list:
        result = collection.find({"pn": part})

        for item in result:
            print("產品編號:"+item['pn'])
            print("製造商:"+item['mfr'])
            print("庫存數量:"+str(item['qty']))
            price_list=json.loads(item['price'])
            for price in price_list:
                print("數量:"+price['goods_num'],end=" ")
                print("價格:"+price['goods_price'])



            #print(item['date'])
            #print(item['Brand'])
