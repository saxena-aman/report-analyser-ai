from flask import jsonify, request
from .dao import get_service2_data

def service2_handler():
    if request.method == 'GET':
        data = get_service2_data()
        return jsonify(data)
    return jsonify({"message": "Invalid method"}), 405
