import random

user = {
    'aufa':{
        "password":"sunardo",
        'email':'ardhiqi@gmail.com',
        "role":"user"
    },
    'dito':{
        "password":"masmu123",
        "email":'ammarditoshafaat2001@gmail.com',
        "role":"admin"
    }
}

def checkValidation(username,password):
    try:
        pw = user[username]['password']
        if pw == password:
            return True
        else:
            return False
    except:
        return False

def generateOTP():
    finalOTP= ''
    for i in range (4):
        finalOTP = finalOTP + str(random.randint(0,9))
    return finalOTP