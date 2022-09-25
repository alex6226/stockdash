import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#　股票交易量表格圖
def table_plot(stock_roi):

    data = stock_roi.sort_values(by='volume', ascending=False)
    stock_name = data['stock_name']
    stock_id = data['stock_id']
    Volumns = data['volume']
    price = data['close']
    roi = data['roi_1']
    category = data['group']
    fill_color = [['#E5ECF6']*906, ['#E5ECF6']*906, ['#E5ECF6']*906, ['#E5ECF6']*906,
                  ['#E5ECF6']*906, np.where(roi >= 0, '#FF2D2D', '#02DF82'), ['#E5ECF6']*906]

    fig = go.Figure(data=[go.Table(columnwidth=[30, 70, 70, 70, 70, 70, 70],
                    header=dict(values=['<b>名次<b>', '<b>股票<b>', '<b>代碼<b>', '<b>交易量<b>', '<b>收盤價<b>', '<b>漲跌幅<b>', '<b>產業<b>'],
                    line_color='darkslategray', fill_color='lightskyblue', align='left'),
                    cells=dict(values=[np.arange(1, data.shape[0]+1, 1), stock_name, stock_id, Volumns, price, roi, category],
                    line_color='darkslategray',
                    fill_color=fill_color,
                    align='left'
                               ))
    ])
    fig.update_layout(height=281.5,
                      margin=dict(l=30, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)'
                      )

    return fig
