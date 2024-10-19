from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"Hello": "World"})

@app.route('/items')
def get_item():
    return jsonify({"Hola": "World"})

if __name__ == '__main__':
    app.run(debug=True)
