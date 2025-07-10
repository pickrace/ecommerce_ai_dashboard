# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# ==== Налаштування сторінки ====
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("E-Commerce AI Dashboard")

# ==== Завантаження даних ====
DATA_PATH = os.path.join('data', 'clean_data.csv')
df = pd.read_csv(DATA_PATH, parse_dates=['InvoiceDate'], encoding='ISO-8859-1')

# ==== Сайдбар-фільтри ====
st.sidebar.header("🔎 Фільтри")
selected_country = st.sidebar.selectbox("Країна", sorted(df['Country'].unique()))
start_date, end_date = st.sidebar.date_input("Діапазон дат", [df['InvoiceDate'].min(), df['InvoiceDate'].max()])

# ==== Фільтрація ====
df_filtered = df[
    (df['Country'] == selected_country) &
    (df['InvoiceDate'] >= pd.to_datetime(start_date)) &
    (df['InvoiceDate'] <= pd.to_datetime(end_date))
]

# ==== KPI Панель ====
total_sales = df_filtered['TotalPrice'].sum()
unique_customers = df_filtered['CustomerID'].nunique()
num_orders = df_filtered['InvoiceNo'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Загальний дохід", f"£{total_sales:,.2f}")
col2.metric("Унікальні клієнти", unique_customers)
col3.metric("Замовлення", num_orders)

st.markdown("---")

# ==== Графік 1: Дохід по місяцях ====
df_filtered['Month'] = df_filtered['InvoiceDate'].dt.to_period("M").astype(str)
monthly_sales = df_filtered.groupby('Month')['TotalPrice'].sum().reset_index()

fig1 = px.line(monthly_sales, x='Month', y='TotalPrice',
               title="Дохід по місяцях", markers=True,
               labels={"TotalPrice": "Дохід", "Month": "Місяць"})

fig1.update_traces(line=dict(color="#0077b6", width=3))
st.plotly_chart(fig1, use_container_width=True)

# ==== Графік 2: Найпопулярніші товари ====
top_products = df_filtered.groupby("Description")['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()

fig2 = px.bar(top_products, x='Quantity', y='Description',
              orientation='h', title="Топ-10 товарів за кількістю",
              color='Quantity', color_continuous_scale='blues')

fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig2, use_container_width=True)

# ==== Графік 3: Дохід по днях тижня ====
df_filtered['DayOfWeek'] = df_filtered['InvoiceDate'].dt.day_name()
sales_by_day = df_filtered.groupby('DayOfWeek')['TotalPrice'].sum().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
).reset_index()

fig3 = px.bar(sales_by_day, x='DayOfWeek', y='TotalPrice',
              title="Дохід по днях тижня", text_auto=True)

fig3.update_traces(marker_color="#90e0ef")
st.plotly_chart(fig3, use_container_width=True)

# ==== Графік 4: Кількість замовлень по годинах ====
df_filtered['Hour'] = df_filtered['InvoiceDate'].dt.hour
orders_by_hour = df_filtered.groupby('Hour')['InvoiceNo'].nunique().reset_index()

fig4 = px.area(orders_by_hour, x='Hour', y='InvoiceNo',
               title="Замовлення по годинах",
               labels={"InvoiceNo": "Кількість замовлень"})

fig4.update_traces(line_color="#00b4d8", fill='tozeroy')
st.plotly_chart(fig4, use_container_width=True)
