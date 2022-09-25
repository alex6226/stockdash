import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#　多空直方圖
def histogram_plot(stock_roi, day):

    data = stock_roi.copy()
    fig = px.histogram(data[data[f'roi_{day}'] != 0], x=f"roi_{day}", color=f"state_{day}", color_discrete_map={
                       'up': '#FF2D2D', 'down': '#02DF82'}, nbins=None)
    fig.update_traces(marker_line_width=1, marker_line_color="black")
    range_dict = dict({1: 10, 5: 20, 10: 30, 20: 40, 60: 100})
    fig.update_xaxes(range=[-range_dict[day], range_dict[day]])
    fig.update_layout(height=500,
                      title_x=0.48, title_y=0.98,
                      title_text=f'近{day}日多空情勢',
                      title_font=dict(size=25, color='#8a8d93',
                                      family="Lato, sans-serif"),
                      margin=dict(l=0, r=0, t=40, b=0),
                      paper_bgcolor='rgba(0,0,0,0)'
                      )

    return fig
