from datetime import datetime
import alpaca_trade_api as tradeapi

api = tradeapi.REST()


class Stock:
    def __init__(self, sign):
        self.sign = sign
        self.avg_price = 0
        self.quantity = 0
        self.order_history = []

        self.position = api.get_position(sign)

    def buy(self, quantity, price):
        prev_avg_price = self.avg_price * self.quantity
        self.quantity += quantity
        self.avg_price = (prev_avg_price + price) / self.quantity
        self.order_history.append(("buy", datetime.now(), quantity, price))

    def sell(self, quantity, price):
        self.quantity -= quantity
        self.order_history.append(("sell", datetime.now(), quantity, price))

    def get_return(self, price, today=False):
        if not today:
            return price - self.avg_price
        return price

