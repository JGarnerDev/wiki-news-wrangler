from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import MongoClient
import datetime
import json


from settings import DB_RAW_URI, DB_CLEAN_URI, DB_ANALYTICS_URI
from auth import check_data
from wrangler import wrangle

app = Flask(__name__)

app.debug = True
CORS(app)
db_raw = PyMongo(app, uri=DB_RAW_URI).db
db_clean = PyMongo(app, uri=DB_CLEAN_URI).db
db_analytics = PyMongo(app, uri=DB_ANALYTICS_URI).db
api = Api(app)


def form_response(status_code):
    retJson = {
        "message": "Not authorized",
        "status": 401
    }
    if status_code == 400:
        retJson = {
            "message": "Data is insufficient",
            "status": 400
        }
    if status_code == 200:
        print("----------------------")
        print("LEEEEEEEEEROOOOOOOOY")
        print("JENNNNNNNNNNNNNNNNNNNKIIIIIIIINS")
        print("----------------------")
        retJson = {
            "message": "All good! Wrangling is underway",
            "status": 200
        }
    return retJson


class Wrangler(Resource):
    def post(self):

        # get the data
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
        response = form_response(status_code)
        # send a success/fail response
        return jsonify(response)


api.add_resource(Wrangler, "/wrangler")


if __name__ == '__main__':
    app.run(debug=True)
