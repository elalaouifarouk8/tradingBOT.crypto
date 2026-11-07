from state import write_state

# inside the main loop, after the trading logic runs:
write_state({
    "mode": "PAPER" if config.PAPER_MODE else "LIVE",
    "symbol": config.SYMBOL,
    "timeframe": config.TIMEFRAME,
    "last_price": last_price,
    "equity": broker.equity(),
    "cash": broker.cash,
    "position": broker.position_size,   # e.g. 0.05 BTC
    "entry_price": broker.entry_price,
    "daily_pnl_pct": risk.daily_pnl_pct(),
    "trades": broker.trades[-50:],      # last 50 trades
    "status": "running",
})
