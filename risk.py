from datetime import date

class RiskManager:
    def __init__(self, cfg):
        self.cfg = cfg
        self.day: date | None = None
        self.day_start_equity = 0.0
        self.halted = False

    def check_day(self, equity: float, now) -> bool:
        """Reset at the start of each UTC day. Halt if daily loss limit is breached."""
        if self.day != now.date():
            self.day = now.date()
            self.day_start_equity = equity
            self.halted = False
        if equity <= self.day_start_equity * (1 - self.cfg.max_daily_loss_pct):
            self.halted = True
        return not self.halted

    def position_size(self, equity: float, price: float) -> float:
        """Size so a stop-out loses roughly risk_per_trade of equity. No leverage."""
        risk_amount = equity * self.cfg.risk_per_trade
        stop_distance = price * self.cfg.stop_loss_pct
        qty = risk_amount / stop_distance
        max_qty = equity / price * 0.95  # keep a small cash buffer for fees
        return min(qty, max_qty)

    def stop_price(self, entry: float) -> float:
        return entry * (1 - self.cfg.stop_loss_pct)
