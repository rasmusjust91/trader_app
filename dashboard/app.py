import dash
import dash_core_components as dcc
import dash_html_components as html

# import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .resources.fetch_data import get_data

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

stock = "MAERSK-B.CO"


def get_stock_history_fig(stock):
    data = get_data(stock)
    time = data.index
    # print(data)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time, y=data["Open"], name="Open", line=dict(color="firebrick", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=time,
            y=data["Close"],
            name="Close",
            line=dict(color="royalblue", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=time,
            y=data["Low"],
            name="Low",
            line=dict(dash="dash", width=2, color="red"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=time,
            y=data["High"],
            name="High",
            line=dict(dash="dash", width=2, color="green"),
        )
    )

    fig.update_layout(
        title=f"{stock}",
        yaxis_title="Stock price [DDK]",
        xaxis_title="Time",
        font=dict(size=18, color="#7f7f7f"),
    )

    return fig


def get_daily_change_fig(stock):
    data = get_data(stock)
    time = data.index
    data["daily_change"] = (data["Open"] - data["Close"]) / data["Open"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time,
            y=data["daily_change"],
            name="Daily change",
            line=dict(color="firebrick", width=3),
        )
    )

    fig.update_layout(
        title=f"Percentage daily change for {stock}",
        yaxis_title="Daily change [%]",
        xaxis_title="Time",
        font=dict(size=18, color="#7f7f7f"),
    )
    return fig


# TODO: Make sure the plots share x-axis
# from plotly.subplots import make_subplots

# fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
# fig.add_trace(get_stock_history_fig(stock), row=1, col=1)
# fig.add_trace(get_daily_change_fig(stock), row=2, col=1)
# fig.update_layout(height=600, width=600,
#                   title_text="Stacked Subplots with Shared X-Axes")
app.layout = html.Div(
    children=[
        html.Center(html.H2(children="Dashboard")),
        dcc.Graph(id="graph", figure=get_stock_history_fig(stock)),
        dcc.Graph(id="graph_2", figure=get_daily_change_fig(stock)),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=29999)
