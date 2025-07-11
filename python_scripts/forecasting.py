import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

class RetailPredictor:
    def __init__(self, data_path='data/clean_data.csv'):
        self.data = pd.read_csv(data_path)
        self.data['InvoiceDate'] = pd.to_datetime(self.data['InvoiceDate'])
        self.models = {}

    def prepare_features(self, target_type='sales'):
        if target_type == 'sales':
            self.data['Year'] = self.data['InvoiceDate'].dt.year
            self.data['Month'] = self.data['InvoiceDate'].dt.month
            self.data['DayOfWeek'] = self.data['InvoiceDate'].dt.dayofweek
            self.data['Hour'] = self.data['InvoiceDate'].dt.hour

            daily_sales = self.data.groupby('InvoiceDate').agg({
                'TotalPrice': 'sum',
                'Quantity': 'sum'
            }).reset_index()

            X = pd.DataFrame({
                'Year': daily_sales['InvoiceDate'].dt.year,
                'Month': daily_sales['InvoiceDate'].dt.month,
                'DayOfWeek': daily_sales['InvoiceDate'].dt.dayofweek,
            })
            y = daily_sales['TotalPrice']

            return X, y, daily_sales

    def train_model(self, target_type='sales'):
        X, y, _ = self.prepare_features(target_type)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        self.models[target_type] = model
        return model.score(X_test, y_test)

    def predict_sales(self, future_days=7):
        if 'sales' not in self.models:
            self.train_model('sales')

        last_date = self.data['InvoiceDate'].max()
        future_dates = [last_date + timedelta(days=x) for x in range(1, future_days + 1)]

        future_features = pd.DataFrame({
            'Year': [d.year for d in future_dates],
            'Month': [d.month for d in future_dates],
            'DayOfWeek': [d.dayofweek for d in future_dates],
        })

        predictions = self.models['sales'].predict(future_features)

        return pd.DataFrame({
            'Date': future_dates,
            'Predicted_Sales': predictions
        })

    def get_top_products(self, n=5):
        return self.data.groupby('Description').agg({
            'Quantity': 'sum',
            'TotalPrice': 'sum'
        }).reset_index().nlargest(n, 'TotalPrice')

    def get_customer_segments(self, n_segments=3):
        last_purchase = self.data.groupby('CustomerID')['InvoiceDate'].max()
        recency = (self.data['InvoiceDate'].max() - last_purchase).dt.days
        frequency = self.data.groupby('CustomerID')['InvoiceNo'].count()
        monetary = self.data.groupby('CustomerID')['TotalPrice'].sum()

        return pd.DataFrame({
            'Recency': recency,
            'Frequency': frequency,
            'Monetary': monetary
        })

    def analyze_trends(self):
        daily_sales = self.data.groupby('InvoiceDate')['TotalPrice'].sum().reset_index()
        rolling_mean = daily_sales['TotalPrice'].rolling(window=7).mean()

        trends = []
        if rolling_mean.iloc[-1] > rolling_mean.iloc[-7]:
            trends.append("Позитивний тренд: Зростання продажів за останній тиждень")
        else:
            trends.append("Негативний тренд: Спад продажів за останній тиждень")

        return trends

    def get_sales_plot(self):
        daily_sales = self.data.groupby('InvoiceDate')['TotalPrice'].sum().reset_index()
        fig = px.line(daily_sales, x='InvoiceDate', y='TotalPrice',
                      title='Динаміка продажів')
        return fig

    def get_forecast_plot(self, days=7):
        forecast = self.predict_sales(days)
        fig = go.Figure()

        # Історичні дані
        daily_sales = self.data.groupby('InvoiceDate')['TotalPrice'].sum().reset_index()
        fig.add_trace(go.Scatter(x=daily_sales['InvoiceDate'], y=daily_sales['TotalPrice'],
                                 name='Історичні дані'))

        # Прогноз
        fig.add_trace(go.Scatter(x=forecast['Date'], y=forecast['Predicted_Sales'],
                                 name='Прогноз', line=dict(dash='dash')))

        fig.update_layout(title='Прогноз продажів',
                          xaxis_title='Дата',
                          yaxis_title='Продажі')
        return fig