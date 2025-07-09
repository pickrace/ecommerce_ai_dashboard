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

plt.title("Топ-10 країн за доходом (без UK)", fontsize=16)
plt.xlabel("Країна", fontsize=12)
plt.ylabel("Сума продажів (£)", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('£{x:,.0f}'))
plt.tight_layout()
plt.show()
