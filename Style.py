import pymongo 
from pymongo import MongoClient
import csv
import pymysql
import Get_Mongo
import re

def filter_emoji(desstr,restr=''):    
    try:  
        co = re.compile(u'[\U00010000-\U0010ffff]')  
    except re.error:  
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')  
    return co.sub(restr, desstr)  

cluster = MongoClient('mongodb+srv://crawler:!QAZ2wsx@cluster0.k1oua.mongodb.net/wear?retryWrites=true&w=majority')
db = cluster['wear']
collection = db['Mondel_M']
results = collection.find({'Mondel_Rank': '90'})
feature = [
    [sets['Set_Url'].split('/')[-3] + "_" + sets['Set_Url'].split('/')[-2], filter_emoji(style)]
    for result in results for sets in result['SET'] for style in sets['Item_Tag']]

# with open('style.csv', 'w', newline='',  encoding="utf-8") as csvfile:
#     writer = csv.writer(csvfile)
#     for f in feature:
#         writer.writerow([f[0], f[1]])



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
            try:
                command = f'INSERT INTO style(OutfitId,Style)VALUES("{f[0]}","{f[1]}");'
                cursor.execute(command)
                
            except Exception as ex:
                print(ex)
                print(command)
           
            print('down')
        # 儲存變更
        conn.commit()
    
except Exception as ex:
    print(ex)