from flask import Flask, jsonify, request, render_template, make_response, url_for,redirect
import json
import random
import jwt # Perlu install pip install PyJWT diawal
import datetime
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

app.config.from_pyfile('config.cfg')
mail = Mail(app)

app.config['SECRET_KEY'] ='tesautentikasi'
storage = []
userData = {
    "email" : '',
    "otp": ''
}

# Token Required
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if len(storage) == 0:
            return jsonify({'message':'Token is missing'}),403
        try:
            data = jwt.decode(storage[0],app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            return jsonify({'message':'Token is invalid'}),403
        return f(*args,**kwargs)
    return decorated
    
#Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username = form['username']
        password = form['password']
        if checkValidation(username,password):
            token = jwt.encode({'user':username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=10)},app.config['SECRET_KEY'])
            storage.append(token)
            return jsonify(token=token)
        else:
            return jsonify('Password atau username salah')
    return render_template('login.html')

# Define what the app does

# Tampilan data (Read)
@app.route("/", methods=['GET','POST'])
def nampilkan():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        cur.execute(f'select * from {table} limit 10')
        data = cur.fetchall()
        return jsonify(data)

# Menambahkan data (create)
@app.route("/create", methods=['GET','POST'])
@token_required
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
def delete():
    cur = mysql.connection.cursor()
    if request.method == 'DELETE':
        payload = request.get_json()
        full_address = payload['full_address']
        cur.execute(f'delete from {table} where full_address = "{full_address}"')
        mysql.connection.commit()
    return render_template('delete.html')

@app.route('/email',methods=['GET'])
def sendEmail():
    return render_template('email.html')

def generateOTP():
    finalOTP= ''
    for i in range (4):
        finalOTP = finalOTP + str(random.randint(0,9))
    return finalOTP

@app.route('/verify',methods=['GET','POST'])
def verify():
    email = request.form['email']
    userData['emai'] = email
    msg = Message('Confirm Email Anda',sender='test@tes.com',recipients=[email])
    otp = generateOTP()
    userData['otp'] = otp
    msg.body = f'Masukkan OTP berikut: {otp}'
    print(email)
    # print(userData['email'])
    print(otp)
    # mail.send(msg)
    return render_template('verify.html')

@app.route('/validate',methods=['POST'])
def validate():
    userOTP = request.form['otp']
    if userData['otp'] == userOTP:
        token = jwt.encode({'user':userData['email'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=10)},app.config['SECRET_KEY'])
        storage.append(token)
        return jsonify('Anda sudah bisa mengelola database')
    else:
        return jsonify('OTP invalid')