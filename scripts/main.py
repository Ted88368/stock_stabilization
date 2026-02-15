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
    default_watchlist = {"hk": [], "us": [], "as": []}
    if os.path.exists(WATCHLIST_PATH):
        try:
            with open(WATCHLIST_PATH, 'r') as f:
                data = json.load(f)
                if isinstance(data, list): # Migration logic
                    new_data = default_watchlist.copy()
                    for ticker in data:
                        market = get_market_key(ticker)
                        new_data[market].append(ticker)
                    return new_data
                return data
        except Exception:
            return default_watchlist
    return default_watchlist

def save_watchlist(watchlist):
    with open(WATCHLIST_PATH, 'w') as f:
        json.dump(watchlist, f, indent=4)

def get_market_key(ticker):
    if ticker.startswith('hk.'): return 'hk'
    if ticker.startswith('us.'): return 'us'
    if ticker.startswith('sh.') or ticker.startswith('sz.'): return 'as'
    return 'us' # Default

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
        print("  uv run scripts/main.py add <ticker>         - Add to watchlist")
        print("  uv run scripts/main.py remove <ticker>      - Remove from watchlist")
        print("  uv run scripts/main.py report [market]      - Run report (hk/us/as/all)")
        print("  uv run scripts/main.py <ticker>             - Quick single analysis")
        return

    cmd = sys.argv[1]
    watchlist = load_watchlist()

    if cmd == "add" and len(sys.argv) > 2:
        ticker = sys.argv[2]
        market = get_market_key(ticker)
        if ticker not in watchlist[market]:
            watchlist[market].append(ticker)
            save_watchlist(watchlist)
            print(f"Added {ticker} to {market} watchlist.")
        else:
            print(f"{ticker} already in {market} watchlist.")
    
    elif cmd == "remove" and len(sys.argv) > 2:
        ticker = sys.argv[2]
        market = get_market_key(ticker)
        if market in watchlist and ticker in watchlist[market]:
            watchlist[market].remove(ticker)
            save_watchlist(watchlist)
            print(f"Removed {ticker} from {market} watchlist.")
        else:
            print(f"{ticker} not in {market} watchlist.")
            
    elif cmd == "report":
        target_market = sys.argv[2] if len(sys.argv) > 2 else "all"
        
        markets_to_run = [target_market] if target_market in watchlist else watchlist.keys()
        
        all_results = {}
        for m in markets_to_run:
            print(f"Generating report for {m} market ({len(watchlist[m])} stocks)...")
            market_results = []
            for ticker in watchlist[m]:
                res = run_analysis(ticker)
                if res:
                    market_results.append(res)
            all_results[m] = market_results
        
        print("\n=== Market Stabilization Report ===")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        
        for m, results in all_results.items():
            if not results: continue
            print(f"\n--- {m.upper()} Market ---")
            for res in results:
                status = "✅ 企稳" if res['stabilized'] else "❌ 未企稳"
                print(f"[{res['ticker']}] {status} | Price: {res['last_close']} (Date: {res['last_date']})")
                print(f"   Score: {res['score']}/100 | Range: {res['details']['price_range_10d']}, Vol: {res['details']['volume_vs_avg']}, Pattern: {res['details']['bullish_pattern']}")
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



