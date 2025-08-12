import yfinance as yf
import pandas as pd
import logging

def collect_raw_stock_data(stocks, period):
     data = yf.download(stocks, period=period, group_by='ticker')
     data = data.stack(level=0,future_stack=True).reset_index()
     return pd.DataFrame(data)

def fix_columns(df):
     df.columns.name = ''
     df.columns = df.columns.str.lower().str.replace(' ','_')



def main():
    logging.basicConfig(level=logging.INFO)
    
    stocks = ['META', 'AAPL', 'AMZN', 'NFLX','SAP', 'GOOG', 'NVDA']


    try:
        df = collect_raw_stock_data(stocks, '2y')
        fix_columns(df)

        df.to_csv('raw_stocks.csv', index=False)

      
    except Exception as e:
        logging.error(f"Collecting raw data failed: {str(e)}")
        raise
    


if __name__ == "__main__":
    main()
