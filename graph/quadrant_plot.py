import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 均線趨勢象限圖
def quadrant_plot(stock_ma_slope):

    data = stock_ma_slope.copy()
    fig = go.Figure()

    for x, y in zip(['5ma_slope_5']*3, ['60ma_slope_5', '20ma_slope_5', '10ma_slope_5']):

        fig.update_traces(visible=False)
        scatter = px.scatter(data, x=x, y=y,
                             hover_data=['stock_id', 'stock_name'], color='group', size='volume')
        fig.add_traces(
            list(scatter.select_traces())
        )

    fig.add_vline(x=0, line_width=1.5, line_color="black", opacity=0.5)
    fig.add_hline(y=0, line_width=1.5, line_color="black", opacity=0.5)
    fig.update_xaxes(range=[-1.5, 1.5])
    fig.update_yaxes(range=[-1.5, 1.5])

    updatemenus = [
        dict(
            active=0,
            x=0.25,
            y=1.1,
            buttons=list([
                dict(label="5ma-10ma",
                     method="update",
                     args=[{"visible": [True if i > 56 else False for i in range(84)]}]),
                dict(label="5ma-20ma",
                     method="update",
                     args=[{"visible": [True if i >= 28 and i < 56 else False for i in range(84)]}]),
                dict(label="5ma-60ma",
                     method="update",
                     args=[{"visible": [True if i < 28 else False for i in range(84)]}])
            ]))]

    fig.update_layout(height=500,
                      title_x=0.4, title_y=0.98,
                      title_text='均線趨勢定位',
                      title_font=dict(size=25, color='#8a8d93',
                                      family="Lato, sans-serif"),
                      updatemenus=updatemenus,
                      margin=dict(l=0, r=0, t=0, b=0),
                      paper_bgcolor='rgba(0,0,0,0)'
                      )

    return fig
