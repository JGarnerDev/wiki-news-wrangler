from settings import SECRET, F_KEY
from cryptography.fernet import Fernet


cypher = Fernet(F_KEY)


# data = {
#   "timestamp":    timestamp,
#   "description": "This is the raw news data scraped from Wikipedia by wiki-news-scraper",
#   "scraped":      all_scraped_news
# }


def is_auth(data):
    if "pw" in data.keys():
        pw = cypher.decrypt(data['pw']).decode('utf-8')
        if pw == SECRET:
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
