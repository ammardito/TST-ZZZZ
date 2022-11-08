from flask import Flask, jsonify, request,render_template
import json
# Intitialise the app
app = Flask(__name__)
# Bikin jsonify sorted sesuai dengan code
app.config['JSON_SORT_KEYS'] = False

def read_json(filename="data.json"):
    with open(filename,"r") as read_file:
        data = json.load(read_file)
        return data
def write_json(new_name,usia,filename="data.json"):
    with open(filename,"r+") as file:
        file_data = json.load(file)
        file_data["result"]["nama"] = new_name
        file_data["result"]["usia"] = int(usia)
        file.seek(0)
        json.dump(file_data,file,indent=4)
        file.truncate()
# Define what the app does
@app.get("/")
def index():
    return render_template("index.html")

@app.get("/editData")
def editName():
    name = request.args.get("name")
    umur = request.args.get("usia")
    data = read_json()
    dUmur = data["result"]["usia"]
    dName = data["result"]["nama"]
    if not name and not umur:
        return jsonify({"status":"error"})    
    elif name and not umur:        
        write_json(name,dUmur)
    elif not name and umur:
        write_json(dName,umur)
    else:
        write_json(name,umur)
    data = read_json()
    return jsonify(data)