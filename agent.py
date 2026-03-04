import os
from dotenv import load_dotenv
from google import genai

from monday_api import fetch_board_items
from data_utils import parse_board_items, clean_dataframe
from config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID

load_dotenv()

import streamlit as st

api_key = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

def get_deals_data():
    data = fetch_board_items(DEALS_BOARD_ID)
    df = parse_board_items(data)
    df = clean_dataframe(df)
    return df


def get_work_orders_data():
    data = fetch_board_items(WORK_ORDERS_BOARD_ID)
    df = parse_board_items(data)
    df = clean_dataframe(df)
    return df

def ask_agent(question):

    steps = []

    steps.append("🔎 Fetching Deals board data...")
    deals = get_deals_data()

    steps.append("🔎 Fetching Work Orders board data...")
    work_orders = get_work_orders_data()

    context = f"""
Deals Data:
{deals.head(50).to_string()}

Work Orders Data:
{work_orders.head(50).to_string()}
"""

    prompt = f"""
You are a business intelligence assistant helping company founders.

Answer the user's question using the data.

If the user asks for a leadership update, generate a concise executive summary including:

• pipeline health
• sector performance
• operational execution
• risks or missing data

Use bullet points and keep it clear for executives.

{context}

Question: {question}
"""

    steps.append("📊 Analyzing business metrics...")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text, steps

if __name__ == "__main__":

    question = "How many deals are there?"

    answer = ask_agent(question)

    print(answer)