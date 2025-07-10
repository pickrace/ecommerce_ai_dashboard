# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
DATA_PATH = os.path.join('data', 'clean_data.csv')
df = pd.read_csv(DATA_PATH, parse_dates=['InvoiceDate'], encoding='ISO-8859-1')

# App title
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("Інтерактивна аналітика e-commerce")

# Sidebar filters
st.sidebar.header("🔎 Фільтри")
country = st.sidebar.selectbox("Обрати країну:", sorted(df['Country'].unique()))
date_range = st.sidebar.date_input("Обрати діапазон дат:",
    [df['InvoiceDate'].min(), df['InvoiceDate'].max()])

# Фільтрація даних
df_filtered = df[(df['Country'] == country) &
                 (df['InvoiceDate'] >= pd.to_datetime(date_range[0])) &
                 (df['InvoiceDate'] <= pd.to_datetime(date_range[1]))]

# KPIs
total_sales = df_filtered['TotalPrice'].sum()
total_invoices = df_filtered['InvoiceNo'].nunique()

col1, col2 = st.columns(2)
col1.metric("Загальний дохід", f"£{total_sales:,.2f}")
col2.metric("Кількість замовлень", f"{total_invoices}")

# Visualization 1: Дохід по місяцях
st.subheader("Динаміка доходу")
df_filtered['Month'] = df_filtered['InvoiceDate'].dt.to_period("M").astype(str)
monthly_sales = df_filtered.groupby("Month")["TotalPrice"].sum()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker="o", ax=ax)
ax.set_title("Загальний дохід по місяцях")
ax.set_ylabel("Дохід")
plt.xticks(rotation=45)
st.pyplot(fig)
