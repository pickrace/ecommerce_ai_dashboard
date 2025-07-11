import streamlit as st
import pandas as pd
import os
from ai_agent import display_chat
from eda_analysis import (
    plot_revenue_by_country,
    plot_sales_over_time,
    plot_top_products,
    plot_heatmap
)

# Шлях до даних
DATA_PATH = os.path.join('data', 'clean_data.csv')

# Завантаження даних
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=['InvoiceDate'], encoding='ISO-8859-1')
    df = df[df['TotalPrice'] > 0]
    return df

df = load_data()

# Фільтри
st.sidebar.header("Фільтри")
country_filter = st.sidebar.multiselect("Країна", options=df['Country'].unique(), default=df['Country'].unique())
date_range = st.sidebar.date_input("Діапазон дат", [df['InvoiceDate'].min(), df['InvoiceDate'].max()])

# Застосування фільтрів
df_filtered = df[
    (df['Country'].isin(country_filter)) &
    (df['InvoiceDate'].dt.date >= date_range[0]) &
    (df['InvoiceDate'].dt.date <= date_range[1])
]

# Заголовок дашборду
st.title("Ecommerce BI Dashboard")

# KPI блок
col1, col2, col3 = st.columns(3)

with col1:
    total_revenue = round(df_filtered['TotalPrice'].sum(), 2)
    st.metric("Загальний дохід", f"£ {total_revenue}")

with col2:
    num_orders = df_filtered['InvoiceNo'].nunique()
    st.metric("Кількість замовлень", num_orders)

with col3:
    unique_customers = df_filtered['CustomerID'].nunique()
    st.metric("Унікальні клієнти", unique_customers)

st.divider()

# Графіки
st.subheader("Динаміка продажів по місяцях")
st.plotly_chart(plot_sales_over_time(df_filtered), use_container_width=True)

st.subheader("Сумарний дохід по країнах")
st.plotly_chart(plot_revenue_by_country(df_filtered), use_container_width=True)

st.subheader("Топ товари")
st.plotly_chart(plot_top_products(df_filtered), use_container_width=True)

st.subheader("Теплова карта активності")
st.plotly_chart(plot_heatmap(df_filtered), use_container_width=True)

#Розділ для чат-бота
st.divider()
st.subheader("AI Assistant")
display_chat()
