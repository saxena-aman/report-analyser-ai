from flask import Flask, jsonify

from services.chatgpt.handler import martin_handler
from services.transformer.handler import service2_handler

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"Hello": "World"})

@app.route('/items')
def get_item():
    return jsonify({"Hola": "World"})

@app.route('/services/martin-ask', methods=['GET', 'POST'])
def martin_call():
    return martin_handler()

# @app.route('/services/endpoint2', methods=['GET', 'POST'])
# def service2_route():
#     return service2_handler()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
