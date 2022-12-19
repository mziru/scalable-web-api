import json

with open('auth.txt') as f:
    credentials_string = f.read()

PASSWD = json.loads(credentials_string)


def basic_auth(username, password):
    if PASSWD.get(username) == password:
        return {"sub": username}
    return None
