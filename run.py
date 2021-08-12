# from flask import request
# from flask import Flask,request
import csv
from flask import Flask, jsonify, render_template, request
from model import RecommendationModel
from utils import prepare_dict_from_request
from flask_cors import CORS, cross_origin
import os


MODEL_PARAMETERS_PATH = os.path.join('ckpt', 'xgb.model')
MODEL_CONFIG_PATH = os.path.join('ckpt', 'config.json')
CUSTOMER_HISTORY_PATH = 'cust_dict.json'

app = Flask(__name__)
PORT = 8080
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={
    r"/recommed": {'origins': "http://*:"+str(PORT)},
})
recommenderModel = RecommendationModel(
    MODEL_PARAMETERS_PATH, MODEL_CONFIG_PATH, CUSTOMER_HISTORY_PATH, 3)


# with open(r'test_ver2.csv', 'r') as f:
#     X = None
#     for row in csv.DictReader(f):

#         print(recommenderModel(row))
#         break


@app.route('/recommend', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def recommend():
    if(request.method == 'POST'):
        # print(request.values.get('HERE'))
        # print(request.values)
        # print()
        in_x = prepare_dict_from_request(request.values)
        prediction, probabilites = recommenderModel(in_x)
        prediction, probabilites = prediction[0], probabilites[0]
        result = {}
        for pred, prob in zip(prediction, probabilites):
            # print(pred, prob)
            result[pred] = str(prob)
        print(result)
        return jsonify(result)
    elif(request.method == 'GET'):
        return jsonify({'None': 'None'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
