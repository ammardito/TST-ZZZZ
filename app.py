from flask import Flask, jsonify, request, render_template, make_response, url_for,redirect,session
import json
import jwt # Perlu install pip3 install PyJWT diawal
import datetime
import urllib.request, json
from functools import wraps
from flask_mysqldb import MySQL
from flask_mail import Mail,Message #pip install Flask-Mail
from user import *

# Intitialise the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tubestst'

mysql = MySQL(app)
table = 'house'

# Config for URL API & Localhost
app.config['API'] ='http://34.101.40.1/'

app.config.from_pyfile('config.cfg')
mail = Mail(app)

app.config['SECRET_KEY'] ='tesautentikasi'
headerTable = ['status','price','bed','bath','acre_lot','full_address','street','city','state','zip_code','house_size','sold_date','crimeRate']
# Define what the app does

# Token Required
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' not in session:
            return redirect('/login')
        try:
            data = jwt.decode(session['token'],app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            session.pop('token',None)
            session.pop('user',None)
            return jsonify({'message':'Token is invalid'}),403
        return f(*args,**kwargs)
    return decorated

def authorization_Admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = jwt.decode(session['token'],app.config['SECRET_KEY'],algorithms=['HS256'])
        if data['role'] != 'admin':
            return ({'message':'you do not permission to access '})
        return f(*args,**kwargs)
    return decorated

# Login
@app.route('/login',methods=['GET','POST'])
def login():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        form = request.form
        username = form['username']
        password = form['password']
        if checkValidation(username,password):
            print('VALIDASI')
            session['user'] = username
            session['email'] = user[username]['email']
            return redirect('/verify')
        else:
            return('Password atau username salah')
    return render_template('login.html')

# Kirim OTP
@app.route('/verify',methods=['GET','POST'])
def verify():
    email = session['email']
    msg = Message('Confirm Email Anda',sender='ammarditoshafaat2001@gmail.com',recipients=[email])
    otp = generateOTP()
    session['otp'] = otp
    msg.body = f'Masukkan OTP berikut: {otp}'
    print(email)
    print(otp)
    mail.send(msg)
    return render_template('verify.html')

# Validasi OTP
@app.route('/validate',methods=['POST'])
def validate():
    userOTP = request.form['otp']
    if session['otp'] == userOTP:
        username = session['user']
        token = jwt.encode({'user':username,'role':user[username]['role'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=2)},app.config['SECRET_KEY'])
        session['token'] = token
        return jsonify('Anda sudah bisa mengelola API')
    else:
        return jsonify('OTP invalid')

# Log out
@app.get('/logout')
def logout():
    session.pop('user',None)
    session.pop('token',None)
    return('Session end')

# Homepage
@app.get("/")
def landing():
    return jsonify('Welcome to API House Recommendation with Considering Crime Rate')

# Core-API -> Pemanfaat API dari teman sekelompok : Aufa Fauqi Ardhiqi(18220096)   
@app.route('/core-api',methods=['GET','POST'])
# @token_required
def coreAPI():
    url = f"{app.config['API']}/data/crimesRate?sort=desc"
    response = urllib.request.urlopen(url)
    dataAPI = response.read()
    crimesRateData = json.loads(dataAPI)
    lenOfHeader = len(headerTable)
    cur = mysql.connection.cursor()
    cleanData = ()
    # form = request.form
    # state = form['state']
    # city = form['city']
    # print(crimesRateData)
    for i in range (0,(len(crimesRateData) - 1)):
        query = f'''select *, "{crimesRateData[i]['crimeRate']}" as crimeRate from {table} where state = "{crimesRateData[i]['state']}" limit 1 '''
        print(query)
        cur.execute(query)
        data = cur.fetchall()
        cleanData += data
    print(cleanData)
    lenData = len(cleanData)
    print(len(crimesRateData))
    return render_template('coreAPI.html',headerTable=headerTable,lenOfHeader=lenOfHeader,lenData=lenData,data=cleanData)

# Penyedia API untuk teman sekelompok dari saya Ammardito Shafaat (18220074)
@app.get("/siti")
def panggil_siti():
    stateList = []
    cur = mysql.connection.cursor()
    city = request.args.get("city")
    if not city :
        return jsonify({"City tidak ditemukan"})
    query = f'SELECT DISTINCT state FROM {table} WHERE city = "{city}"'
    cur.execute(query)
    data = cur.fetchall()
    for d in data:
        stateList.append(d[0])
    return jsonify(stateList)

# Membaca data (read)
@app.route("/show",methods=['GET','POST'])
def read():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        form = request.form
        state = form['state']
        if not state:
            cur.execute(f'''select * from {table} limit 10''')
            data = cur.fetchall()
            return render_template('show.html',data = data)
        cur.execute(f'select * from {table} where state = {state} limit 10')
        data = cur.fetchall()
        return render_template('show.html',data = data)
    cur.execute(f'''select * from {table} limit 10''')
    data = cur.fetchall()
    return render_template('show.html',data = data)

# Menambahkan data (create)
@app.route("/create", methods=['GET','POST'])
@token_required
@authorization_Admin
def create():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        form = request.form
        status = form['status']
        price = form['price']
        full_address = form['full_address']
        cur.execute(f'insert into {table} (status,price,full_address) values ("{status}","{price}","{full_address}"")')
        mysql.connection.commit()
        return jsonify('New data of the house created')
    return render_template('create.html')

# Mengubah data (update)
@app.route('/update', methods=['GET','POST','PUT'])
@token_required
@authorization_Admin
def update():
    cur = mysql.connection.cursor()
    if request.method == 'PUT':
        payload = request.get_json()
        status = payload['status']
        full_address = payload['full_address']
        cur.execute(f'update {table} set status = "{status}" where full_address = "{full_address}"')
        mysql.connection.commit()
    return render_template('update.html')

# Menghapus data (delete)
@app.route('/delete', methods=['GET','POST','DELETE'])
@token_required
@authorization_Admin
def delete():
    cur = mysql.connection.cursor()
    if request.method == 'DELETE':
        payload = request.get_json()
        full_address = payload['full_address']
        cur.execute(f'delete from {table} where full_address = "{full_address}"')
        mysql.connection.commit()
    return render_template('delete.html')