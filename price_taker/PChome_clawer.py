import argparse
import requests
import json
import pandas as pd
import time

def crawl_pchome(keyword):
    # URL1
    url = f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={keyword}&page=1&sort=sale/dc'
    prodnum = 0
    products_list = []

    # 爬取多頁數據
    for i in range(1, 10):  # 爬9頁
        #URL2
        url = f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={keyword}&page={i}&sort=sale/dc'
        
        list_req = requests.get(url)
        getdata = json.loads(list_req.content)

        for products in getdata['prods']:
            prodnum += 1
            products_list.append({
                '編號': prodnum, 
                '品名': products['name'],
                '商品連結': f'https://24h.pchome.com.tw/prod/{products["Id"]}', 
                '價格': products['price']
            })

        time.sleep(3)  # 睡覺

    # 轉成 DataFrame
    products_df = pd.DataFrame(products_list)

    # 儲存為 CSV
    try:
        products_df.to_csv('./price_taker/PChome.csv', encoding='utf-8-sig', index=False, header=True)
        print("CSV 檔案已建立")
    except Exception as e:
        print(f"儲存 CSV 文件時出現錯誤：{e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="PChome Crawler")
    parser.add_argument('keyword', type=str, help='要搜尋的關鍵字')
    args = parser.parse_args()
    crawl_pchome(args.keyword)
