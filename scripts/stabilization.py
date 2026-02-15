import pandas as pd
import numpy as np

def calculate_sma(data, window):
    return data.rolling(window=window).mean()

def is_stabilized(df, ticker):
    """
    Analyzes if a stock has stabilized based on recent K-line data.
    df: DataFrame with columns ['open', 'high', 'low', 'close', 'volume']
    """
    # Ensure columns are lowercase for robustness
    df.columns = [c.lower() for c in df.columns]
    
    if len(df) < 20:
        return {"status": "error", "message": "Not enough data for analysis (min 20 days)"}

    # 1. Price consolidation check (narrow range in last 5-10 days)
    last_10 = df.tail(10)
    price_range = (last_10['high'].max() - last_10['low'].min()) / last_10['low'].min()
    consolidated = price_range < 0.05  # Within 5% range
    
    # 2. Volume check (decreasing or low volume after trend)
    vol_sma = df['volume'].rolling(window=20).mean()
    last_vol_avg = vol_sma.iloc[-1]
    last_vol = df['volume'].tail(5).mean()
    low_volume = last_vol < last_vol_avg * 1.2 # Volume not spiking significantly
    
    # 3. Moving Average alignment
    df['sma5'] = calculate_sma(df['close'], 5)
    df['sma10'] = calculate_sma(df['close'], 10)
    ma_flattening = abs(df['sma5'].iloc[-1] - df['sma10'].iloc[-1]) / df['close'].iloc[-1] < 0.01

    # 4. Trend context (optional: was it recently in a downtrend?)
    # Simple check: is it above SMA20?
    df['sma20'] = calculate_sma(df['close'], 20)
    above_sma20 = df['close'].iloc[-1] >= df['sma20'].iloc[-1]

    # Combine signals
    score = 0
    if consolidated: score += 40
    if low_volume: score += 20
    if ma_flattening: score += 20
    if above_sma20: score += 20

    stabilized_flag = score >= 60

    # Extract latest date and price for reporting
    last_row = df.iloc[-1]
    last_date = str(df.index[-1]).split(' ')[0] # Handle datetime or string index
    last_close = float(last_row['close'])

    return {
        "ticker": ticker,
        "stabilized": bool(stabilized_flag),
        "score": int(score),
        "last_date": last_date,
        "last_close": last_close,
        "details": {
            "price_range_10d": f"{price_range:.2%}",
            "volume_vs_avg": f"{float(last_vol/last_vol_avg):.2f}x",
            "ma_diff": f"{float(abs(df['sma5'].iloc[-1] - df['sma10'].iloc[-1]) / df['close'].iloc[-1]):.2%}",
            "above_sma20": bool(above_sma20)
        }
    }



