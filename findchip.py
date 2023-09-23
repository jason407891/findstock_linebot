import requests
from bs4 import BeautifulSoup
import re


pn="gvrsvfv"
url = "https://www.findchips.com/search/"+str(pn)
response = requests.get(url)

def findchips(response,supplier_code,name):
    price_results=[]
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            rows = soup.find(id="list"+str(supplier_code)).find_all(class_="row")
            for row in rows:
                price_result={}
                price_result["supplier_code"]=supplier_code
                #pn
                pn =row.find(class_="onclick")
                pn=pn.text.strip()
                if pn!=name:
                    break
                price_result["pn"]=pn
                #mfr
                mfr=row.find(class_="td-mfg")
                mfr=mfr.text.strip()
                price_result["mfr"]=mfr
                #stock
                stock=row.find(class_="td-stock")
                stock=stock.text.strip()
                match = re.search(r'\d+\.\d+|\d+', stock)
                if match:
                    found_number = match.group()
                    if int(found_number)==0:
                        break
                    price_result["stock"]=stock
                #price_break
                prices=row.find_all(class_="price-list")
                price_breaks=[] # []
                for price in prices:
                    labels = price.find_all(class_="label")
                    values = price.find_all(class_="value")
                    for i in range(len(labels)):
                        price_info = {
                            "goods_num":labels[i].text.strip(),
                            "goods_price":values[i].text.strip()
                        }
                        price_breaks.append(price_info)
                price_result["price"] = price_breaks
                price_results.append(price_result)                  
            return(price_results)
        except:
            return([])
    else:
        return({"results":"SOMETHING ERROR"})


"""
DGKEY 1588
CHIPONE 4327862
AVNET 313766970
ELEMENT 2953375
MOUSER 1577
TME 150002559
"""

#findchips(response,1588,pn)
#print(findchips(response,4327862,pn))
#print(findchips(response,2167609,pn))