# app.py
import streamlit as st
from eda_analysis import (
    load_clean_data,
    kpi_cards,
    revenue_by_country,
    revenue_over_time,
    top_products,
    orders_by_hour
)

st.set_page_config(page_title="Ecommerce AI Dashboard", layout="wide")
st.title("🛍 Ecommerce AI Dashboard")
st.markdown("Інтерактивна аналітика для інтернет-магазину")

# Загрузка даних
df = load_clean_data()

# KPI-карточки
st.plotly_chart(kpi_cards(df), use_container_width=True)

# Layout: 2 колонки з графіками
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(revenue_over_time(df), use_container_width=True)
with col2:
    st.plotly_chart(revenue_by_country(df), use_container_width=True)

# Нижній блок
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(top_products(df), use_container_width=True)
with col4:
    st.plotly_chart(orders_by_hour(df), use_container_width=True)

st.markdown("---")
st.caption("Побудовано з Plotly + Streamlit")
