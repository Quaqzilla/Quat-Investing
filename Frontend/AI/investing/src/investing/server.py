from flask import Flask, request, jsonify, render_template
from investing.main import run
from Backend.Anomalies import Anomalies
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class newsFinder():
    def __init__(self, news_findings=None, summary_of_news=None):
        self.news_findings = news_findings
        self.summary_of_news = summary_of_news

@app.route('/')
def main_page():
    return render_template('index.html')

# News search endpoint expects POST with JSON
@app.route('/news-search', methods=['POST'])
def news_found():
    try:
        data = request.get_json()
        users_ticker_input = data.get("user_input")
        if not users_ticker_input:
            return jsonify({"error": "Missing user_input"}), 400
        finder = newsFinder()
        finder.news_findings = run(users_ticker_input)
        return jsonify({"news_findings": finder.news_findings})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ticker signals endpoint expects GET with query param ?ticker=...
@app.route('/ticker-signals', methods=['GET'])
def ticker_valuation():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Missing ticker parameter"}), 400
    try:
        program = Anomalies(ticker.upper() + ".JO")
        program.get_information()
        program.calculate_rsi()
        program.detect_anomalies()
        signals = program.validate_entry_signals()
        signal_list = [
            {"date": signal[0], "price": signal[1], "type": signal[2]}
            for signal in signals
        ]
        # If visualize returns a plot, you may need to save and return the file path or encode it
        program_run = program.visualize()
        return jsonify({"signals": signal_list, "visualization": str(program_run)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


