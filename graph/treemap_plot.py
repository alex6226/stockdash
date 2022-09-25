
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 類股交易量樹狀圖
def treemap_plot(stock_roi, group, day):

    fig = go.Figure()
    data = stock_roi.query(f"group=='{group}'")
    labels = data['stock_name']
    parents = [f'{group}']*30
    values = data['volume']
    text = [f'{t}%' for t in data[f'roi_{day}']]
    marker_colors = pd.cut(data[f'roi_{day}'], bins=[-100, -30, -7, -4, -1, 1, 4, 7, 30, 100], labels=[
        '#003E3E', '#139794', '#75ACA2', '#BFCFB8', '#EFE9C7', '#E9C9B6', '#DA8D96', '#D0587E', '#AE0000'])
    fig = fig.add_trace(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        text=text,
        textfont=dict(
            family="Lato, sans-serif",
            size=18,
            color="black"
        ),
        textposition="middle center",
        root_color="lightgrey",
        textinfo="label+text",
        marker_colors=marker_colors,
    ))

    fig.update_layout(
        title_x=0.5, title_y=0.98,
        title_text='類股交易量',
        title_font=dict(size=25, color='#8a8d93',
                        family="Lato, sans-serif"),
        margin=dict(l=0, r=0, t=45, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig
