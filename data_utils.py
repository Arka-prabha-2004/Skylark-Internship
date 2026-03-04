import pandas as pd


def parse_board_items(api_response):

    boards = api_response["data"]["boards"]
    items = boards[0]["items_page"]["items"]

    rows = []

    for item in items:

        row = {"Item Name": item["name"]}

        for col in item["column_values"]:
            column_title = col["column"]["title"]
            value = col["text"]

            row[column_title] = value

        rows.append(row)

    df = pd.DataFrame(rows)

    return df


def clean_dataframe(df):

    df = df.fillna("Unknown")

    return df