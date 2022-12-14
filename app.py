from flask import Flask, jsonify, request, render_template, make_response, url_for,redirect
import json
import jwt # Perlu install pip3 install PyJWT diawal
import datetime
from functools import wraps
from flask_mysqldb import MySQL
from user import *
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

# City -> State
@app.get("/siti")
def panggil_sity():
    cur = mysql.connection.cursor()
    city = request.args.get("city")
    if not city :
        return jsonify("City tidak ditemukan")
    # query
    # cur.execute(query)
    data = cur.fetchall()
    return jsonify(data)