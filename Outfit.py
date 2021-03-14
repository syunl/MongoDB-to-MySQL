import pymongo 
from pymongo import MongoClient
import csv
import pymysql
import Get_Mongo
import datetime

cluster = MongoClient('mongodb+srv://crawler:!QAZ2wsx@cluster0.k1oua.mongodb.net/wear?retryWrites=true&w=majority')
db = cluster['wear']
collection = db['Mondel_W']
results = collection.find({'Mondel_Rank': { "10": "15" }})
feature = []
for result in results: 
    for sets in result['SET']:
        featL = []
        featL.append(sets['Set_Url'].split('/')[-3] + "_" + sets['Set_Url'].split('/')[-2])
        featL.append(sets['Set_Url'].split('/')[-3])
        
        
        
        if '前' in sets['Update_time']:
            featL.append('2021-01-31')
            featL.append('winter')
            featL.append(sets['Like_Num'])
            
        elif '天' in sets['Update_time']:
            featL.append('2021-01-31')
            featL.append('winter')
            featL.append(sets['Like_Num'])

        else:
            outfitT = sets['Update_time'].replace('.','-').replace('/','-')
            featL.append(outfitT)
            year = int(outfitT.split('-')[0])
            month = int(outfitT.split('-')[1])
            if   3 <= month < 6:
                featL.append('spring')
            elif  6 <= month < 9:
                featL.append('summer')
            elif 9<= month < 12:
                featL.append('autumn')
            else:
                featL.append('winter') 
            if year >= 2020:
                featL.append(int(sets['Like_Num']))
            elif year == 2019:
                featL.append(round(int(sets['Like_Num']) / 2, 3))
            elif year == 2018:
                featL.append(round(int(sets['Like_Num']) / 3, 3))
            else:
                featL.append(round(int(sets['Like_Num']) / 4, 3))
        featL.append(int(sets['Like_Num']))
        featL.append(sets['Img_Url']) 
        featL.append(sets['Set_Url'])
        feature.append(featL)
 

# # Insert to MySQl
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
            command = f"INSERT INTO outfit(OutfitId, Uid, PicUploadTime, Season, LikesAdj, Likes, PicUrl, OutfitUrl)VALUES('{f[0]}','{f[1]}', '{f[2]}', '{f[3]}', '{f[4]}', '{f[5]}','{f[6]}','{f[7]}');"
            cursor.execute(command)
            print('down')

        # 儲存變更
        conn.commit()
    
except Exception as ex:
    print(ex)