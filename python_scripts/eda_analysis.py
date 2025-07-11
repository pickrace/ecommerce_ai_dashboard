# eda_analysis.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_clean_data():
    df = pd.read_csv("data/clean_data.csv", parse_dates=["InvoiceDate"])
    return df

# KPI-індикатори
def kpi_cards(df):
    total_revenue = df["TotalPrice"].sum()
    total_orders = df["InvoiceNo"].nunique()
    total_customers = df["CustomerID"].nunique()

    kpi = go.Figure()

    kpi.add_trace(go.Indicator(
        mode="number",
        value=total_revenue,
        title={"text": "Total Revenue"},
        number={"prefix": "$"},
        domain={"row": 0, "column": 0}
    ))

    kpi.add_trace(go.Indicator(
        mode="number",
        value=total_orders,
        title={"text": "Orders"},
        domain={"row": 0, "column": 1}
    ))

    kpi.add_trace(go.Indicator(
        mode="number",
        value=total_customers,
        title={"text": "Unique Customers"},
        domain={"row": 0, "column": 2}
    ))

    kpi.update_layout(grid={"rows": 1, "columns": 3}, height=200, margin={"t": 20, "b": 0})
    return kpi


def revenue_by_country(df, top_n=10):
    top = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(top_n).reset_index()
    fig = px.bar(top, x="Country", y="TotalPrice", title="🌍 Revenue by Country", text_auto=".2s")
    fig.update_layout(template="plotly_white")
    return fig


def revenue_over_time(df):
    df_time = df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"].sum().reset_index()
    df_time["InvoiceDate"] = df_time["InvoiceDate"].dt.to_timestamp()
    fig = px.line(df_time, x="InvoiceDate", y="TotalPrice", title="Monthly Revenue Trend")
    fig.update_traces(mode="lines+markers")
    return fig


def top_products(df, top_n=10):
    top = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(top_n).reset_index()
    fig = px.bar(top, x="TotalPrice", y="Description", orientation="h", title="Top Products by Revenue")
    fig.update_layout(template="plotly_white", yaxis={"categoryorder": "total ascending"})
    return fig


def orders_by_hour(df):
    df["Hour"] = df["InvoiceDate"].dt.hour
    hourly = df.groupby("Hour")["TotalPrice"].sum().reset_index()
    fig = px.area(hourly, x="Hour", y="TotalPrice", title="Revenue by Hour of Day")
    fig.update_layout(template="plotly_white")
    return fig
