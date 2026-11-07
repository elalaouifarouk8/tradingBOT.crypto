import ccxt
import pandas as pd

def get_ohlcv(exchange_id: str, symbol: str, timeframe: str, limit: int = 300) -> pd.DataFrame:
    """Fetch public candle data. No API keys needed."""
    ex = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    raw = ex.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=["ts", "open", "high", "low", "close", "volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")
    return df
