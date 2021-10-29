from flask import Flask
from flask_restful import Api
from utils.Config import Config
from endpoints.Recomendacao import Recomendacao

app = Flask(__name__)
api = Api(app)

config = Config()
app.config.from_object(config)

api.add_resource(Recomendacao, '/api/recomendacao')

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT)