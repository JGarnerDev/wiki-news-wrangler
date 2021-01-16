from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_pymongo import pymongo
from pymongo import MongoClient
from flask_cors import CORS


import json
import urllib.parse


from settings import DB_USER, DB_PASS, DB_HOST, DB_RAW_NAME, DB_CLEAN_NAME, DB_ANALYTICS_NAME
from auth import check_data
from wrangler import wrangle
from utils import t_str


app = Flask(__name__)


app.debug = True
CORS(app)

limiter = Limiter(app, key_func=get_remote_address,
                  default_limits=["60 per day"])


api = Api(app)

DB_USER = urllib.parse.quote(DB_USER)
DB_PASS = urllib.parse.quote(DB_PASS)
DB_RAW_NAME = urllib.parse.quote(DB_RAW_NAME)
DB_CLEAN_NAME = urllib.parse.quote(DB_CLEAN_NAME)
DB_ANALYTICS_NAME = urllib.parse.quote(DB_ANALYTICS_NAME)


db_raw = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0.4vass.mongodb.net/%s?retryWrites=true&w=majority" %
                             (DB_USER, DB_PASS, DB_RAW_NAME)).raw
db_clean = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0.4vass.mongodb.net/%s?retryWrites=true&w=majority" %
                               (DB_USER, DB_PASS, DB_CLEAN_NAME)).clean
db_analytics = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0.4vass.mongodb.net/%s?retryWrites=true&w=majority" %
                                   (DB_USER, DB_PASS, DB_ANALYTICS_NAME)).analytics


def form_response(status_code=401):
    awesome = {'message': 'Awesome.'}
    switch = {
        200: json.dumps(awesome),
        201: json.dumps(awesome),
        401: json.dumps({'message': 'Password is invalid or not present.', 'error': 'Unauthorized'}),
        405: json.dumps({'message': "Request method is not offered at this endpoint.", 'error': 'Method Not Allowed'}),
        406: json.dumps({'message': 'Data provided does not conform to specifications.', 'error': 'Not Acceptable'}),
        421: json.dumps({'message': 'No endpoint', 'error': 'Misdirected Request'}),
    }
    msg = switch[status_code]
    return Response(msg, status=status_code, mimetype='application/json')


class Wrangler(Resource):
    def post(self):
        # get the data
        req_body = request.get_json()
        if not req_body:
            return form_response(406)
        data = json.loads(request.get_json())
        # authenticate and validate
        status_code = check_data(data)
        if status_code == 200:
            time = t_str
            # send raw data to a db
            db_raw[time].insert_one(data)
            # wrangle, send to a db, return analytics
            analytics = wrangle(data, db_clean[time])
            # send analytics to a db
            db_analytics[time].insert_one(analytics)
        # create a response, send it
        return form_response(status_code)

    def get(self):
        return form_response(406)

    def head(self):
        return form_response(406)

    def put(self):
        return form_response(405)

    def patch(self):
        return form_response(405)

    def delete(self):
        return form_response(405)

    def options(self):
        return form_response(405)

    def connect(self):
        return form_response(405)

    def trace(self):
        return form_response(405)


class Refuser(Resource):
    def get(self, path="", content=""):
        return form_response(421)

    def head(self, path="", content=""):
        return form_response(421)

    def put(self, path="", content=""):
        return form_response(421)

    def patch(self, path="", content=""):
        return form_response(421)

    def delete(self, path="", content=""):
        return form_response(421)

    def options(self, path="", content=""):
        return form_response(421)

    def connect(self, path="", content=""):
        return form_response(421)

    def trace(self, path="", content=""):
        return form_response(421)


api.add_resource(Wrangler, "/api/wrangler")
api.add_resource(Refuser, "/<path:content>")

if __name__ == '__main__':
    app.run(port=33507, debug=True)
