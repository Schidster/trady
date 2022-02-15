from cmath import nan
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from .bot import Bot
from .rules import *
   
def test_data_source(filename, drop_cols):
    data = pd.read_csv(filename).drop(drop_cols, axis=1)
    for i in range(len(data)):
        try:
            candle = list(data.iloc[i])
        except IndexError:
            raise StopIteration
        candle[0] = datetime.strptime(candle[0], '%Y-%m-%d %H:%S:%M%z')
        yield candle

def moving(list, n):
    # Moving average is average of PAST n intervals.
    mov_avgs = [nan] * n
    n_windows = len(list) - n
    for i in range(n_windows):
        mov_avg = sum(list[i:i+n])/n
        mov_avgs.append(mov_avg)
    return mov_avgs

def plotCrossovers():
    data = pd.read_csv('<path-to-file>/TATASTEEL.csv')
    fast_moving = moving(list(data['close']), 7)
    slow_moving = moving(list(data['close']), 20)
    x = data['timestamp']

    plt.figure(figsize=(40, 20), dpi=80)
    plt.plot(x, fast_moving)
    plt.plot(x, slow_moving)
    plt.legend(['fast moving (7)', 'slow moving (20)'])
    plt.show()

if __name__ == "__main__":
    buy_rules = [
        is_close_greater_than_20_sma,
        is_close_greater_than_s1,
    ]
    sell_rules = [
        is_close_lesser_than_20_sma,
        is_close_lesser_than_s1,
    ]

    bot = Bot(test_data_source('<path-to-file>/TATASTEEL.csv', ['index']), buy_rules, sell_rules, 1, 0.5)

    bot.run()

    plotCrossovers()