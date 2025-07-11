import streamlit as st
import re
from dataclasses import dataclass
from typing import Dict
import pandas as pd
from forecasting import RetailPredictor

@dataclass
class UserQuery:
    text: str
    intent: str
    parameters: Dict

class RetailAIAgent:
    def __init__(self, data_path: str = 'data/clean_data.csv'):
        self.predictor = RetailPredictor(data_path)
        self.intents = {
            'sales_forecast': r'(?i)(прогноз|передбачити|спрогнозувати).*продаж',
            'product_analysis': r'(?i)(топ|найкращ|популярн).*продукт',
            'customer_segments': r'(?i)(сегмент|груп|аналіз).*клієнт',
            'trend_analysis': r'(?i)(тренд|тенденц|динамік)',
            'help': r'(?i)(допомог|поміч|help)',
        }

    def parse_query(self, text: str) -> UserQuery:
        intent = None
        parameters = {}

        for intent_name, pattern in self.intents.items():
            if re.search(pattern, text):
                intent = intent_name
                break

        days_match = re.search(r'(\d+)\s*(день|дні|днів)', text)
        if days_match:
            parameters['days'] = int(days_match.group(1))

        top_match = re.search(r'топ[- ](\d+)', text)
        if top_match:
            parameters['top_n'] = int(top_match.group(1))

        return UserQuery(text=text, intent=intent, parameters=parameters)

    def process_query(self, query: str) -> tuple:
        """Повертає кортеж (текст_відповіді, графік_якщо_є)"""
        parsed_query = self.parse_query(query)

        if not parsed_query.intent:
            return self._generate_help_message(), None

        try:
            if parsed_query.intent == 'sales_forecast':
                return self._handle_sales_forecast(parsed_query)
            elif parsed_query.intent == 'product_analysis':
                return self._handle_product_analysis(parsed_query)
            elif parsed_query.intent == 'customer_segments':
                return self._handle_customer_segments(parsed_query)
            elif parsed_query.intent == 'trend_analysis':
                return self._handle_trend_analysis(parsed_query)
            elif parsed_query.intent == 'help':
                return self._generate_help_message(), None
        except Exception as e:
            return f"Вибачте, виникла помилка при обробці запиту: {str(e)}", None

    def _handle_sales_forecast(self, query: UserQuery) -> tuple:
        days = query.parameters.get('days', 7)
        forecast = self.predictor.predict_sales(future_days=days)

        response = f"Прогноз продажів на наступні {days} днів:\n\n"
        for _, row in forecast.iterrows():
            response += f"Дата: {row['Date'].strftime('%Y-%m-%d')}, "
            response += f"Прогноз продажів: £{row['Predicted_Sales']:.2f}\n"

        return response, self.predictor.get_forecast_plot(days)

    def _handle_product_analysis(self, query: UserQuery) -> tuple:
        n = query.parameters.get('top_n', 5)
        top_products = self.predictor.get_top_products(n=n)

        response = f"Топ-{n} продуктів за продажами:\n\n"
        for i, (_, product) in enumerate(top_products.iterrows(), 1):
            response += f"{i}. {product['Description']}\n"
            response += f"   Кількість: {product['Quantity']}\n"
            response += f"   Сума продажів: £{product['TotalPrice']:.2f}\n"

        return response, None

    def _handle_customer_segments(self, query: UserQuery) -> tuple:
        segments = self.predictor.get_customer_segments()

        response = "Аналіз клієнтських сегментів:\n\n"
        for metric in ['Recency', 'Frequency', 'Monetary']:
            response += f"\n{metric}:\n"
            response += f"Середнє значення: {segments[metric].mean():.2f}\n"
            response += f"Медіана: {segments[metric].median():.2f}\n"

        return response, None

    def _handle_trend_analysis(self, query: UserQuery) -> tuple:
        trends = self.predictor.analyze_trends()

        response = "Аналіз трендів продажів:\n\n"
        for trend in trends:
            response += f"- {trend}\n"

        return response, self.predictor.get_sales_plot()

    def _generate_help_message(self) -> str:
        return """Я можу допомогти вам з наступними запитами:
1. Прогноз продажів (наприклад, "спрогнозуй продажі на 7 днів")
2. Аналіз продуктів (наприклад, "покажи топ-5 продуктів")
3. Аналіз клієнтських сегментів (наприклад, "проаналізуй сегменти клієнтів")
4. Аналіз трендів (наприклад, "які тренди в продажах")

Будь ласка, сформулюйте ваш запит відповідно до цих категорій."""

def initialize_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = RetailAIAgent()

def display_chat():
    initialize_chat()

    st.title("AI Assistant для аналізу продажів")

    # Показуємо історію чату
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("fig"):
                st.plotly_chart(message["fig"])

    # Поле введення
    if prompt := st.chat_input("Введіть ваш запит..."):
        # Додаємо запит користувача до історії
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Отримуємо відповідь від агента
        response, fig = st.session_state.agent.process_query(prompt)

        # Додаємо відповідь до історії
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "fig": fig
        })

        # Оновлюємо чат
        st.rerun()

if __name__ == "__main__":
    display_chat()