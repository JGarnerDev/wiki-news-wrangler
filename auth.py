from settings import SECRET


# data = {
#   "timestamp":    timestamp,
#   "description": "This is the raw news data scraped from Wikipedia by wiki-news-scraper",
#   "scraped":      all_scraped_news
# }


def is_auth(data):
    if "pw" in data.keys():
        if data['pw'] == SECRET:
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
        return 400
    return 200
