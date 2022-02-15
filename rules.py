def is_close_greater_than_s1(data):
    if len(data) < 2: return False
    latest = data.iloc[-1]
    
    prev_day = data.iloc[-2]
    # counter = 1
    # while (counter <= len(data)) & (latest['timestamp'].date() <= prev_day['timestamp'].date()):
    #     prev_day = data.iloc[-counter]
    #     counter += 1

    p = (prev_day['high'] + prev_day['low'] + prev_day['close']) / 3 # 
    s1 = (p * 2) - prev_day['high']

    return latest['close'] > s1

def is_close_greater_than_20_sma(data):
    if len(data) < 21: return False
    mov_avg = sum(data['close'][-21:-1])/20
    return data['close'].iloc[-1] > mov_avg
   
def is_close_lesser_than_s1(data):
    if len(data) < 2: return False
    latest = data.iloc[-1]

    prev_day = data.iloc[-2]
    # counter = 1
    # while (counter <= len(data)) & (latest['timestamp'].date() <= prev_day['timestamp'].date()):
    #     prev_day = data.iloc[-counter]
    #     counter += 1

    p = (prev_day['high'] + prev_day['low'] + prev_day['close']) / 3 
    s1 = (p * 2) - prev_day['high']

    return latest['close'] < s1

def is_close_lesser_than_20_sma(data):
    if len(data) < 21: return False
    mov_avg = sum(data['close'][-21:-1])/20
    return data['close'].iloc[-1] < mov_avg