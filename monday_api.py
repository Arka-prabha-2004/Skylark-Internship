import requests
import os
from dotenv import load_dotenv
from config import MONDAY_API_URL
from data_utils import parse_board_items, clean_dataframe

load_dotenv()

API_KEY = os.getenv("MONDAY_API_KEY")

print("API KEY LOADED:", API_KEY is not None)

headers = {
    "Authorization": API_KEY
}

def fetch_board_items(board_id):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        name
        items_page(limit: 100) {{
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

    return response.json()




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



if __name__ == "__main__":

    from config import DEALS_BOARD_ID
    from data_utils import parse_board_items, clean_dataframe

    data = fetch_board_items(DEALS_BOARD_ID)

    df = parse_board_items(data)

    df = clean_dataframe(df)

    print(df.head())

