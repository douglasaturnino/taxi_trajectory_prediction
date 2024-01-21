import os
import pickle

import inflection
import pandas as pd



class taxi(object):
    def __init__(self):
        self.home_path = os.path.dirname(os.getcwd())
        self.parameter_path = os.path.join(self.home_path, 'paremeter')

    def data_cleaning(self,df):

        # Renomear colunas
        cols_old = list(df.columns)

        snakecase = lambda x: inflection.underscore( x )
        cols_new = list( map( snakecase, cols_old ) )
        df.columns = cols_new

        # Substituir valores NAN por 0
        df['origin_call'] = df['origin_call'].fillna(0)
        df['origin_stand'] = df['origin_stand'].fillna(0)

        # Alterar tipos de dados
        df['origin_call'] = df['origin_call'].astype(int)
        df['origin_stand'] = df['origin_stand'].astype(int)

        return df

    def data_preparation(self, df):
        call_type_dic = {"A":1, "B":2, "C":3}
        df["call_type"] = df["call_type"].map(call_type_dic)
        return df

    def get_prediction(self, teste_data, model):
        pred = model.predict(teste_data)
        return pred
        