import yfinance as yf

class getIntrinsic:
    def __init__(self, ticker):
        self.ticker = ticker
        self.intrinsic = 0
        self.currentPrice = 0
        self.safetyMargin = 10/100


    def valueResult(self):
        try:
            companyResult = yf.Ticker(self.ticker.upper()+".JO")
            eps = companyResult.info.get("trailingEps", 0) or 0.05
            eps = eps * 100
            pe = 8.5
            currentPrice = companyResult.fast_info["last_price"]/100
            growth = companyResult.info.get("earningsGrowth", 0)
            y = 5.46
            
            intrinsicValue = (eps * (pe + (growth * 2)) * 4.4/y)

            self.intrinsic = intrinsicValue
            self.currentPrice = currentPrice

            return(f"Intrinsic Value: {intrinsicValue:.2f}\nGrowth Rate: {growth}")

        except KeyError:
            return("The particular stock can not be found")
        
    def stockSignal(self):
        acceptanceBuyPrice = (1 - self.safetyMargin) * self.intrinsic
        acceptanceBuyPrice = acceptanceBuyPrice/100

        if (self.currentPrice < acceptanceBuyPrice):
            return (f"The acceptance buy price is: {acceptanceBuyPrice:.2f} and the signal is a BUY \n The current price is {self.currentPrice:.2f}")
        else: 
            return (f"The signal is a sell due to a huge difference. The acceptance price is {acceptanceBuyPrice:.2f} \n The current price is {self.currentPrice:.2f}")
        




