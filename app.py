import lightgbm as lgb
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import pickle

from flask import Flask
from flask import request
import requests
from flask import jsonify

import os
import json
from ast import literal_eval
import traceback

application = Flask(__name__)

# загружаем модели из файла
vec = pickle.load(open("./models/tfidf.pickle", "rb"))
model = lgb.Booster(model_file='./models/my_lgbm_model.txt')


# тестовый вывод
@application.route("/")
def hello():
    resp = {'message': "Hello World!"}

    response = jsonify(resp)

    return response


# предикт категории
@application.route("/categoryPrediction", methods=['GET', 'POST'])
def registration():
    resp = {'message': 'ok'
        , 'category': -1
            }

    try:
        getData = request.get_data()
        json_params = json.loads(getData)

        # напишите прогноз и верните его в ответе в параметре 'prediction'
        message = json_params['user_message']

        result = model.predict(vec.transform([message]).toarray())

        #resp['prediction'] = result.tolist()  
        pred = result.tolist()
        resp['message'] = str(message)        
        resp['category'] = pred.argmax()


    except Exception as e:
        print(e)
        resp['message'] = e

    response = jsonify(resp)

    return response


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    application.run(debug=False, port=port, host='0.0.0.0', threaded=True)
