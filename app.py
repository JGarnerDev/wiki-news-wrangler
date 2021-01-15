from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import json
import urllib.parse


from settings import DB_USER, DB_PASS, DB_HOST, DB_RAW_NAME, DB_CLEAN_NAME, DB_ANALYTICS_NAME
from auth import check_data
from wrangler import wrangle


app = Flask(__name__)

app.debug = True
CORS(app)

limiter = Limiter(app, key_func=get_remote_address,
                  default_limits=["2 per hour"])

DB_HOST = urllib.parse.quote_plus(DB_HOST)
DB_USER = urllib.parse.quote_plus(DB_USER)
DB_PASS = urllib.parse.quote_plus(DB_PASS)


db_raw = MongoClient(DB_HOST, username=DB_USER, password=DB_PASS,
                     authSource=DB_RAW_NAME, authMechanism='SCRAM-SHA-256').db
db_clean = MongoClient(DB_HOST, username=DB_USER, password=DB_PASS,
                       authSource=DB_CLEAN_NAME, authMechanism='SCRAM-SHA-256').db
db_analytics = MongoClient(DB_HOST, username=DB_USER, password=DB_PASS,
                           authSource=DB_ANALYTICS_NAME, authMechanism='SCRAM-SHA-256').db


api = Api(app)


def form_response(status_code=401):
    switch = {
        201: json.dumps({'message': 'All good! Wrangling underway.'}),
        401: json.dumps({'error': 'Unauthorized', 'message': 'Password is invalid or not present.'}),
        405: json.dumps({'error': 'Method Not Allowed', 'message': "Request method is not offered at this endpoint."}),
        406: json.dumps({'error': 'Not Acceptable', 'message': 'Data provided does not conform to specifications.'}),
        421: json.dumps({'error': 'Misdirected Request', 'message': 'No endpoint'}),
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
            time = '{:%Y-%m-%d}'.format(datetime.datetime.now())
            # send raw data to a db
            db_raw[time].insert_one(data)
            # wrangle, send to a db, return analytics
            analytics = wrangle(data, db_clean[time])
            # send analytics to a db
            db_analytics[time].insert_one(analytics)
        # create a response
        return form_response(status_code)
        # send a success/fail response

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
    app.run(port=33507)
