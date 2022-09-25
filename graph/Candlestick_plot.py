import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# K線圖
def Candlestick_plot(stock_trend, stock, trading_day):

    data = stock_trend.copy()
    data = data.query(f"stock_name == '{stock}' or stock_id == '{stock}'", engine='python').sort_values(
        by='Date').iloc[-trading_day:]

    # 版面布置
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03,
                        row_width=[0.2, 0.7])

    # k棒圖
    fig.add_trace(go.Candlestick(x=data['Date'],
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 increasing_line_color='red',
                                 decreasing_line_color='green',
                                 showlegend=False),
                  row=1, col=1)

    # 均線
    ema_5 = go.Scatter(x=data['Date'], y=data['5ma'],
                       mode='lines', name='5ma', marker=dict(color='#FF5809'))
    ema_10 = go.Scatter(x=data['Date'], y=data['10ma'],
                        mode='lines', name='10ma', marker=dict(color='#C6A300'))
    ema_20 = go.Scatter(x=data['Date'], y=data['20ma'],
                        mode='lines', name='20ma', marker=dict(color='#0080FF'))
    ema_60 = go.Scatter(x=data['Date'], y=data['60ma'],
                        mode='lines', name='60ma', marker=dict(color='#6F00D2'))
    ema_100 = go.Scatter(x=data['Date'], y=data['100ma'],
                         mode='lines', name='100ma', marker=dict(color='#3C3C3C'))

    # 布林通道
    upper_band_5 = go.Scatter(x=data['Date'], y=data['upper_band_5'],
                              mode='lines', name='upper_band_5', marker=dict(color='#7B7B7B'))
    lower_band_5 = go.Scatter(x=data['Date'], y=data['lower_band_5'],
                              mode='lines', name='lower_band_5', marker=dict(color='#7B7B7B'))
    upper_band_10 = go.Scatter(x=data['Date'], y=data['upper_band_10'],
                               mode='lines', name='upper_band_10', marker=dict(color='#7B7B7B'))
    lower_band_10 = go.Scatter(x=data['Date'], y=data['lower_band_10'],
                               mode='lines', name='lower_band_10', marker=dict(color='#7B7B7B'))
    upper_band_20 = go.Scatter(x=data['Date'], y=data['upper_band_20'],
                               mode='lines', name='upper_band_20', marker=dict(color='#7B7B7B'))
    lower_band_20 = go.Scatter(x=data['Date'], y=data['lower_band_20'],
                               mode='lines', name='lower_band_20', marker=dict(color='#7B7B7B'))

    # 添加線圖
    fig.add_traces([ema_5, ema_10, ema_20, ema_60, ema_100, upper_band_5,
                    lower_band_5, upper_band_10, lower_band_10, upper_band_20, lower_band_20])

    # 成交量
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], showlegend=False, marker=dict(
        color='#930000')), row=2, col=1)

    # 特定線圖只顯示圖示
    fig.for_each_trace(lambda trace: trace.update(visible="legendonly")
                       if trace.name in ['10ma', '60ma', '100ma', 'upper_band_5', 'lower_band_5', 'upper_band_10', 'lower_band_10', 'upper_band_20', 'lower_band_20'] else ())

    # 刪除六日
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    # 隱藏滑動
    fig.update(layout_xaxis_rangeslider_visible=False)
    # 版面設置
    fig.update_layout(height=400,
                      title_x=0.43, title_y=0.93,
                      title_text=(
                          f'{data.stock_id.unique()[0]} {data.stock_name.unique()[0]}'),
                      title_font=dict(size=18, color='#8a8d93',
                                      family="Lato, sans-serif"),
                      margin=dict(l=30, r=20, t=10, b=30),
                      paper_bgcolor='rgba(0,0,0,0)'
                      )

    return fig
