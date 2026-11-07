import pandas as pd

def add_signals(df: pd.DataFrame, fast: int, slow: int) -> pd.DataFrame:
    """
    signal = 1 on the candle where fast MA crosses above slow MA
    signal = -1 on the candle where fast MA crosses below slow MA
    Always act on a CLOSED candle (the row before the last one in live mode).
    """
    df = df.copy()
    df["fast"] = df["close"].rolling(fast).mean()
    df["slow"] = df["close"].rolling(slow).mean()
    prev_fast = df["fast"].shift(1)
    prev_slow = df["slow"].shift(1)

    df["signal"] = 0
    df.loc[(prev_fast <= prev_slow) & (df["fast"] > df["slow"]), "signal"] = 1
    df.loc[(prev_fast >= prev_slow) & (df["fast"] < df["slow"]), "signal"] = -1
    return df
