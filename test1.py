from findchip import findchips
import requests
from bs4 import BeautifulSoup

pn="55100-0680"
url = "https://www.findchips.com/search/"+str(pn)
response = requests.get(url)


"""
DGKEY 1588
CHIPONE 4327862
AVNET 313766970
ELEMENT 2953375
MOUSER 1577
TME 150002559
ARROW 1538
VERICAL 2167609
"""

#print(findchips(response,1588,pn))
#print(findchips(response,2167609,pn))
print(requests.__version__)

