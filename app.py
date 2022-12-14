from flask import Flask, jsonify, request, render_template, make_response, url_for,redirect
import json
import jwt # Perlu install pip3 install PyJWT diawal
import datetime
from functools import wraps
from flask_mysqldb import MySQL

# Intitialise the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tubestst'
mysql = MySQL(app)
table = 'house'

app.config['SECRET_KEY'] ='needbucin'
storage = []

# Define what the app does

# Homepage
@app.get("/")
def landing():
    return jsonify('Home Page API House Recommendation Considering Crime Rate')

# Core-API -> Pemanfaat API dari teman sekelompok : Aufa Fauqi Ardhiqi(18220096)   
@app.route('/core-api',methods=['GET','POST'])
# @token_required
def coreAPI():
    cur = mysql.connection.cursor()
    cleanData = []
    form = request.form
    state = form['state']
    city = form['city']
    return jsonify('Home Page API House Recommendation Considering Crime Rate')

# Penyedia API untuk teman sekelompok dari saya Ammardito Shafaat (18220074)
@app.get("/siti")
def panggil_siti ():
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