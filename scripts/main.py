import os
import sys
import json
import pandas as pd
from datetime import datetime, timedelta

# Add the libs directory to the system path
LIBS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'libs'))
sys.path.append(LIBS_PATH)

# Deployment environment check
DATA_CENTER = os.environ.get("K_DATA_CENTER", "/opt/kdata_data")
WATCHLIST_PATH = os.path.join(os.path.dirname(__file__), '..', 'watchlist.json')

from stabilization import is_stabilized

def load_watchlist():
    if os.path.exists(WATCHLIST_PATH):
        with open(WATCHLIST_PATH, 'r') as f:
            return json.load(f)
    return []

def save_watchlist(watchlist):
    with open(WATCHLIST_PATH, 'w') as f:
        json.dump(list(set(watchlist)), f, indent=4)

def fetch_data(ticker):
    """
    Fetches stock data using kdata library.
    """
    try:
        from kdata.data import get_ohlc
        from kdata.provider import Period
        
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = "2022-01-01" # Fetch enough history
        
        df = get_ohlc(ticker, start_date, end_date, period=Period.DAILY)
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def run_analysis(ticker):
    df = fetch_data(ticker)
    if df is not None:
        result = is_stabilized(df, ticker)
        return result
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  uv run scripts/main.py add <ticker>    - Add to watchlist")
        print("  uv run scripts/main.py remove <ticker> - Remove from watchlist")
        print("  uv run scripts/main.py report          - Run batch report")
        print("  uv run scripts/main.py <ticker>        - Quick single analysis")
        return

    cmd = sys.argv[1]
    watchlist = load_watchlist()

    if cmd == "add" and len(sys.argv) > 2:
        ticker = sys.argv[2]
        watchlist.append(ticker)
        save_watchlist(watchlist)
        print(f"Added {ticker} to watchlist.")
    
    elif cmd == "remove" and len(sys.argv) > 2:
        ticker = sys.argv[2]
        if ticker in watchlist:
            watchlist.remove(ticker)
            save_watchlist(watchlist)
            print(f"Removed {ticker} from watchlist.")
        else:
            print(f"{ticker} not in watchlist.")
            
    elif cmd == "report":
        print(f"Generating report for {len(watchlist)} stocks...")
        results = []
        for ticker in watchlist:
            res = run_analysis(ticker)
            if res:
                results.append(res)
        
        print("\n=== Daily Stabilization Report ===")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        print("-" * 40)
        for res in results:
            status = "✅ 企稳" if res['stabilized'] else "❌ 未企稳"
            print(f"[{res['ticker']}] {status} | Price: {res['last_close']} (Date: {res['last_date']})")
            print(f"   Score: {res['score']}/100 | Range: {res['details']['price_range_10d']}, Vol: {res['details']['volume_vs_avg']}")
        print("-" * 40)

    else:
        # Legacy/Single ticker mode
        ticker = cmd
        res = run_analysis(ticker)
        if res:
            status = "Stabilized" if res['stabilized'] else "Not Stabilized"
            print(f"Analysis for {ticker}: {status} (Score: {res['score']})")
            print(f"Latest Close: {res['last_close']} (Date: {res['last_date']})")
            print(f"Details: {res['details']}")
        else:
            print(f"Failed to analyze {ticker}")


if __name__ == "__main__":
    main()



