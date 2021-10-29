from flask import request
from flask_restful import Resource, reqparse
from services.PredictService import PredictService

model = reqparse.RequestParser()
model.add_argument('TamanhoContainer', type=float, help='Informe o tamanho da embalagem da bebida', required=True)
model.add_argument('PercentualAlcoolico', type=float, help='Informe o percentual alcoolico da bebida', required=True)
model.add_argument('Variedade', type=str, help='Informe a variedade da bebida', required=True)
model.add_argument('Segmento', type=str, help='Informe o segmento da bebida', required=True)
model.add_argument('Descricao', type=str, help='Informe a descrição da bebida', required=True)
model.add_argument('Harmonizacao', type=str, help='Informe os produtos que hamonizam com a bebida', required=True)
model.add_argument('Ingredientes', type=str, help='Informe os ingrientes que compoem a bebida', required=True)
model.add_argument('Alergico', type=str, help='Informe os ingridiente que são alergicos as pessoas', required=True)
model.add_argument('Temperatura', type=str, help='Informe a temperatura que a bebida deve ser armazenada', required=True)
model.add_argument('Ibu', type=int, help='Informe o taxa de amargor da bebida', required=True)

class Recomendacao(Resource):

    def __init__(self):
        self.__service = PredictService()
        pass

    def post(self):
        arg: dict = model.parse_args()
        query_top = request.args.get('top', '1')

        top = 3
        
        if query_top is not '':
            top = int(query_top)

        predict = self.__service.predict(arg, top)
        return dict(message='ok', predict=predict), 200

