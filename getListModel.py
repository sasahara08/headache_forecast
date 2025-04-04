import pytz, datetime

# 現在時刻より先の値を取得（24時間分/3時間おきに）
def getList(weatherData):
    
    # 日本のタイムゾーンを取得
    jst = pytz.timezone('Asia/Tokyo')
    
    # 現在時刻を日本時間で取得
    current_datetime = datetime.datetime.now(jst)
    current_timestamp = current_datetime.timestamp()
    
    listPoint = 0
    
    for i in range(len(weatherData['list'])):  # weatherData['list'] をループ処理
        if weatherData['list'][i]['dt'] - current_timestamp >= 0:
            print(weatherData['list'][i]['dt'])
            print(current_timestamp)
            print(weatherData['list'][i]['dt'] - current_timestamp)
            break
        else:
            listPoint += 1
            
    return weatherData['list'][listPoint:(listPoint + 8)]