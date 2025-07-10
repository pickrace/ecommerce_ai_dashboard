import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Завантаження даних ===
DATA_PATH = os.path.join('data', 'clean_data.csv')
df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"], encoding='ISO-8859-1')

# === Попередня обробка ===
df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
df['Hour'] = df['InvoiceDate'].dt.hour

# === 1. Загальний дохід по країнах (barplot) ===
def plot_revenue_by_country():
    revenue = df.groupby('Country')["TotalPrice"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.barplot(x=revenue.index, y=revenue.values, ax=ax, palette="crest")
    ax.set_title("Загальний дохід по країнах", fontsize=16)
    ax.set_ylabel("Дохід")
    ax.set_xlabel("Країна")
    plt.xticks(rotation=90)
    plt.tight_layout()
    return fig

# === 2. Дохід по місяцях (lineplot) ===
def plot_monthly_revenue():
    monthly = df.groupby("Month")["TotalPrice"].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=monthly.index, y=monthly.values, marker='o', ax=ax, color='navy')
    ax.set_title("Дохід по місяцях", fontsize=16)
    ax.set_ylabel("Дохід")
    ax.set_xlabel("Місяць")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# === 3. Топ-10 товарів (horizontal barplot) ===
def plot_top_products():
    top = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top.values, y=top.index, ax=ax, palette="flare")
    ax.set_title("Топ-10 товарів за доходом", fontsize=16)
    ax.set_xlabel("Дохід")
    ax.set_ylabel("Товар")
    plt.tight_layout()
    return fig

# === 4. Розподіл доходу на клієнта (histogram) ===
def plot_customer_distribution():
    customer_value = df.groupby("CustomerID")["TotalPrice"].sum()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(customer_value, bins=40, kde=True, ax=ax, color='purple')
    ax.set_title("Розподіл доходу на клієнта", fontsize=16)
    ax.set_xlabel("Загальний дохід")
    ax.set_ylabel("Кількість клієнтів")
    plt.tight_layout()
    return fig

# === 5. Продажі протягом доби (hourly pattern, lineplot) ===
def plot_hourly_sales():
    hourly = df.groupby("Hour")["TotalPrice"].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=hourly.index, y=hourly.values, marker='o', ax=ax, color='darkgreen')
    ax.set_title("Активність продажів по годинах", fontsize=16)
    ax.set_xlabel("Година")
    ax.set_ylabel("Дохід")
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    return fig

# === 6. Країни з найменшими продажами (pie chart) ===
def plot_least_sales_countries():
    country_sum = df.groupby('Country')["TotalPrice"].sum().sort_values().head(5)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(country_sum.values, labels=country_sum.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.set_title("Країни з найменшими продажами", fontsize=14)
    return fig
