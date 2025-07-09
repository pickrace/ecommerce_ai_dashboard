
import pandas as pd
import os

input_path = os.path.join('data', 'data_for_master.csv')
output_path = os.path.join('data', 'clean_data.csv')

def clean_data():
    df = pd.read_csv(input_path, encoding='ISO-8859-1')

    df.dropna(how='all', inplace=True) # видаляємо порожні рядки
    df.fillna('', inplace=True) # заповнення пропущених значень

    if {"Quantity", "UnitPrice"}.issubset(df.columns):
        df["TotalPrice"] = df["Quantity"] * df["UnitPrice"].round(1)  # робимо нову колонку

    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors='coerce', format="%d/%m/%Y %H:%M") # адаптуємо дату

    df.to_csv(output_path, index=False) # зберігаємо все
    print("Data cleaned successfully")

if __name__ == "__main__":
    clean_data()

