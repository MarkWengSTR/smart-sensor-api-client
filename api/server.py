from flask import Flask, request, jsonify
from flask_cors import CORS

from use_case_1 import get_plant_data, get_detailed_sensor_and_asset_data, get_simplified_asset_data
from use_case_5 import get_latest_measurements

app = Flask(__name__)
CORS(app)  # local development cors

@app.route('/get_plant_data', methods=["get"])
def get_plan_data_api():
    return jsonify(get_plant_data.run_task(debug=True))

@app.route('/get_detailed_sensor_and_asset_data', methods=["get"])
def get_detailed_sensor_and_asset_data_api():
    return jsonify(get_detailed_sensor_and_asset_data.run_task(debug=True))

@app.route('/get_simplified_asset_data', methods=["get"])
def get_simplified_asset_data_api():
    return jsonify(get_simplified_asset_data.run_task(debug=True))

@app.route('/get_latest_measurements', methods=["get"])
def get_latest_measurements_api():
    return jsonify(get_latest_measurements.run_task(debug=True))

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(port=5000, debug=True)
