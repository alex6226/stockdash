# 資料處理
import pandas as pd
import numpy as np
import re
# 資料庫
from sqlalchemy import create_engine
# 儀錶板
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output
# 圖表
from graph.bar_plot import bar_plot
from graph.Candlestick_plot import Candlestick_plot
from graph.histogram_plot import histogram_plot
from graph.quadrant_plot import quadrant_plot
from graph.table_plot import table_plot
from graph.treemap_plot import treemap_plot

#　資料讀取
stock_trend_engine = create_engine(
    "mysql+pymysql://root:alex50703@127.0.0.1:3306/stockdash?charset=utf8mb4")
stock_trend = pd.read_sql('stock_trend', stock_trend_engine)

stock_ma_slope_engine = create_engine(
    "mysql+pymysql://root:alex50703@127.0.0.1:3306/stockdash?charset=utf8mb4")
stock_ma_slope = pd.read_sql('stock_ma_slope', stock_ma_slope_engine)

stock_roi_engine = create_engine(
    "mysql+pymysql://root:alex50703@127.0.0.1:3306/stockdash?charset=utf8mb4")
stock_roi = pd.read_sql('stock_roi', stock_roi_engine)

app = dash.Dash(__name__, external_stylesheets=['app\assets\css.css'])
app.title = '股市觀測站'

# dash布局
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='table', figure=table_plot(stock_roi))
    ]),

    html.Div([
        dcc.Input(id="input_stock", type="text", placeholder="輸入股票名稱或代碼", debounce=True, value='台積電',
                  style={'marginLeft': '50px', 'marginRight': '10px'}),
        dcc.Input(id="input_day", type="text",
                  placeholder="近N個交易日", debounce=True, value=90, style={'marginRight': '10px'}),

        dcc.Graph(id='Candlestick'),
    ]),
    html.Div([
        html.Div([dcc.Dropdown(['近1日', '近5日', '近10日', '近20日', '近60日'],
                               value='近1日', id='day2')
                  ], style={'marginLeft': '57%', 'marginRight': '35%'
                            }),
        html.Div([
            dcc.Graph(id='quadrant', figure=quadrant_plot(
                stock_ma_slope), style={'display': 'inline-block', 'width': '50%'}),
            dcc.Graph(id='histogram', style={
                'display': 'inline-block', 'width': '50%'})
        ])
    ]),
    html.Div([
        html.Div([

            dcc.Dropdown(['水泥工業', '食品工業', '塑膠工業', '化學工業', '汽車工業', '紡織纖維', '貿易百貨業', '其他業',
                          '建材營造業', '電子零組件業', '電機機械', '生技醫療業', '電器電纜', '玻璃陶瓷', '造紙工業', '鋼鐵工業',
                          '橡膠工業', '航運業', '電腦及週邊設備業', '半導體業', '其他電子業', '通信網路業', '光電業',
                          '電子通路業', '資訊服務業', '油電燃氣業', '觀光事業', '金融保險業'],
                         value='航運業', id='group', style={'display': 'inline-block', 'width': '150px'}),
            dcc.Dropdown(['近1日', '近5日', '近10日', '近20日', '近60日'],
                         value='近1日', id='day3', style={'display': 'inline-block', 'width': '80px'})
        ], style={'marginLeft': '57%'}),
        html.Div([
            dcc.Graph(id='bar', figure=bar_plot(stock_roi), style={
                      'display': 'inline-block', 'width': '50%'}),
            dcc.Graph(id='treemap', style={
                      'display': 'inline-block', 'width': '50%'})
        ])

    ])

], style={'backgroundColor': '#F2F2F2'})


@app.callback([Output('Candlestick', 'figure'), Output('histogram', 'figure'), Output('treemap', 'figure')],
              [Input('input_stock', 'value'),
              Input('input_day', 'value'),
              Input('day2', 'value'),
              Input('group', 'value'),
              Input('day3', 'value')])
def update_outputs(input_stock, input_day, day2, group, day3):

    # k線圖
    Candlestick = Candlestick_plot(stock_trend, input_stock, int(input_day))
    # 多空直方圖
    day2 = int(re.sub(r'[近日]', '', day2))
    histogram = histogram_plot(stock_roi, day2)
    # 類股交易量樹狀圖
    day3 = int(re.sub(r'[近日]', '', day3))
    treemap = treemap_plot(stock_roi, group, day3)

    return Candlestick, histogram, treemap


if __name__ == '__main__':
    app.run_server(debug=False)
