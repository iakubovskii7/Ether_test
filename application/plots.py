import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

layout = go.Layout(
    title='Plot Title',
    xaxis=dict(
        title='x Axis',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='y Axis',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)


def plotly_line_df(data, x, y, title):
    fig_line = px.line(data,
                       x=x, y=y,
                       title=title)
    fig_line.update_layout(
        autosize=False,
        width=1200,
        height=500, )
    return fig_line


def plotly_line_series(data, title):
    fig_line = px.line(data, title=title)
    fig_line.update_layout(
        autosize=False,
        width=1000,
        height=400, )
    return fig_line


def plotly_boxplot(data, x, y, title):
    fig_box = px.box(data, x=x, y=y, points='outliers', title=title)
    fig_box.update_layout(
        autosize=False,
        width=1500,
        height=750,
        )
    return fig_box


def hist_line(data, x, y1, y2, y2_missing, title):
    fig_pos_mot = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig_pos_mot.add_trace(
        go.Bar(x=data[x],
               y=data[y1].values,
               name="ETH transactions in Quantity"),
        secondary_y=False,
    )

    fig_pos_mot.add_trace(
        go.Line(x=data[x],
                y=data[y2].values, name="Tokens value in USD"),
        secondary_y=True,
    )

    # fig_pos_mot.add_trace(
    #     go.Line(x=data[x],
    #             y=data[y2_missing].values, name="Second line"),
    #     secondary_y=True,
    # )

    # Add figure title
    fig_pos_mot.update_layout(
        title_text=f"<b>{title}<b>",
        titlefont=dict(family='Gravitas One', size=25, color='#7f7f7f')
    )

    # Set x-axis title
    fig_pos_mot.update_xaxes(title_text="Time",
                             titlefont=dict(
                                 family='Courier New, monospace',
                                 size=18,
                                 color='#7f7f7f'
                             )
                             )

    # Set y-axes titles
    fig_pos_mot.update_yaxes(title_text="<b>ETH transactions</b> ", secondary_y=False,
                             titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')
                             )
    fig_pos_mot.update_yaxes(title_text="<b>Cumulative token value in USD</b>", secondary_y=True,
                             titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
    fig_pos_mot.update_layout(
        autosize=False,
        width=1500,
        height=600, )

    return fig_pos_mot

