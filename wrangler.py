import re
from unidecode import unidecode
from dms2dec.dms_convert import dms2dec
from urllib.parse import quote
import requests

from settings import HERE_API_KEY


def location_help_from_here_api_with(clue):
    query = "https://geocode.search.hereapi.com/v1/geocode?q=%s&apiKey=%s" % (
        clue, HERE_API_KEY)
    response = requests.get(query)
    response_dict = response.json()
    if len(response_dict['items']):
        return response_dict['items'][0]['position']
    else:
        return None


def cleanup_and_get_location_data_for(news):
    keys = news.keys()

    if "content" in keys:
        for i, content in enumerate(news['content']):
            content = re.sub(
                r"\[\d\]", "", content)
            content = unidecode(content)
            news['content'][i] = content

    if 'geo_dec' in keys:
        coords = news['geo_dec'].split(' ')
        for i, coord in enumerate(coords):
            for s in coord:
                if (s == "S" or s == "W"):
                    coords[i] = f"-{coord}"[:-2]
                else:
                    coords[i] = f"{coord}"[:-2]
        news['coords'] = {'lat': coords[0], 'lon': coords[1]}

    elif 'geo_dms' in keys:
        coords = news['geo_dms'].split(' ')
        for i, coord in enumerate(coords):
            coords[i] = dms2dec(coord.strip())
        news['coords'] = {'lat': coords[0], 'lon': coords[1]}

    elif 'location_string' in keys:
        news['coords'] = location_help_from_here_api_with(
            news['location_string'])
    elif 'ptod' in keys:
        news['coords'] = location_help_from_here_api_with(
            news['ptod'])

    else:
        news['coords'] = location_help_from_here_api_with(news['title'])

    return news


def wrangle(data, collection):
    data_clean = {}
    for category in data['scraped']:
        data_clean[category] = []
        for news in data['scraped'][category]:
            data_clean[category].append(
                cleanup_and_get_location_data_for(news))

    collection.insert_one(data_clean)
    analytics = {"ass": "butt"}
    return analytics
