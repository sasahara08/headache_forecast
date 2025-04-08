import requests, sqlite3, datetime
import pytz

#特定地域の現在から２４時間の気象情報を取得
def getNowParameter(cityName):

    # OpenWeatherのAPIキーとエンドポイント
    API_KEY = '7f8bbcc81532cb8129d34496ee621a39'
    # (例)CITY_NAME = 'Fukuoka,JP'  # 福岡市の場合
    URL = f'https://api.openweathermap.org/data/2.5/forecast?q={cityName}&appid={API_KEY}&units=metric'

    # APIからデータを取得
    response = requests.get(URL)
    return response.json()


#頭痛薬を服用情報を取得
def takingCount(userId):

    #今日の日付を取得
    todayData = datetime.date.today()

    # DB接続--------------------------------------------
    connection = sqlite3.connect('headache.db')
    cursor = connection.cursor()
    # --------------------------------------------------

    #DBから服用情報を取得
    cursor.execute('select * from medicine where date = ? AND userId = ?', (todayData, userId))
    taking = cursor.fetchone()

    return taking
    

# 頭痛薬の服用カウントカラムを生成する
def newCount(userId):

    #今日の日付を取得
    todayData = datetime.date.today()

    #今の時刻を取得
    takingTime = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
    
    # DB接続--------------------------------------------
    connection = sqlite3.connect('headache.db')
    cursor = connection.cursor()
    # --------------------------------------------------

    cursor.execute('''
    insert into medicine (userId, count, drinkTime, date) values
    (?, ?, ?, ?)''', (userId, 1, takingTime, todayData))

    connection.commit()
    connection.close()


# 頭痛薬の服用回数を増やす
def countUp(count, userId):

    #今日の日付を取得
    todayData = datetime.date.today()

    #今の時刻を取得
    takingTime = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')

    # DB接続--------------------------------------------
    connection = sqlite3.connect('headache.db')
    cursor = connection.cursor()
    # --------------------------------------------------

    cursor.execute('''
    update medicine set count = ?, drinkTime = ? where date = ? AND userId = ? ''',
    (count + 1 , takingTime, todayData, userId))

    connection.commit()
    connection.close()


# 都市コードを都市名に変換して返す
def changeName(cityName):
    
    if cityName == "Hokkaido,JP":
        return "北海道"
    elif cityName == "Sendai,JP":
        return "仙台"
    elif cityName == "Tokyo,JP":
        return "東京"
    elif cityName == "Nagoya,JP":
        return "名古屋"
    elif cityName == "Osaka,JP":
        return "大阪"
    elif cityName == "Hiroshima,JP":
        return "広島"
    elif cityName == "Fukuoka,JP":
        return "福岡"
    elif cityName == "Kagoshima,JP":
        return "鹿児島"
    else:
        return "不明"