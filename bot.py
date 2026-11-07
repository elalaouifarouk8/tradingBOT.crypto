import os
import time
import logging
from config import CFG
from data import get_ohlcv
from strategy import add_signals
from risk import RiskManager
from broker import PaperBroker, LiveBroker
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
log = logging.getLogger("bot")

def make_broker():
    if CFG.paper_mode:
        return PaperBroker(CFG.starting_cash, CFG.fee_rate)
    return LiveBroker(CFG.exchange_id, os.environ["API_KEY"],
                      os.environ["API_SECRET"], CFG.symbol)

def run():
    broker = make_broker()
    risk = RiskManager(CFG)
    stop = None
    last_signal_ts = None
    log.info("Starting bot | paper=%s | %s %s", CFG.paper_mode, CFG.symbol, CFG.timeframe)

    while True:
        try:
            now = datetime.now(timezone.utc)
            df = add_signals(get_ohlcv(CFG.exchange_id, CFG.symbol, CFG.timeframe),
                             CFG.fast_ma, CFG.slow_ma)
            price = float(df.iloc[-1]["close"])
            closed = df.iloc[-2]  # last fully closed candle
            equity = broker.equity(price)

            if not risk.check_day(equity, now):
                log.warning("Daily loss limit hit. Trading halted until next UTC day.")
                time.sleep(CFG.poll_seconds)
                continue

            # Stop-loss check
            if broker.qty > 0 and stop is not None and price <= stop:
                broker.sell_all(price)
                log.info("STOP-LOSS exit at %.2f", price)
                stop = None

            # Act once per closed candle
            if closed["ts"] != last_signal_ts:
                if closed["signal"] == 1 and broker.qty == 0:
                    qty = risk.position_size(equity, price)
                    broker.buy(price, qty)
                    stop = risk.stop_price(price)
                    log.info("BUY %.6f at %.2f | stop %.2f", qty, price, stop)
                    last_signal_ts = closed["ts"]
                elif closed["signal"] == -1 and broker.qty > 0:
                    broker.sell_all(price)
                    stop = None
                    log.info("SELL (cross down) at %.2f", price)
                    last_signal_ts = closed["ts"]

            log.info("price=%.2f equity=%.2f qty=%.6f", price, equity, broker.qty)
        except Exception as e:
            log.exception("Loop error: %s", e)

        time.sleep(CFG.poll_seconds)

if __name__ == "__main__":
    run()
