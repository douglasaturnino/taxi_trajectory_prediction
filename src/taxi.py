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

        df = df[['call_type','origin_call','origin_stand', 'missing_data','timestamp', 'polyline']].copy()

        # Substituir valores NAN por 0
        df['origin_call'] = df['origin_call'].fillna(0)
        df['origin_stand'] = df['origin_stand'].fillna(0)

        # Alterar tipos de dados
        df['origin_call'] = df['origin_call'].astype(int)
        df['origin_stand'] = df['origin_stand'].astype(int)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

        return df

    def feature_engineering(self, df):

        # Criar as coodenadas latitude e logitude
        start_lat = 0
        start_long = 1
        end_lat = -2
        end_long = -1
        df["start_lat"] = self.extract_coordinates(df, start_lat)
        df["start_long"] = self.extract_coordinates(df, start_long)
        df["end_lat"] = self.extract_coordinates(df, end_lat)
        df["end_long"] = self.extract_coordinates(df, end_long)

        # Alterar os tipos de dados
        df["start_lat"] = df["start_lat"].astype(float)
        df["start_long"] = df["start_long"].astype(float)
        df["end_lat"] = df["end_lat"].astype(float)
        df["end_long"] = df["end_long"].astype(float)


        return df[["call_type",'origin_call','origin_stand', 'missing_data', 'start_lat', 'start_long']].copy()

    def extract_coordinates(self, df, coord):

        lista=list()
        for i in range(0,len(df["polyline"])):
            if df["polyline"][i] == '[]':
                ax=0

            else:
                ax = df["polyline"][i].split(',')[coord].strip('[]')

            lista.append(ax)

        return lista


    def data_preparation(self, df):
        df["missing_data"] = df.apply(self.miss_flg, axis=1)

        call_type_dic = {"A":1, "B":2, "C":3}
        df["call_type"] = df["call_type"].map(call_type_dic)
        return df

    def miss_flg(self, df):
        return 1 if df["missing_data"] else 0

    def get_prediction(self, teste_data, model):
        pred = model.predict(teste_data)
        return pred
        