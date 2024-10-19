import mysql.connector
from mysql.connector import Error
import pandas as pd

# 配置 MySQL 連接參數
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234567890',
    'database': 'Pchome'
}

# 假設已經有一個從爬蟲中抓取到的商品列表 dataframe
def insert_into_db(data):
    try:
        connection = mysql.connector.connect(**mysql_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # 創建表
            create_table_query = """
            CREATE TABLE IF NOT EXISTS pchome (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                link VARCHAR(255),
                price DECIMAL(10, 2)
            )
            """
            cursor.execute(create_table_query)

            # 插入數據
            insert_query = "INSERT INTO pchome (name, link, price) VALUES (%s, %s, %s)"
            for index, row in data.iterrows():
                cursor.execute(insert_query, (row['品名'], row['商品連結'], row['價格']))

            connection.commit()
            print("數據插入成功")

    except Error as e:
        print(f"錯誤: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 使用爬蟲抓取到的資料（假設以 Pandas DataFrame 格式存儲）
data = pd.read_csv('./price_taker/PChome.csv')
insert_into_db(data)