from findchip import findchips,findchips_qty,findchips_desqty
import requests
from bs4 import BeautifulSoup

pn="PAP-03V-S"
url = "https://www.findchips.com/search/"+str(pn)
response = requests.get(url)


"""
DGKEY 1588 DES
CHIPONE 4327862
AVNET 313766970
ELEMENT 2953375
MOUSER 1577
TME 150002559
ARROW 1538
VERICAL 2167609
"""

#print(findchips(response,1588,pn))
#print(findchips_qty(response,4327862,pn,300))
inputtext="PAP-02V-S 100"
split_data = inputtext.split(" ")  # 使用空格分割字符串
if len(split_data) >= 2:
    pn = split_data[0]  # 第0个元素是产品编号
    qty = split_data[1]  # 第1个元素是数量
    print("產品:", pn)
    print("數量:", qty)
else:
    print("格式不正確")
