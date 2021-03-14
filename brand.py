import pymongo 
from pymongo import MongoClient
import csv
import pymysql
import Get_Mongo
# import charts

cluster = MongoClient('mongodb+srv://crawler:!QAZ2wsx@cluster0.k1oua.mongodb.net/wear?retryWrites=true&w=majority')
db = cluster['wear']
collection = db['Mondel_M']
results = collection.find({'Mondel_Rank': '98'})
feature = [[result["Mondel_ID"].split('/')[1],brand] for result in results for brand in result["brands"]]
# print(feature)
# with open('brand.csv', 'w', newline='',  encoding="utf-8") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Model_Id', 'Brand'])
#     for f in feature:
#         writer.writerow([f[0], f[1]])

# 資料庫參數設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "wear",
    "charset": "utf8"
}

try:
# 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        for f in feature:
            command = f'INSERT INTO oftenusebrand(Uid,brands)VALUES("{f[0]}","{f[1]}");'
            cursor.execute(command)
            print('down')
        # 儲存變更
        conn.commit()
    
except Exception as ex:
    print(ex)