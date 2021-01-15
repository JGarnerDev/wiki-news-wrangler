from settings import SECRET, F_KEY
from cryptography.fernet import Fernet

key = bytes(F_KEY, 'utf-8')
f = Fernet(key)


def is_auth(data):
    if "token" in data.keys():
        b = f.decrypt(bytes(data['token'], 'utf-8'))
        pw_attempt = b.decode('utf-8')
        if pw_attempt == SECRET:
            return True
    return False


def is_valid(data):
    if "scraped" in data.keys():
        return True
    return False


def check_data(data):
    if not is_auth(data):
        return 401
    if not is_valid(data):
        return 406
    return 200
