import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    exchange_id: str = os.getenv("EXCHANGE_ID", "binance")
    symbol: str = os.getenv("SYMBOL", "BTC/USDT")
    timeframe: str = os.getenv("TIMEFRAME", "1h")
    fast_ma: int = int(os.getenv("FAST_MA", 20))
    slow_ma: int = int(os.getenv("SLOW_MA", 50))
    starting_cash: float = float(os.getenv("STARTING_CASH", 10000))
    risk_per_trade: float = float(os.getenv("RISK_PER_TRADE", 0.01))
    stop_loss_pct: float = float(os.getenv("STOP_LOSS_PCT", 0.02))
    max_daily_loss_pct: float = float(os.getenv("MAX_DAILY_LOSS_PCT", 0.05))
    poll_seconds: int = int(os.getenv("POLL_SECONDS", 60))
    paper_mode: bool = os.getenv("PAPER_MODE", "true").lower() == "true"
    fee_rate: float = 0.001  # 0.1% per trade, typical spot taker fee

CFG = Config()
