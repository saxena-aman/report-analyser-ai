from flask import jsonify, request
from .dao import martin_dao


def martin_handler():
    if request.method == 'POST':
        # Extract s3_url and vs_id from the request body
        request_data = request.json  # Parse the JSON data from the request body
        
        # Check if the required fields are present
        s3_url = request_data.get("s3_url")
        vs_id = request_data.get("vs_id")

        if not s3_url or not vs_id:
            return jsonify({"message": "Missing s3_url or vs_id"}), 400  # Bad Request

        # Call the DAO function with the extracted data (if necessary)
        data = martin_dao(s3_url, vs_id)  # Update your DAO function to accept parameters if needed
        return jsonify(data)

    return jsonify({"message": "Invalid method"}), 405
