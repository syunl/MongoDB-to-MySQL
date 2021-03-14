import pymongo 
from pymongo import MongoClient
import csv
import pymysql
import Get_Mongo
import re
import emoji

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
exist=[]
feature = []
category=['T恤','襯衫','商務襯衫','POLO衫','針織衫','背心外套','連帽外套','運動衫','針織衫/披肩','開衫',\
          '運動服','坦克背心','細肩帶背心','小可愛','休閒西裝','無領外套','無領大衣','牛仔外套','機車外套',\
          '短外套','軍裝外套','MA-1','羽絨衣','羽絨背心','毛呢大衣','連帽長外套','中長外套','插肩外套',\
          '風衣','西裝大衣','羊皮大衣','尼龍夾克','防風外套','運動外套','橫須賀外套','套裝','連體套裝','披肩',\
          '牛仔褲','休閒短褲','休閒長褲','衛褲','西裝休閒褲','背帶褲','連體褲','裙子','牛仔裙','洋裝',\
          '襯衫洋裝','无袖连衣裙','短款洋裝','禮服','禮服褲裝','西裝外套','西裝背心','西裝褲','西裝裙',\
          '西服套裝','領帶','領結','領帶夾','袖扣','西服手帕','單肩包','手提包','背包/雙肩背包',\
          '波士頓包','腰包','手袋','手袋','郵差包','公文包','旅行箱包','水桶包','環保袋','草編包',\
          '球鞋','懒人鞋','涼鞋','高跟鞋','靴子','禮服鞋','芭蕾舞鞋','乐福鞋','懶漢鞋','雨鞋',\
          '沙灘涼鞋','踝靴','皮帶','背帶','太陽鏡','眼鏡','長款圍巾/披巾','圍巾','頸部保暖套/圍脖','手套',\
          '護臂','耳套','裝飾領','錢包','零錢包','便攜小包','手帕/手巾','方巾','錢包鏈','卡包','非智能手錶',\
         '智能手錶','頭繩','髮帶','髮箍','髮夾','发夹','髮圈','項鏈','戒指','耳環','耳夾','全耳式耳環',\
          '手鏈','腕帶','腳鏈','Choker','胸針/胸花','裝飾小物','帽子','寬邊帽','毛綫帽','貝雷帽','報童帽'\
          '遮陽帽','連體褲/背帶褲']
for result in results:
    for sets in result['SET']:
        outfitId = sets['Set_Url'].split('/')[-3] + "_" + sets['Set_Url'].split('/')[-2]
        for item in sets['ITEM']:
            if ">" in item['Item_Type'].split('(')[0]:
                itemType = item['Item_Type'].split('(')[0].split('> ')[-1]
                if itemType not in category:
                    continue
            if item['Item_Color'] == "其他":
                continue
            uniqID = item['Item_Url'].split('/')[-3] + '_' + item['Item_Url'].split('/')[-2] 
            if uniqID not in exist:             
                exist.append(uniqID)
                tempList = []
                tempList.append(item['Item_Url'].split('/')[-3] + '_' + item['Item_Url'].split('/')[-2])
                tempList.append(item['Shop_Url'])
                tempList.append(filter_emoji(item['Item_Type'].split('(')[0].split('> ')[-1].replace('\"','\\\"')))
                tempList.append(item['Item_Color'])
                tempList.append(filter_emoji(item['Item_Brand'].replace('\"','\\\"')))
                tempList.append(outfitId)
                feature.append(tempList)

# print(feature)



# with open('itemInfo.csv', 'w', newline='',  encoding="utf-8") as csvfile:
#     writer = csv.writer(csvfile)
#     for f in feature:
#         writer.writerow([f[0], f[1], f[2], f[3], f[4]])
#Insert to MySQl
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "wear",
    "charset": "utf8"
}

command = ''
try:
# 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        for f in feature:
            try:
                command = f'INSERT INTO iteminfo(ItemId, purchaseUrl, ItemType, color, brand)VALUES("{f[0]}", "{f[1]}", "{f[2]}", "{f[3]}", "{f[4]}");'
                command2 = f'INSERT INTO item(OutfitId,ItemId)VALUES("{f[5]}","{f[0]}");'
                cursor.execute(command)
                cursor.execute(command2)

            except Exception as ex:
                print(ex)
                print(command)
                print(command2)
                
            print('down')
        
        # 儲存變更
        conn.commit()
    
except Exception as ex:
    print(ex)
    print(command)