import numpy as np
import ccxt
from datetime import datetime
import plotly.graph_objects as go

def get_ma_va(open_price, close_price, volume, ma, volume_avarage):
    start = 0   # стартер, если среднее значение цены за 20 часов а обьема за 25, то нет смысла учитывать первые 24 часа потому что не будет данных по обьему
    if ma > volume_avarage : 
        start = ma
    else :
        start = volume_avarage
    ma_arr = []
    va_arr = []

    for i in range(start, len(close_price)): # просто arrays со средними значениями
        ma_arr.append( (np.mean(close_price[i-ma:i]) + np.mean(open_price[i-ma:i]))/2 )
        va_arr.append(np.mean(volume[i-ma:i]))

    return start, ma_arr, va_arr
        
  

def get_crypto_data(trading_pair , time_interval, ma, va):
    binance = ccxt.binance()
    candles = binance.fetch_ohlcv(trading_pair, time_interval)
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume_data = []

    for candle in candles:
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
        open_data.append(candle[1])
        high_data.append(candle[2])
        low_data.append(candle[3])
        close_data.append(candle[4])
        volume_data.append(candle[5])
    
    start, ma_data , _ = get_ma_va(open_data, close_data, volume_data, ma, va)
    start = -100
    open_data, close_data, high_data, low_data, dates, ma_data = open_data[start:], close_data[start:], high_data[start:], low_data[start:], dates[start:], ma_data[start:]
    fig = go.Figure(data = [go.Candlestick(x = dates,
                      open = open_data, high = high_data,
                      low = low_data, close = close_data),
                      go.Scatter(x = dates, y = ma_data, line=dict(color='orange', width=1) ) ])
    fig.update_layout(xaxis_rangeslider_visible=False)
    img = fig.to_image(format="png", engine="kaleido")
    return open_data, close_data, ma_data, img 


def buy_or_sell(eth):
    btc_open, btc_close, btc_ma, btc_img = get_crypto_data('BTC/USDT', '1h', 90, 0)
    eth_open, eth_close, eth_ma, eth_img = get_crypto_data('ETH/USDT', '1d', 10, 0)
    btc_action, eth_action = '', ''
    btc_stop, eth_stop = 0, 0
    if  btc_ma[-2]<btc_close[-2] and btc_ma[-2]>btc_open[-2] and btc_close[-1]>btc_ma[-1]:
        btc_action = 'Buy or hold'
        btc_stop = 0.99*btc_close[-1]

    elif btc_ma[-2]>btc_close[-2] and btc_ma[-2]<btc_open[-2] and btc_close[-1]<btc_ma[-1]:
        btc_action = 'Sell or hold'
        btc_stop = 1.01*btc_close[-1]
    print('BTC: working')
    if eth : 
        if  eth_ma[-2]<eth_close[-2] and eth_ma[-2]>eth_open[-2] and eth_close[-1]>eth_ma[-1]:
            eth_action = 'Buy or hold'
            eth_stop = 0.995*eth_close[-1]

        elif eth_ma[-2]>eth_close[-2] and eth_ma[-2]<eth_open[-2] and eth_close[-1]<eth_ma[-1]:
            eth_action = 'Sell or hold'
            eth_stop = 1.005*eth_close[-1] 
        print('ETH: working')
    
    return btc_action, btc_stop, btc_img,  eth_action, eth_stop, eth_img

            
