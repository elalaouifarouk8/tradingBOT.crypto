import pandas as pd
from config import CFG
from data import get_ohlcv
from strategy import add_signals
from risk import RiskManager
from broker import PaperBroker

def backtest(limit: int = 1000):
    df = add_signals(get_ohlcv(CFG.exchange_id, CFG.symbol, CFG.timeframe, limit),
                     CFG.fast_ma, CFG.slow_ma)
    broker = PaperBroker(CFG.starting_cash, CFG.fee_rate)
    risk = RiskManager(CFG)
    stop = None
    equity_curve, exits = [], 0

    for i in range(1, len(df)):
        row, prev = df.iloc[i], df.iloc[i - 1]
        price = float(row["close"])
        eq = broker.equity(price)

        # Stop-loss (checked on close, a simplification)
        if broker.qty > 0 and stop is not None and price <= stop:
            broker.sell_all(price); stop = None; exits += 1

        # Act on previous closed candle's signal
        if prev["signal"] == 1 and broker.qty == 0:
            qty = risk.position_size(eq, price)
            broker.buy(price, qty)
            stop = risk.stop_price(price)
        elif prev["signal"] == -1 and broker.qty > 0:
            broker.sell_all(price); stop = None; exits += 1

        equity_curve.append(broker.equity(price))

    eq = pd.Series(equity_curve)
    total_return = (eq.iloc[-1] / CFG.starting_cash - 1) * 100
    max_dd = ((eq / eq.cummax()) - 1).min() * 100
    buy_hold = (df["close"].iloc[-1] / df["close"].iloc[0] - 1) * 100

    print(f"Symbol:            {CFG.symbol} ({CFG.timeframe}, {len(df)} candles)")
    print(f"Strategy return:   {total_return:.2f}%")
    print(f"Buy & hold return: {buy_hold:.2f}%")
    print(f"Max drawdown:      {max_dd:.2f}%")
    print(f"Exits taken:       {exits}")
    print(f"Final equity:      {eq.iloc[-1]:.2f}")

if __name__ == "__main__":
    backtest()
