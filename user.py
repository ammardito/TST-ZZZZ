user = {
    'tes123':'masmu123'
}

def checkValidation(username,password):
    try:
        pw = user[username]
        if pw == password:
            return True
        else:
            return False
    except:
        return False