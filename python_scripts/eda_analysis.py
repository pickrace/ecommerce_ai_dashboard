import pandas as pd
import plotly.express as px

# Графік: Дохід по країнах
def plot_revenue_by_country(df):
    df_country = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(df_country, x='Country', y='TotalPrice',
                 title='Сумарний дохід по країнах',
                 color='TotalPrice', height=400)
    return fig

# Графік: Продажі по часу
def plot_sales_over_time(df):
    df_time = df.resample('M', on='InvoiceDate')['TotalPrice'].sum().reset_index()
    fig = px.line(df_time, x='InvoiceDate', y='TotalPrice',
                  title='Динаміка продажів по місяцях',
                  markers=True)
    return fig

# Графік: Топ-товари
def plot_top_products(df, top_n=10):
    top_products = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(top_n).reset_index()
    fig = px.bar(top_products, x='TotalPrice', y='Description', orientation='h',
                 title=f'Топ {top_n} товарів по доходу', height=450)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

# Графік: Heatmap день × година
def plot_heatmap(df):
    df['Hour'] = df['InvoiceDate'].dt.hour
    df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
    heatmap_data = df.groupby(['DayOfWeek', 'Hour'])['TotalPrice'].sum().reset_index()
    pivot_table = heatmap_data.pivot(index='DayOfWeek', columns='Hour', values='TotalPrice')
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(ordered_days)

    fig = px.imshow(pivot_table, aspect="auto", color_continuous_scale='Blues',
                    labels=dict(x="Година", y="День тижня", color="Дохід"),
                    title="Теплова карта продажів (день × година)")
    return fig
