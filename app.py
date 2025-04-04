from flask import Flask, flash, render_template, request, redirect, session
from datetime import datetime
import sqlite3
import model
import pytz

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# カスタムフィルタを定義
@app.template_filter('timestamp_to_datetime')
def timestamp_to_datetime_jst(timestamp):
    # タイムスタンプをUTCのdatetimeオブジェクトに変換
    utc_time = datetime.fromtimestamp(timestamp, tz=pytz.utc)
    # タイムゾーンをJSTに変換
    jst_timezone = pytz.timezone('Asia/Tokyo')
    jst_time = utc_time.astimezone(jst_timezone)
    return jst_time

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

    # OpenWeatherAPIから気圧情報を取得
    weatherData = model.getNowParameter(cityName)

    # 24時間分のデータを抽出
    data_24h = weatherData['list'][:8]
    # print(data_24h)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run()