from flask import Flask, jsonify
from flask_cors import CORS
from Anomalies import Anomalies
import pandas as pd

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route('/api/stock/<ticker>')
def get_stock_data(ticker):
    program = Anomalies(ticker)
    df = program.get_information()
    program.calculate_rsi()
    program.detect_anomalies()
    df = program.historical
    if df is None or not isinstance(df, pd.DataFrame):
        return jsonify({'error': 'No data found'}), 404
    # Reset index to get date as a column
    df = df.reset_index()
    # Only send the columns you need
    cols = [col for col in ["Date", "Close", "RSI", "Z-score", "Anomaly"] if col in df.columns]
    return jsonify(df[cols].to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)
