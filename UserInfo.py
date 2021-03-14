import pymongo 
from pymongo import MongoClient
import csv
import pymysql
import Get_Mongo

#Fetch data from Mongodb
cluster = MongoClient('mongodb+srv://crawler:!QAZ2wsx@cluster0.k1oua.mongodb.net/wear?retryWrites=true&w=majority')
db = cluster['wear']
collection = db['Mondel_W']
results = collection.find({'Mondel_Rank': '16'})
feature = [[result['Mondel_ID'].split('/')[1],
            result['Mondel_Gender'],
            result['Mondel_Hight'],
            result['Mondel_Url'],
            result['Mondel_Rank']] for result in results]

#Insert to MySQl
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
            command = f"INSERT INTO userinfo(Uid, Gender, Height, UserURL, UserRanking)VALUES('{f[0]}','{f[1]}', '{f[2]}', '{f[3]}', '{f[4]}');"
            cursor.execute(command)
            print('down')

        # 儲存變更
        conn.commit()
    
except Exception as ex:
    print(ex)