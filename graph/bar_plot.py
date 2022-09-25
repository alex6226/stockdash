import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 產業類股漲跌長條圖
def bar_plot(stock_roi):

    data = stock_roi.groupby('group').mean().reset_index()
    fig = go.Figure()
    for day in [1, 5, 10, 20, 60]:

        x = data.sort_values(by=f'roi_{day}', ascending=False)['group']
        y = data.sort_values(by=f'roi_{day}', ascending=False)[f'roi_{day}']
        y = np.array([round(i, 2) for i in y])

        colors = ['#FF2D2D', ] * len(x)
        for idx in np.where(y < 0)[0]:
            colors[idx] = '#02DF82'

        bar = go.Bar(x=x, y=y, name=f'roi_{day}', marker_color=colors)

        fig.add_trace(bar)

    fig.for_each_trace(lambda trace: trace.update(visible=False)
                       if trace.name != 'roi_1' else trace.update(visible=True))
    fig.update_traces(marker_line_width=1, marker_line_color="black")

    updatemenus = [
        dict(
            active=0,
            x=0.16,
            y=1.15,
            buttons=list([
                dict(label="近1日",
                     method="update",
                     args=[{"visible": [True, False, False, False, False]}]),
                dict(label="近5日",
                     method="update",
                     args=[{"visible": [False, True, False, False, False]}]),
                dict(label="近10日",
                     method="update",
                     args=[{"visible": [False, False, True, False, False]}]),
                dict(label="近20日",
                     method="update",
                     args=[{"visible": [False, False, False, True, False]}]),
                dict(label="近60日",
                     method="update",
                     args=[{"visible": [False, False, False, False, True]}]),
            ]))]

    fig.update_layout(
        title_x=0.5, title_y=0.98,
        title_text='產業漲跌',
        title_font=dict(size=25, color='#8a8d93',
                        family="Lato, sans-serif"),
        updatemenus=updatemenus,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig
