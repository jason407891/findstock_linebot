import requests
import openpyxl
import json
import time


def getbreak(price_breaks_data,qty):
    goods_num = 1
    if price_breaks_data:
        price=price_breaks_data[0]['Price']
        for price_break in price_breaks_data:
            if qty <= price_break['Quantity']:
                break
            goods_num = price_break['Quantity']
            price=price_break['Price']
        return [goods_num,price]
    else:
        return["NA","NA"]

def getdata(pn):
    # Swagger API 文件中的路徑和參數
    url = 'https://api.mouser.com/api/v1/search/partnumber?apiKey=8b1390e5-5fbc-4169-9c88-ac16c0599220'
    api_key_order = '19c5e8f6-6454-4387-bbbd-fbfa3b4d1434'

    # 設定請求的 headers，如果需要 API 金鑰
    headers = {
        'Authorization': f'Bearer {api_key_order}',
        'Content-Type': 'application/json'
    }

    # 設定請求的資料，這裡使用 JSON 格式
    data = {
        "SearchByPartRequest": {
            "mouserPartNumber": pn,
            "partSearchOptions": "string"
        }
    }

    # 發送 POST 請求
    response = requests.post(url,headers=headers,json=data)

    # 解析回應內容
    response_content = response.json()

    # 檢查回應是否為空
    if response.status_code == 200:
        # 解析回應內容
        response_content = response.json()

        # 檢查回應是否包含 SearchResults
        if response_content and 'SearchResults' in response_content:
            # 取得 Parts
            parts = response_content['SearchResults']['Parts']
        
        # 逐個處理每個部分
            for part in parts:
                availability = part.get('Availability')
                manufacturer = part.get('Manufacturer')
                manufacturer_part_number = part.get('ManufacturerPartNumber')
                price_breaks = part.get('PriceBreaks', [])
                
                all_parts_info = {}
                # 顯示資訊
                part_info = {
                    'Availability': availability,
                    'Manufacturer': manufacturer,
                    'ManufacturerPartNumber': manufacturer_part_number,
                    'PriceBreaks': price_breaks
                }
                
                all_parts_info[manufacturer_part_number] = part_info
                
                return all_parts_info
        else:
            return {"nodata"}
    else:
        return {"nodata"}




