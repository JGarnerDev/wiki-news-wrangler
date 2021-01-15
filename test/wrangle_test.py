import re
from unidecode import unidecode
from dms2dec.dms_convert import dms2dec
from urllib.parse import quote
import requests

from settings import HERE_API_KEY

news = {
    "title": "Sriwijaya Air Flight 182",
    "href": "https://en.wikipedia.org/wiki/Sriwijaya_Air_Flight_182",
    "content": [
        "Sriwijaya Air Flight 182 was a scheduled domestic passenger flight from Jakarta to Pontianak, Indonesia. On 9 January 2021, the Sriwijaya Air Boeing 737-524 flying the route disappeared from radar four minutes after departure from Soekarno–Hatta International Airport. Officials confirmed that the aircraft crashed in the waters off the Thousand Islands, some 19 nmi (22 mi; 35 km) from the airport. Preliminary investigation suggested that the aircraft's engine(s) were still operating upon impact.",
        "Reported by local fishermen, the search for the aircraft was immediately initiated. Although wreckage, human remains, and clothing have been found, searches for the full aircraft and all passengers are still ongoing. The flight data recorder was recovered on 12 January 2021, but the cockpit voice recorder (CVR) has not yet been recovered. As of 14 January 2021, no survivors have been found.",
        "Prior to Flight 182, the aircraft arrived at Soekarno–Hatta International Airport in Tangerang, Banten at 12:11 PM from Pangkal Pinang Depati Amir Airport.[4] The aircraft was scheduled to take off at 13:25 WIB (06:25 UTC), and was scheduled to arrive at Supadio International Airport in Pontianak, West Kalimantan, at 15:00 WIB (08:00 UTC). After pushing back from the airport's Terminal 2D Gate B1,[5] the aircraft took off from Runway 25R at 14:36 local time (07:36 UTC).[6] The flight took off amid heavy monsoon rain, following a bad weather delay.[7] Due to the significant delay, it was expected to land in Pontianak at 15:50 WIB (08:50 UTC).[5]"
    ],
    "feature_img_src": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Sriwijaya_Air_Boeing_737-524%28WL%29%3B_%40CGK2017_%28cropped%29.jpg/290px-Sriwijaya_Air_Boeing_737-524%28WL%29%3B_%40CGK2017_%28cropped%29.jpg",
    "location_string": "Montreal West"
}


def location_help_from_here_api_with(clue):
    query = "https://geocode.search.hereapi.com/v1/geocode?q=%s&apiKey=%s" % (
        clue, HERE_API_KEY)
    response = requests.get(query)
    response_dict = response.json()
    return response_dict['items'][0]['position']


def wrangle(news):
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

    else:
        news['coords'] = location_help_from_here_api_with(news['title'])

    print(news['coords'])


wrangle(news)
