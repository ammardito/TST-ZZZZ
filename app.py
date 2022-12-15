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
storage = []
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