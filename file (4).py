import ccxt

class PaperBroker:
    """Simulated broker. Holds one position at a time."""
    def __init__(self, cash: float, fee: float):
        self.cash = cash
        self.qty = 0.0
        self.fee = fee

    def equity(self, price: float) -> float:
        return self.cash + self.qty * price

    def buy(self, price: float, qty: float) -> float:
        cost = qty * price
        if cost * (1 + self.fee) > self.cash:
            qty = self.cash / (price * (1 + self.fee))
            cost = qty * price
        self.cash -= cost * (1 + self.fee)
        self.qty += qty
        return qty

    def sell_all(self, price: float) -> float:
        if self.qty <= 0:
            return 0.0
        proceeds = self.qty * price
        self.cash += proceeds * (1 - self.fee)
        sold, self.qty = self.qty, 0.0
        return sold


class LiveBroker:
    """Real orders via ccxt. Only used when PAPER_MODE=false."""
    def __init__(self, exchange_id: str, key: str, secret: str, symbol: str):
        self.ex = getattr(ccxt, exchange_id)({
            "apiKey": key, "secret": secret, "enableRateLimit": True,
        })
        self.symbol = symbol
        self.base, self.quote = symbol.split("/")

    def _free(self, currency: str) -> float:
        return float(self.ex.fetch_balance().get(currency, {}).get("free", 0.0) or 0.0)

    @property
    def qty(self) -> float:
        return self._free(self.base)

    def equity(self, price: float) -> float:
        return self._free(self.quote) + self.qty * price

    def buy(self, price: float, qty: float):
        # Market orders for simplicity. Limit orders give better fills.
        return self.ex.create_market_buy_order(self.symbol, qty)

    def sell_all(self, price: float):
        q = self.qty
        if q > 0:
            self.ex.create_market_sell_order(self.symbol, q)
        return q
