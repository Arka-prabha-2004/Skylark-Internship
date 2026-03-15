import os
from dotenv import load_dotenv
from google import genai

from monday_api import fetch_board_items
from data_utils import parse_board_items, clean_dataframe
from config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID

import streamlit as st

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)


# ------------------------------
# FETCH DATA FROM MONDAY BOARDS
# ------------------------------

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


# ------------------------------
# BUSINESS METRICS
# ------------------------------

def compute_metrics(deals, work_orders):

    metrics = {}

    if "masked_deal_value" in deals.columns:
        metrics["total_pipeline_value"] = deals["masked_deal_value"].fillna(0).sum()

    if "sector_service" in deals.columns:
        metrics["deals_per_sector"] = deals["sector_service"].value_counts().to_dict()

    if "execution_status" in work_orders.columns:
        metrics["completed_work_orders"] = (
            work_orders["execution_status"]
            .str.lower()
            .eq("completed")
            .sum()
        )

    metrics["total_work_orders"] = len(work_orders)

    return metrics


# ------------------------------
# AGENT FUNCTION
# ------------------------------

def ask_agent(question, deals, work_orders, chat_history=None):

    steps = []

    steps.append("🔎 Fetching data from monday.com boards...")
    steps.append(f"📥 Retrieved {len(deals)} deals")
    steps.append(f"📥 Retrieved {len(work_orders)} work orders")

    metrics = compute_metrics(deals, work_orders)

    # conversation memory for follow-up queries
    conversation_context = ""

    if chat_history:
        for role, msg in chat_history[-4:]:
            conversation_context += f"{role}: {msg}\n"

    context = f"""
Business Metrics

Total Pipeline Value: {metrics.get("total_pipeline_value")}
Deals per Sector: {metrics.get("deals_per_sector")}
Completed Work Orders: {metrics.get("completed_work_orders")}
Total Work Orders: {metrics.get("total_work_orders")}

Deals Data (sample):
{deals.head(50).to_string(index=False)}

Work Orders Data (sample):
{work_orders.head(50).to_string(index=False)}
"""

    prompt = f"""
You are a business intelligence assistant helping company founders analyze company data.

Conversation so far:
{conversation_context}

Follow these rules:

1. Use the provided business metrics first when answering.
2. Only use raw tables if more detail is needed.
3. Never invent numbers or sectors not present in the data.
4. If data is missing or unclear, explain the limitation.

If the user asks for a leadership update, produce an executive summary including:

• pipeline health
• sector performance
• operational execution
• risks or missing data

Keep responses concise and executive-friendly.

{context}

User Question:
{question}
"""

    steps.append("📊 Analyzing business metrics...")

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[prompt]
    )

    return response.text, steps


# ------------------------------
# KPI DASHBOARD METRICS
# ------------------------------

def get_kpis():

    deals = get_deals_data()
    work_orders = get_work_orders_data()

    deal_count = len(deals)
    work_orders_count = len(work_orders)

    sector_count = deals["sector_service"].nunique() if "sector_service" in deals.columns else 0

    return deal_count, work_orders_count, sector_count