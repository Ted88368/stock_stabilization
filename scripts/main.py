import os
import sys
import pandas as pd
from datetime import datetime, timedelta

# Add the libs directory to the system path
LIBS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'libs'))
sys.path.append(LIBS_PATH)

from stabilization import is_stabilized

def fetch_data(ticker):
    """
    Fetches stock data using kdata library.
    ticker: str (e.g., 'us.AAPL', 'hk.0700', 'sh.600000')
    """
    print(f"Fetching data for {ticker} using kdata...")
    try:
        from kdata.data import get_ohlc
        from kdata.provider import Period
        
        # Default to last 90 days
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = "2022-01-01"
        
        df = get_ohlc(ticker, start_date, end_date, period=Period.DAILY)
        
        if df is None or df.empty:
            return None
            
        # Ensure standard column names if kdata differs (assuming OHLCV)
        # Some libraries return lowercase or different names. Adjust as needed.
        # Based on user example, assuming df is standard or handleable by stabilization.py
        return df
    except ImportError:
        print("kdata library not found. Please ensure kdata-3.0.3-py3-none-any.whl is in libs/ and installed.")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/main.py <ticker>")
        print("Example: python scripts/main.py us.AAPL")
        return

    ticker = sys.argv[1]
    df = fetch_data(ticker)
    
    if df is not None:
        result = is_stabilized(df, ticker)
        print("\n--- Stabilization Report ---")
        print(f"Ticker: {result['ticker']}")
        print(f"Stabilized: {'YES' if result['stabilized'] else 'NO'}")
        print(f"Confidence Score: {result['score']}/100")
        print(f"Details: {result['details']}")
    else:
        print(f"Failed to fetch data for {ticker}. Check ticker format (e.g., us.AAPL) and kdata installation.")

if __name__ == "__main__":
    main()


