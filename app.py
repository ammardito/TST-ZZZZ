from flask import Flask, jsonify, request
import json
from flask_mysqldb import MySQL

# Intitialise the app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tubestst'
mysql = MySQL(app)
table = 'house'

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
def create():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        status = 'for_sale'
        price = '20,000'
        full_address = 'SoekarnoHatta'
        street = 'Dago'
        city = 'Bandung'
        state = 'Indonesia'
        cur.execute(f'insert into {table} (status,price,full_address,street,city,state) values ("{status}","{price}","{full_address}","{street}","{city}","{state}")')
        mysql.connection.commit()
        return 'New data of the house created'

# Mengubah data (update)
@app.route('/update', methods=['GET','POST','PUT'])
def update():
    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        status = 'sold'
        full_address = 'SoekarnoHatta'
        cur.execute(f'update {table} set status = "{status}" where full_address = "{full_address}"')
        mysql.connection.commit()
        return 'Data of the house updated'

# Menghapus data (delete)
@app.route('/delete', methods=['GET','POST','DELETE'])
def delete():
    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        full_address = 'SoekarnoHatta'
        cur.execute(f'delete from {table} where full_address = "{full_address}"')
        mysql.connection.commit()
        return 'Data of the house deleted'


@app.route("/tes", methods=['GET','POST'])
def bukti():
    cur = mysql.connection.cursor()
    if request.method == 'GET':
        full_address = 'SoekarnoHatta'
        cur.execute(f'select * from {table} where full_address = "{full_address}"')
        data = cur.fetchall()
        return jsonify(data)