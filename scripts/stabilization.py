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
    
    if len(df) < 30:
        return {"status": "error", "message": f"Not enough data for analysis (min 30 days, got {len(df)})"}

    # 1. Price consolidation check (narrow range in last 10 days)
    last_10 = df.tail(10)
    price_range = (last_10['high'].max() - last_10['low'].min()) / last_10['low'].min()
    consolidated = price_range < 0.05  # Within 5% range
    
    # 2. Volume check (decreasing or low volume after trend)
    vol_sma = df['volume'].rolling(window=20).mean()
    last_vol_avg = vol_sma.iloc[-1]
    last_vol = df['volume'].tail(5).mean()
    low_volume = last_vol < last_vol_avg * 1.5 # Volume not spiking excessively
    
    # 3. Moving Average alignment
    df['sma5'] = calculate_sma(df['close'], 5)
    df['sma10'] = calculate_sma(df['close'], 10)
    ma_flattening = abs(df['sma5'].iloc[-1] - df['sma10'].iloc[-1]) / df['close'].iloc[-1] < 0.01

    # 4. Trend context
    df['sma20'] = calculate_sma(df['close'], 20)
    above_sma20 = df['close'].iloc[-1] >= df['sma20'].iloc[-1]

    # 5. Trading Pattern Detection (New)
    has_bullish_pattern = False
    pattern_name = "None"
    try:
        from tradingpatterns import get_recent_bullish_patterns
        # Check for confirmed patterns with at least strength 2 in the last 3 days
        patterns = get_recent_bullish_patterns(df, n=3, enable_confirmation=True, min_strength=2)
        if patterns:
            has_bullish_pattern = True
            pattern_name = patterns[-1]['pattern']
    except Exception as e:
        print(f"Warning: tradingpatterns check failed: {e}")

    # Combine signals
    score = 0
    if consolidated: score += 30
    if low_volume: score += 15
    if ma_flattening: score += 15
    if above_sma20: score += 10
    if has_bullish_pattern: score += 30

    stabilized_flag = score >= 60

    # Extract latest date and price for reporting
    last_row = df.iloc[-1]
    last_date = str(df.index[-1]).split(' ')[0]
    last_close = float(last_row['close'])

    return {
        "ticker": ticker,
        "stabilized": bool(stabilized_flag),
        "score": int(score),
        "last_date": last_date,
        "last_close": round(last_close, 2),
        "details": {
            "price_range_10d": f"{price_range:.2%}",
            "volume_vs_avg": f"{float(last_vol/last_vol_avg):.2f}x",
            "ma_diff": f"{float(abs(df['sma5'].iloc[-1] - df['sma10'].iloc[-1]) / df['close'].iloc[-1]):.2%}",
            "above_sma20": bool(above_sma20),
            "bullish_pattern": pattern_name
        }
    }



