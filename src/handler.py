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

@app.route('/predict', methods=['GET'])
def index():
    dados_json = request.get_json()

    if dados_json: # there is data
        if isinstance(dados_json, dict): # unique example 
            raw = pd.DataFrame(dados_json, index=[0])
        
        else: # multiple example
            raw = pd.DataFrame(dados_json, columns=dados_json[0].keys())

        # Instantiate Taxi class
        taxis = taxi()

        df = (raw.pipe(taxis.data_cleaning)
                      .pipe(taxis.data_preparation)
                      .pipe(taxis.get_prediction, model=model))

        # join pred into the original data
        raw[['pred_lat', 'pred_long']] = df

        return raw.to_json(orient='records', date_format='iso')

    else:
        return Response('{}', status=200, mimetype='application/json')
if __name__ == '__main__':
    app.run(debug=True)