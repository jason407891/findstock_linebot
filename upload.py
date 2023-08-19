import pandas as pd
import pymongo


client=pymongo.MongoClient("mongodb+srv://root:12root28@cluster0.r39qy0s.mongodb.net/?retryWrites=true&w=majority")
db=client['pteam']
collection=db['stock']
df=pd.read_excel(r"C:\Users\MENGTA LIN\Downloads\stock1.xlsx")
data=df.to_dict('records')
collection.insert_many(data)