# from typing import OrderedDict
import xgboost as xgb
import os
import pandas as pd
import json
import numpy as np
from datahandler import XGBDataHandler
# from collections import OrderedDict
from collections import OrderedDict
from utils import Timer
import time
import functools


def timer(timedFunction, *args):
    @functools.wraps(timedFunction)
    def wrapper_timer(*args):
        startTime = time.time()
        value = timedFunction(args)
        endTime = time.time()
        print(endTime-startTime)
        return value

    return wrapper_timer


class RecommendationModel:
    def __init__(self, model_path=r'ckpt\xgb.model', model_config_path=r'ckpt\config.json', cust_history_path=r'cust_dict.json', n_recommendation=7):
        with open(model_config_path, 'r') as f:
            self.model_config = json.load(f)
        self.data_handler = XGBDataHandler(cust_history_path)
        self.model_path = model_path
        self.xgb_model = xgb.Booster()
        self.xgb_model.load_config(self.model_config)
        self.xgb_model.load_model(model_path)
        # print()
        # print(self.model_config['learner'])
        self.model_config = json.loads(self.model_config)
        self.n_recommendations = max(min(int(
            self.model_config['learner']['objective']['softmax_multiclass_param']['num_class']), n_recommendation), 2)
        return

    # @timer
    def __call__(self, X: OrderedDict):
        in_sample = self.data_handler(X)
        prob = self.xgb_model.predict(in_sample)
        # print(predictions)
        predictions = np.argsort(prob, axis=1)
        predictions = np.fliplr(predictions)  # [:, :7]

        return self.data_handler.getTargetFromPrediction(predictions, self.n_recommendations), prob[:self.n_recommendations]
