import os
import pickle

import pandas as pd
from flask import Flask, request, Response

from taxi import taxi

# loading model
home = os.getcwd()
model_pah = os.path.join(home, 'model', 'GradientBoostingRegressor.pkl')
model = pickle.load(open(model_pah, 'rb'))

#inicialize API
app = Flask(__name__)

@app.route('/taxi/predict', methods=['GET'])
def index():
    teste_json = request.get_json()

    if teste_json: # there is data
        if isinstance(teste_json, dict): # unique example 
            test_raw = pd.DataFrame(teste_json, index=[0])
        
        else: # multiple example
            test_raw = pd.DataFrame(teste_json, columns=teste_json[0].keys())

        # Instantiate Taxi class
        pipeline = taxi()

        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)

        # feature engineering
        df2 = pipeline.feature_engineering(df1)

        # data preparation
        df3 = pipeline.data_preparation(df2)

        # prediction
        df4 = pipeline.get_prediction(model, df3)
        
        # join pred into the original data
        test_raw[['pred_lat', 'pred_long']] = df4

        return test_raw.to_json(orient='records', date_format='iso')

    else:
        return Response('{}', status=200, mimetype='application/json')
if __name__ == '__main__':
    app.run()