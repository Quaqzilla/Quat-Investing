import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Anomalies:
    def __init__(self, ticker):
        self.ticker = ticker.upper() + ".JO"
        self.historical = None
        self.intrinsic = None
        self.overvalued = False
        self.undervalued = False
        self.signals = []

    def get_information(self):
        try:
            ticker = yf.Ticker(self.ticker)
            fetch_data = ticker.history(period="1y") 

            if fetch_data.empty:
                raise ValueError(f"No data found for {self.ticker}")

            fetch_data["Daily Return"] = fetch_data["Close"].pct_change()
            self.historical = fetch_data.dropna() 

            return self.historical

        except:
            return "This company is not listed on the JSE"

    def calculate_intrinsic_value(self):
        try:
            ticker = yf.Ticker(self.ticker)
            eps = ticker.info.get("trailingEps", 0)
            pe = ticker.info.get("trailingPE", 0)
            growth = ticker.info.get("revenueGrowth", 0)
            y = 9.125
            
            self.intrinsic = (eps * (pe + (growth * 1)) * 4.4/y)

            return f"Intrinsic Value: {self.intrinsic:.2f}"

        except KeyError:
            return "The particular stock cannot be found"
    
    def calculate_rsi(self, window=14):
        if self.historical is None or not isinstance(self.historical, pd.DataFrame):
            self.get_information()
        if self.historical is None or not isinstance(self.historical, pd.DataFrame):
            print("Historical data is not available or invalid.")
            return None
        delta = self.historical["Close"].diff().astype(float).to_numpy()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, np.abs(delta), 0)
        avg_gain = pd.Series(gain).rolling(window=window).mean()
        avg_loss = pd.Series(loss).rolling(window=window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        self.historical["RSI"] = rsi.values
        return self.historical["RSI"]

    def detect_anomalies(self):
        if self.historical is None or not isinstance(self.historical, pd.DataFrame):
            self.get_information()
        if self.historical is None or not isinstance(self.historical, pd.DataFrame):
            print("Historical data is not available or invalid.")
            return None
        mean_return = self.historical["Daily Return"].mean()
        std_return = self.historical["Daily Return"].std()
        self.historical["Z-score"] = (self.historical["Daily Return"] - mean_return) / std_return
        anomaly_threshold = 2
        self.historical["Anomaly"] = np.where(abs(self.historical["Z-score"]) > anomaly_threshold, True, False)
        return self.historical[["Close", "Z-score", "Anomaly"]]

    def validate_entry_signals(self):
        if self.historical is None or not isinstance(self.historical, pd.DataFrame):
            self.get_information()
        if self.historical is None or not isinstance(self.historical, pd.DataFrame):
            print("Historical data is not available or invalid.")
            return []
        if "RSI" not in self.historical.columns:
            self.calculate_rsi()
        anomalies = self.detect_anomalies()
        if anomalies is None:
            return []
        for index, row in anomalies.iterrows():
            z_score = row["Z-score"]
            rsi = self.historical.loc[index, "RSI"]
            price = row["Close"]
            if z_score < -2 and rsi < 30:
                self.signals.append((index, price, "BUY"))
            elif z_score > 2 and rsi > 70:
                self.signals.append((index, price, "SELL"))
        return self.signals

    def visualize(self):
        # Ensure historical data is available and valid
        if self.historical is None or not isinstance(self.historical, pd.DataFrame):
            self.get_information()
        if self.historical is None or not isinstance(self.historical, pd.DataFrame):
            print("Historical data is not available or invalid.")
            return
        if "RSI" not in self.historical.columns:
            self.calculate_rsi()

        sns.set_style("whitegrid")
        fig, ax = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

        # Price Trend
        ax[0].plot(self.historical.index, self.historical["Close"], label="Close Price", color="blue")
        if self.signals:
            ax[0].scatter([s[0] for s in self.signals if s[2] == "BUY"],
                          [s[1] for s in self.signals if s[2] == "BUY"],
                          color="green", marker="^", label="BUY Signal", edgecolors='none')
            ax[0].scatter([s[0] for s in self.signals if s[2] == "SELL"],
                          [s[1] for s in self.signals if s[2] == "SELL"],
                          color="red", marker="v", label="SELL Signal", edgecolors='none')
        ax[0].set_ylabel("Stock Price")
        ax[0].legend()

        # RSI Trend
        if "RSI" in self.historical.columns:
            ax[1].plot(self.historical.index, self.historical["RSI"], label="RSI", color="purple")
            ax[1].axhline(70, linestyle="--", color="red", label="Overbought (70)")
            ax[1].axhline(30, linestyle="--", color="green", label="Oversold (30)")
            ax[1].set_ylabel("RSI")
            ax[1].legend()
        else:
            ax[1].text(0.5, 0.5, 'No RSI data', ha='center', va='center', transform=ax[1].transAxes)

        # Z-score Trend
        if "Z-score" in self.historical.columns:
            ax[2].plot(self.historical.index, self.historical["Z-score"], label="Z-score", color="orange")
            ax[2].axhline(2, linestyle="--", color="red", label="Upper Threshold")
            ax[2].axhline(-2, linestyle="--", color="green", label="Lower Threshold")
            ax[2].set_ylabel("Z-score")
            ax[2].legend()
        else:
            ax[2].text(0.5, 0.5, 'No Z-score data', ha='center', va='center', transform=ax[2].transAxes)

        plt.xlabel("Date")
        plt.tight_layout()
        plt.show()

# Execution
if __name__ == "__main__":
    print("Welcome to Phemelo Quant Investor")
    user_input = input("Please enter your desired stock: ")
    program = Anomalies(user_input)
    program.get_information()
    program.calculate_rsi()
    program.detect_anomalies()
    signals = program.validate_entry_signals()
    for signal in signals:
        print(f"{signal[2]} signal on {signal[0]} at price {signal[1]:.2f}")
    program.visualize()

