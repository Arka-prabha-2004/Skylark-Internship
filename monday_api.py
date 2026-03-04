import requests
import os
from dotenv import load_dotenv
from config import MONDAY_API_URL
import streamlit as st

load_dotenv()

API_KEY = os.getenv("MONDAY_API_KEY") or st.secrets["MONDAY_API_KEY"]

headers = {
    "Authorization": API_KEY
}


def fetch_board_items(board_id):

    all_items = []
    cursor = None

    while True:

        cursor_part = f', cursor: "{cursor}"' if cursor else ""

        query = f"""
        query {{
          boards(ids: {board_id}) {{
            name
            items_page(limit: 100{cursor_part}) {{
              cursor
              items {{
                name
                column_values {{
                  text
                  column {{
                    title
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        response = requests.post(
            MONDAY_API_URL,
            json={"query": query},
            headers=headers
        )

        data = response.json()

        boards = data["data"]["boards"]
        items_page = boards[0]["items_page"]

        items = items_page["items"]
        cursor = items_page["cursor"]

        all_items.extend(items)

        if not cursor:
            break

    return {
        "data": {
            "boards": [
                {
                    "items_page": {
                        "items": all_items
                    }
                }
            ]
        }
    }


def get_board_schema(board_id):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        name
        columns {{
          id
          title
          type
        }}
      }}
    }}
    """

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query},
        headers=headers
    )

    return response.json()