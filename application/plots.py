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


def plotly_barplot(data, x, y, title):
    fig_bar = px.bar(data, x=x, y=y, orientation='h')
    fig_bar.update_layout(
        autosize=False,
        width=1200,
        height=500, )
    return fig_bar


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


def two_lines(data, x, y1, y2, title):
    plot = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    plot.add_trace(
        go.Line(x=data[x],
                y=data[y1].values,
                name="Outflow of tokens"),
        secondary_y=False,
    )

    plot.add_trace(
        go.Line(x=data[x],
                y=data[y2].values,
                name="Inflow of tokens"),
        secondary_y=True,
    )

    # fig_pos_mot.add_trace(
    #     go.Line(x=data[x],
    #             y=data[y2_missing].values, name="Second line"),
    #     secondary_y=True,
    # )

    # Add figure title
    plot.update_layout(
        title_text=f"<b>{title}<b>",
        titlefont=dict(family='Gravitas One', size=25, color='#7f7f7f')
    )

    # Set x-axis title
    plot.update_xaxes(title_text="Time",
                      titlefont=dict(
                                 family='Courier New, monospace',
                                 size=18,
                                 color='#7f7f7f'
                             )
                      )

    # Set y-axes titles
    plot.update_yaxes(title_text="<b>OUTFLOW</b> ", secondary_y=False,
                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')
                      )
    plot.update_yaxes(title_text="<b>INFLOW</b>", secondary_y=True,
                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
    plot.update_layout(
        autosize=False,
        width=1500,
        height=600, )

    return plot

