from flask import Flask, jsonify
from Anomalies import Anomalies
from Intrinsic import getIntrinsic
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/api/stock/<ticker>')
def get_stock_data(ticker):
    program = Anomalies(ticker)
    df = program.get_information()
    '''
    Fix the RSI "NaN" value to accormodate the JSON values
    '''
    #program.calculate_rsi()
    program.detect_anomalies()
    df = program.historical
    if df is None or not isinstance(df, pd.DataFrame):
        return jsonify({'error': 'No data found'}), 404
    df = df.reset_index()
    cols = [col for col in ["Date", "Close",  "Z-score", "Anomaly"] if col in df.columns]
    df = df[cols].where(pd.notnull(df[cols]), None) 

    intrinsic = getIntrinsic(ticker)
    intrinsic.valueResult()
    signal = intrinsic.stockSignal()

    return  jsonify({
        "signal": signal,
        "data": df.to_dict(orient='records')
    })

if __name__ == "__main__":
    app.run(debug=True)
