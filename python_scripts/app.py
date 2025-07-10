# app.py

import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Додаткова конфігурація Streamlit
st.set_page_config(page_title="E-commerce AI Dashboard", layout="wide")

# Шлях до даних
DATA_PATH = os.path.join("data", "clean_data.csv")
df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"], encoding="ISO-8859-1")

st.title("E-commerce Dashboard with AI Agent")

# KPI блок
col1, col2, col3 = st.columns(3)
col1.metric("Загальний дохід", f"£{df['TotalPrice'].sum():,.2f}")
col2.metric("Замовлень", df["InvoiceNo"].nunique())
col3.metric("Клієнтів", df["CustomerID"].nunique())

st.markdown("---")

# Фільтр по країні (сайдбар)
countries = df["Country"].unique().tolist()
selected_countries = st.sidebar.multiselect("Оберіть країни:", countries, default=["United Kingdom"])

filtered_df = df[df["Country"].isin(selected_countries)]

# Графік: дохід по країнах
st.subheader("🌍 Дохід по країнах")
revenue_by_country = (
    filtered_df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=revenue_by_country.index, y=revenue_by_country.values, palette="viridis", ax=ax1)
ax1.set_xlabel("Країна")
ax1.set_ylabel("Дохід")
ax1.set_title("Дохід по країнах")
plt.xticks(rotation=45)
st.pyplot(fig1)
