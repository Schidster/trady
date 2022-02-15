from functools import reduce
import pandas as pd

# This bot deals with only one asset and buys/sells/holds only 1 stock at a time.

class Bot:
    def __init__(self, data_source, buy_rules, sell_rules, target, stoploss):
        self.total_profit = 0
        self.portfolio = list() # List of dictionary of quantity and average price
        self.data = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        self.counter = 0
        # assuming data_source yields tuple/list of (timestamp, open, high, low, close, volume) or candles
        self.data_source = iter(data_source)
        self.buy_rules = buy_rules
        self.sell_rules = sell_rules
        self.target = target
        self.stoploss = stoploss
    
    def run(self):
        print("Bot starting...")
        t_day = None
        while True:
            try:
                candle = next(self.data_source)
                self.data.loc[self.counter] = candle
           
                now = self.data.iloc[-1]['timestamp']

                if not t_day: t_day = now.date() # initialization
                if now.date() > t_day: # square off at end of the day, complexity due to simulated time.
                    self.square_off()
                    t_day = now.date()

                if self.is_market_closed(now): continue

                self.sell_if_targets_met()
                self.sell_if_stoploss_met()

                is_portflio_empty = not bool(self.portfolio)
                should_buy = is_portflio_empty & self.reduce_rules(self.buy_rules)
                should_sell = (not is_portflio_empty) & self.reduce_rules(self.sell_rules)

                if should_buy:
                    print(f"Candle {self.counter}: Buying 1 stock at {self.data.iloc[-1]['close']}")
                    self.portfolio.append({
                        'quantity': 1,
                        'avg_price': self.data.iloc[-1]['close'],
                    })
                
                if should_sell:
                    self.sell()
        
                self.counter += 1
            except StopIteration:
                print("Shutting Bot down: Data source has closed.")
                print(f"Bot generated a total profit of {self.total_profit}")
                break
    
    def reduce_rules(self, rules):
        if len(rules) == 0: return False
        reduce_func = lambda rule, another_rule: rule(self.data) & another_rule(self.data)
        return reduce(reduce_func, rules)

    def is_market_closed(self, now):
        open_time = pd.Timestamp('9:25', tz='+05:30')   # 9:25 am
        close_time = pd.Timestamp('3:15', tz='+05:30') # 3:15 pm

        return (now < open_time) & (now > close_time)


    def square_off(self):
        if self.portfolio:
            print(f"Candle {self.counter}: Squaring off at end of the day.")
            print(f"Candle {self.counter}: Selling {len(self.portfolio)} at {self.data.iloc[-2]['close']}")
            print(f"Candle {self.counter}: Generated profit of {self.calc_current_profit_loss()}")
            self.total_profit += self.calc_current_profit_loss()
            self.portfolio.clear()

    def calc_current_profit_loss(self):
        price = self.data['close'].iloc[-1]
        profit = 0
        for asset in self.portfolio:
            profit += (asset['quantity'] * (price - asset['avg_price']))
        return profit

    def sell(self):
        print(f"Candle {self.counter}: Selling {len(self.portfolio)} at {self.data.iloc[-1]['close']}")
        print(f"Candle {self.counter}: Generated profit of {self.calc_current_profit_loss()}")
        self.total_profit += self.calc_current_profit_loss()
        self.portfolio.clear()

    def sell_if_targets_met(self):
        if self.portfolio:
            price = self.portfolio[0]['avg_price']
            if ((self.data.iloc[-1]['close'] - price)/price)*100 >= self.target:
                print(f"Candle {self.counter}: Target Acheived")
                self.sell()

    def sell_if_stoploss_met(self):
        if self.portfolio:
            price = self.portfolio[0]['avg_price']
            if ((price - self.data.iloc[-1]['close'])/price)*100 >= self.stoploss:
                print(f"Candle {self.counter}: Stoploss Triggered")
                self.sell()
