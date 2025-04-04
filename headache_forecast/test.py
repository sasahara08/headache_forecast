from flask import Flask, flash, render_template, request, redirect, session
from datetime import datetime
import sqlite3
import model

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# カスタムフィルタを定義
@app.template_filter('timestamp_to_datetime')
def timestamp_to_datetime(timestamp):
    # タイムスタンプを datetime オブジェクトに変換
    return datetime.fromtimestamp(timestamp)

# ホーム画面
@app.route("/", methods=['GET', 'POST'])
def indexAccess():

    # ログインセッション取得
    user = session.get('loginUser')

    # DB接続-----------------------------------------
    connection = sqlite3.connect('headache.db')
    cursor = connection.cursor()
    # -----------------------------------------------

    # テーブル作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
  userId INTEGER PRIMARY KEY AUTOINCREMENT, 
  email VARCHAR(30) NOT NULL, 
  pass VARCHAR(30) NOT NULL
);
    ''')

    cursor.execute('''
  CREATE TABLE IF NOT EXISTS medicine (
  medicineId INTEGER PRIMARY KEY AUTOINCREMENT, 
  userId INTEGER NOT NULL, 
  count INTEGER, 
  drinkTime TIME, 
  date DATE, 
  FOREIGN KEY(userId) REFERENCES users(userId)
);
    ''')

    cursor.execute('''
  CREATE TABLE IF NOT EXISTS mood (
  moodId INTEGER PRIMARY KEY AUTOINCREMENT, 
  userId INTEGER NOT NULL, 
  mood INTEGER, 
  date DATE, 
  FOREIGN KEY(userId) REFERENCES users(userId)
);
    ''')

    connection.close()

    # 都市名を取得(パラメータ無しの場合は福岡)
    cityName = request.form.get('cityName')
    if not cityName:
        cityName = 'Fukuoka,JP'
        
    disPlayCityName = model.changeName(cityName)
    
    # test用jsonデータ
    data_24h = [
  {
    "dt": 1743735600,
    "main": {
      "temp": 13.95,
      "feels_like": 12.63,
      "temp_min": 13.95,
      "temp_max": 14.23,
      "pressure": 1020,
      "sea_level": 1020,
      "grnd_level": 1000,
      "humidity": 47,
      "temp_kf": -0.28
    },
    "weather": [
      {
        "id": 801,
        "main": "Clouds",
        "description": "few clouds",
        "icon": "02d"
      }
    ],
    "clouds": {
      "all": 20
    },
    "wind": {
      "speed": 3.86,
      "deg": 4,
      "gust": 3.75
    },
    "visibility": 10000,
    "pop": 0,
    "sys": {
      "pod": "d"
    },
    "dt_txt": "2025-04-04 03:00:00"
  },
  {
    "dt": 1743746400,
    "main": {
      "temp": 14,
      "feels_like": 12.71,
      "temp_min": 14,
      "temp_max": 14.11,
      "pressure": 1010,
      "sea_level": 1010,
      "grnd_level": 999,
      "humidity": 48,
      "temp_kf": -0.11
    },
    "weather": [
      {
        "id": 801,
        "main": "Clouds",
        "description": "few clouds",
        "icon": "02d"
      }
    ],
    "clouds": {
      "all": 15
    },
    "wind": {
      "speed": 4.12,
      "deg": 350,
      "gust": 3.43
    },
    "visibility": 10000,
    "pop": 0,
    "sys": {
      "pod": "d"
    },
    "dt_txt": "2025-04-04 06:00:00"
  },
  {
    "dt": 1743757200,
    "main": {
      "temp": 12.55,
      "feels_like": 11.24,
      "temp_min": 11.85,
      "temp_max": 12.55,
      "pressure": 1025,
      "sea_level": 1025,
      "grnd_level": 1000,
      "humidity": 53,
      "temp_kf": 0.7
    },
    "weather": [
      {
        "id": 800,
        "main": "Clear",
        "description": "clear sky",
        "icon": "01d"
      }
    ],
    "clouds": {
      "all": 7
    },
    "wind": {
      "speed": 2.8,
      "deg": 358,
      "gust": 3.81
    },
    "visibility": 10000,
    "pop": 0,
    "sys": {
      "pod": "d"
    },
    "dt_txt": "2025-04-04 09:00:00"
  },
  {
    "dt": 1743768000,
    "main": {
      "temp": 9.57,
      "feels_like": 9.11,
      "temp_min": 9.57,
      "temp_max": 9.57,
      "pressure": 1015,
      "sea_level": 1015,
      "grnd_level": 1001,
      "humidity": 66,
      "temp_kf": 0
    },
    "weather": [
      {
        "id": 800,
        "main": "Clear",
        "description": "clear sky",
        "icon": "01n"
      }
    ],
    "clouds": {
      "all": 1
    },
    "wind": {
      "speed": 1.55,
      "deg": 22,
      "gust": 1.74
    },
    "visibility": 10000,
    "pop": 0,
    "sys": {
      "pod": "n"
    },
    "dt_txt": "2025-04-04 12:00:00"
  },
  {
    "dt": 1743778800,
    "main": {
      "temp": 8.73,
      "feels_like": 8.27,
      "temp_min": 8.73,
      "temp_max": 8.73,
      "pressure": 1030,
      "sea_level": 1030,
      "grnd_level": 1000,
      "humidity": 61,
      "temp_kf": 0
    },
    "weather": [
      {
        "id": 803,
        "main": "Clouds",
        "description": "broken clouds",
        "icon": "04n"
      }
    ],
    "clouds": {
      "all": 67
    },
    "wind": {
      "speed": 1.44,
      "deg": 154,
      "gust": 1.35
    },
    "visibility": 10000,
    "pop": 0,
    "sys": {
      "pod": "n"
    },
    "dt_txt": "2025-04-04 15:00:00"
  },
  {
    "dt": 1743789600,
    "main": {
      "temp": 8.39,
      "feels_like": 7.57,
      "temp_min": 8.39,
      "temp_max": 8.39,
      "pressure": 1018,
      "sea_level": 1019,
      "grnd_level": 998,
      "humidity": 64,
      "temp_kf": 0
    },
    "weather": [
      {
        "id": 803,
        "main": "Clouds",
        "description": "broken clouds",
        "icon": "04n"
      }
    ],
    "clouds": {
      "all": 81
    },
    "wind": {
      "speed": 1.73,
      "deg": 135,
      "gust": 1.65
    },
    "visibility": 10000,
    "pop": 0,
    "sys": {
      "pod": "n"
    },
    "dt_txt": "2025-04-04 18:00:00"
  },
  {
    "dt": 1743800400,
    "main": {
      "temp": 8.8,
      "feels_like": 7.75,
      "temp_min": 8.8,
      "temp_max": 8.8,
      "pressure": 1008,
      "sea_level": 1018,
      "grnd_level": 998,
      "humidity": 68,
      "temp_kf": 0
    },
    "weather": [
      {
        "id": 804,
        "main": "Clouds",
        "description": "overcast clouds",
        "icon": "04n"
      }
    ],
    "clouds": {
      "all": 100
    },
    "wind": {
      "speed": 2.05,
      "deg": 163,
      "gust": 2.41
    },
    "visibility": 10000,
    "pop": 0,
    "sys": {
      "pod": "n"
    },
    "dt_txt": "2025-04-04 21:00:00"
  },
  {
    "dt": 1743811200,
    "main": {
      "temp": 11.57,
      "feels_like": 10.38,
      "temp_min": 11.57,
      "temp_max": 11.57,
      "pressure": 1022,
      "sea_level": 1019,
      "grnd_level": 998,
      "humidity": 61,
      "temp_kf": 0
    },
    "weather": [
      {
        "id": 804,
        "main": "Clouds",
        "description": "overcast clouds",
        "icon": "04d"
      }
    ],
    "clouds": {
      "all": 100
    },
    "wind": {
      "speed": 2.39,
      "deg": 165,
      "gust": 4.25
    },
    "visibility": 10000,
    "pop": 0,
    "sys": {
      "pod": "d"
    },
    "dt_txt": "2025-04-05 00:00:00"
  }
]

    # ６時間後の気圧の差が6hPAある場合警告を出す。
    # 0・・・安全　１・・・危険
    dangerNotification = 0

    # 取得した要素内で気圧の低下が見られたら警告を出す。
    for i in range(len(data_24h) - 2):
        if (data_24h[i]['main']['pressure'] - data_24h[i + 2]['main']['pressure'] >= 6) or (data_24h[i]['main']['pressure'] - data_24h[i + 1]['main']['pressure'] >= 6):
            print('気圧が6hPA以上下がっています')
            dangerNotification = 1
    # print(dangerNotification)
    
    # 薬の服用回数を取得（ログインユーザーのみ）
    if user:
        takingCount = model.takingCount(user[0])
    else:
        takingCount = None

    return render_template('index.html',
                           disPlayCityName=disPlayCityName,
                           data_24h=data_24h,
                           dangerNotification=dangerNotification,
                           user=user,
                           takingCount=takingCount
                           )


# 頭痛薬服用時に服用回数を増やして遷移
@app.route("/countUp", methods=['GET', 'POST'])
def countUp():

    # ログインセッション取得
    user = session.get('loginUser')

    # 薬の服用回数を取得
    takingCount = model.takingCount(user[0])

    # 本日の服用がない場合はtrue(レコードを新規作成)
    # 本日の服用がある場合はカウントアップしてリダイレクト
    if not takingCount:
        model.newCount(user[0])
    else:
        count = takingCount[2]
        model.countUp(count, user[0])

    return redirect('/')

# ログイン・ログアウト処理-----------------------------------------------------------------


# ログインページに遷移
@app.route('/login', methods=['GET'])
def getLogin():
    return render_template('login.html')


# ログイン処理(login--->index)
@app.route('/login', methods=["POST"])
def postLogin():

    # parameter受け取り
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    # DB接続(userテーブルからデータを取得してログイン処理を行う)----
    connection = sqlite3.connect('headache.db')
    cursor = connection.cursor()
    # --------------------------------------------------

    # DBからuser情報を取得
    cursor.execute('select * from users where email = ?', (email,))
    user = cursor.fetchone()

    # 入力されたuser情報の照合
    if not email or not password:
        msg = 'メールアドレスとパスワードを入力してください'
        return render_template('login.html', msg=msg)
    elif not user:
        msg = '入力されたメールアドレスもしくはパスワードが間違えています'
        return render_template('login.html', msg=msg)
    elif user[2] != password:
        msg = '入力されたメールアドレスもしくはパスワードが間違えています'
        return render_template('login.html', msg=msg)
    else:
        # セッション追加
        session['loginUser'] = user
        msg = 'ログインしました。'
        return redirect('/')


# ログアウト処理
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('loginUser', None)
    flash('ログアウトしました。', 'info')  # メッセージを一時保存
    return redirect('/')



# 新規登録ページに遷移
@app.route('/signup', methods=['GET'])
def getSignin():
    # ログインセッション取得
    user = session.get('loginUser')

    return render_template('signup.html', user = user)


# 新規登録
@app.route('/signup', methods=['POST'])
def postSignin():

    # parameter受け取り
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    # DB接続--------------------------------------------
    connection = sqlite3.connect('headache.db')
    cursor = connection.cursor()
    # --------------------------------------------------

    # DBからuser情報を取得
    cursor.execute('select * from users where email = ?', (email,))
    user = cursor.fetchone()
    
    # 入力されたuser情報の照合
    if not email or not password:
        msg = 'メールアドレスとパスワードを入力してください'
        return render_template('signup.html', msg = msg)
    elif user:
        msg = '入力されたメールアドレスはすでに使用されています'
        return render_template('signup.html', msg = msg)
    else:
        cursor.execute(
            '''insert into users (email, pass) values (?, ?)''', (email, password))
        connection.commit()

    connection.close()

    msg = '新規登録完了しました'

    return render_template('login.html', msg = msg)

# -----------------------------------------------------------------------------------


app.run()
