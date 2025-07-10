import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.ticker as mtick

DATA_PATH = os.path.join('data', 'clean_data.csv')
df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"], encoding='ISO-8859-1')

country_sales = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False)

# Видаляємо UK, щоб побачити інші країни
top_non_uk = country_sales.drop('United Kingdom').head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_non_uk.index, y=top_non_uk.values, palette="magma")

# Графік Топ-10 країн за доходом
plt.title("Топ-10 країн за доходом (без UK)", fontsize=16)
plt.xlabel("Країна", fontsize=12)
plt.ylabel("Сума продажів (£)", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('£{x:,.0f}'))
plt.tight_layout()
plt.show()

# Підготовка
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
monthly_sales = df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
monthly_sales['YearMonth'] = monthly_sales['YearMonth'].astype(str)

# Графік Місячний дохід
plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_sales, x='YearMonth', y='TotalPrice', marker='o', linewidth=2.5, color='#4c72b0')
plt.title("Місячна динаміка доходу", fontsize=16)
plt.xlabel("Місяць", fontsize=12)
plt.ylabel("Сума продажів (£)", fontsize=12)
plt.xticks(rotation=45)
plt.grid(visible=True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


# Підготовка
top_products = (
    df.groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Графік Топ-10 товарів за к-стю продажів
plt.figure(figsize=(12,6))
sns.barplot(
    y=top_products.index,
    x=top_products.values,
    palette='YlGnBu'
)
plt.title("🛍Топ-10 товарів за кількістю продажів", fontsize=16)
plt.xlabel("Кількість одиниць", fontsize=12)
plt.ylabel("Назва товару", fontsize=12)
plt.grid(visible=True, axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Підготовка
country_counts = (
    df['Country']
    .value_counts()
    .drop('United Kingdom')  # перевага країни в продажах - 92%, немає сенсу її показувати
    .head(10)
)

# Графік Частка замовлень по країнах
plt.figure(figsize=(8,8))
plt.pie(
    country_counts.values,
    labels=country_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=sns.color_palette('pastel')
)
plt.title("Частка замовлень по країнах (без UK)", fontsize=16)
plt.tight_layout()
plt.show()

