import pickle

import os
import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

class PredictService:
    def __init__(self):
        directory = os.path.abspath(os.path.dirname(__file__))

        self.__df = pd.DataFrame(columns=['ProdutoTamanhoContainer', 'ProdutoPercentAlcoolico', 'ProdutoVariedade', 'ProdutoSegmento1', 'Descricao', 'Harmonizacao', 'Ingredientes', 'Alergico', 'Temperatura', 'Ibu'])
        self.__data = pd.read_csv(os.path.join(directory, 'dataset/produto_data.csv'))

        encoders: dict = pickle.load(open(os.path.join(directory, 'transformers/encoders_produto.pickle'), 'rb'))
        self.__variedade_encoder: LabelEncoder = encoders.get('ProdutoVariedade')
        self.__segmento_encoder: LabelEncoder = encoders.get('ProdutoSegmento1')
        
        scalers: dict = pickle.load(open(os.path.join(directory, 'transformers/scalers_produto.pickle'), 'rb'))
        self.__container_scaler : MinMaxScaler= scalers.get('ProdutoTamanhoContainer')
        self.__percent_alcoolico_scaler: MinMaxScaler = scalers.get('ProdutoPercentAlcoolico')
        self.__variedade_scaler: MinMaxScaler = scalers.get('ProdutoVariedade')
        self.__segmento1_scaler: MinMaxScaler = scalers.get('ProdutoSegmento1')
        
        self.__tf_idf:TfidfVectorizer = pickle.load(open(os.path.join(directory, 'transformers/tf_idf.pickle'), 'rb'))
        self.__model: SVC = pickle.load(open(os.path.join(directory, 'model/model.pickle'), 'rb'))

    
    def predict(self, args: dict, top: int = 3):
        df_predict = self.__df.copy()
        df_predict.loc[0] = [args.get('TamanhoContainer', 0.0),
                            args.get('PercentualAlcoolico', 0.0),
                            args.get('Variedade', ''),
                            args.get('Segmento', ''),
                            args.get('Descricao', ''),
                            args.get('Harmonizacao', ''),
                            args.get('Ingredientes', ''),
                            args.get('Alergico', ''),
                            args.get('Temperatura', ''),
                            args.get('Ibu', 0.0)]
        
        df_predict = self.__fill_dataset(df_predict)
        result = self.__model.predict(df_predict)

        if not result or len(result) == 0:
            return []

        recomendacao = self.__data[self.__data['cluster_caracteristica'] == result[0]][['PedidoProdutoId', 'ProdutoSubmarca', 'ProdutoTamanhoContainer', 'ProdutoSegmento1', 'ProdutoPercentAlcoolico']][0:top]
        return recomendacao.rename(columns={'PedidoProdutoId': 'Id', 'ProdutoSubmarca': 'Submarca', 'ProdutoTamanhoContainer': 'Litros', 'ProdutoSegmento1': 'Segmento', 'ProdutoPercentAlcoolico': 'PercentualAlcoolico'}).to_dict('record')

    def __fill_dataset(self, df_predict):
        df_predict['ProdutoVariedade'] = df_predict['ProdutoVariedade'].apply(lambda x: x if x in self.__variedade_encoder.classes_ else self.__variedade_encoder.classes_[0])
        df_predict['ProdutoVariedade'] = self.__variedade_encoder.transform(df_predict['ProdutoVariedade'])

        df_predict['ProdutoSegmento1'] = df_predict['ProdutoSegmento1'].apply(lambda x: x if x in self.__segmento_encoder.classes_ else self.__segmento_encoder.classes_[0])
        df_predict['ProdutoSegmento1'] = self.__segmento_encoder.transform(df_predict['ProdutoSegmento1'])

        df_predict['ProdutoTamanhoContainer'] = self.__container_scaler.transform(df_predict['ProdutoTamanhoContainer'].values.reshape(-1,1))
        df_predict['ProdutoPercentAlcoolico'] = self.__percent_alcoolico_scaler.transform(df_predict['ProdutoPercentAlcoolico'].values.reshape(-1,1))
        df_predict['ProdutoVariedade'] = self.__variedade_scaler.transform(df_predict['ProdutoVariedade'].values.reshape(-1,1))
        df_predict['ProdutoSegmento1'] = self.__segmento1_scaler.transform(df_predict['ProdutoSegmento1'].values.reshape(-1,1))

        df_predict['Descricao'] = df_predict['Descricao'] + '. ' + df_predict['Harmonizacao'] + '. '+ df_predict['Ingredientes'] + '. '+ df_predict['Alergico'] + '. ' + df_predict['Temperatura'] + '. ' + df_predict['Ibu'].astype(str)
        df_predict.drop(columns=['Harmonizacao', 'Ingredientes', 'Alergico', 'Temperatura', 'Ibu'], inplace=True)
        bow = self.__tf_idf.transform(df_predict['Descricao'])

        features = pd.DataFrame(bow.toarray(), columns=self.__tf_idf.get_feature_names())
        df_predict = pd.concat([df_predict, features], axis=1)
        df_predict.drop(columns=['Descricao'], inplace=True)
        return df_predict

     