from flask import Flask, jsonify
from Anomalies import Anomalies
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/stock/<ticker>')
def get_stock_data(ticker):
    program = Anomalies(ticker)
    program.get_information()
    program.calculate_rsi()
    anomalies = program.detect_anomalies()
    
    # Convert DataFrame to JSON
    return jsonify(anomalies.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
