import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Ecommerce Dashboard", layout="wide")

# === Завантаження даних ===
DATA_PATH = os.path.join('data', 'clean_data.csv')
df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"], encoding='ISO-8859-1')
df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
df['Hour'] = df['InvoiceDate'].dt.hour

st.title("Ecommerce AI Dashboard")
st.markdown("Інтерактивна панель для аналізу електронної комерції")

# === Вкладки ===
tabs = st.tabs([
    "Дохід по країнах",
    "Дохід по місяцях",
    "Топ-10 товарів",
    "Розподіл по клієнтах",
    "Продажі по годинах",
    "Найменші продажі (країни)"
])

# === 1. Дохід по країнах ===
with tabs[0]:
    st.subheader("Загальний дохід по країнах")
    revenue = df.groupby('Country')["TotalPrice"].sum().sort_values(ascending=False)
    fig = px.bar(
        revenue.head(20).reset_index(),
        x="Country", y="TotalPrice",
        color="TotalPrice",
        color_continuous_scale="viridis",
        title="Дохід по країнах (топ 20)"
    )
    st.plotly_chart(fig, use_container_width=True)

# === 2. Дохід по місяцях ===
with tabs[1]:
    st.subheader("Дохід по місяцях")
    monthly = df.groupby("Month")["TotalPrice"].sum().reset_index()
    fig = px.line(monthly, x="Month", y="TotalPrice", markers=True, title="Дохід по місяцях")
    st.plotly_chart(fig, use_container_width=True)

# === 3. Топ-10 товарів ===
with tabs[2]:
    st.subheader("Топ-10 товарів за доходом")
    top = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(
        top, x="TotalPrice", y="Description", orientation='h',
        color="TotalPrice", color_continuous_scale="plasma",
        title="Найприбутковіші товари"
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

# === 4. Розподіл доходу по клієнтах ===
with tabs[3]:
    st.subheader("Розподіл доходу по клієнтах")
    customer_value = df.groupby("CustomerID")["TotalPrice"].sum().reset_index()
    fig = px.histogram(customer_value, x="TotalPrice", nbins=40, title="Розподіл доходу")
    st.plotly_chart(fig, use_container_width=True)

# === 5. Продажі по годинах ===
with tabs[4]:
    st.subheader("Продажі протягом доби")
    hourly = df.groupby("Hour")["TotalPrice"].sum().reset_index()
    fig = px.line(hourly, x="Hour", y="TotalPrice", markers=True, title="Дохід по годинах")
    st.plotly_chart(fig, use_container_width=True)

# === 6. Найменші продажі (країни) ===
with tabs[5]:
    st.subheader("Країни з найменшими доходами")
    least = df.groupby('Country')["TotalPrice"].sum().sort_values(ascending=True).head(5).reset_index()
    fig = px.pie(least, names='Country', values='TotalPrice', title='Найменші продажі по країнах')
    st.plotly_chart(fig, use_container_width=True)
