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

    # -----------------------------
    # 1. Standardize column names
    # -----------------------------
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )

    # -----------------------------
    # 2. Replace empty values
    # -----------------------------
    df = df.replace("", pd.NA)
    df = df.fillna("Unknown")

    # -----------------------------
    # 3. Convert date columns
    # -----------------------------
    date_cols = [
        "tentative_close_date",
        "created_date",
        "data_delivery_date",
        "date_of_po_loi",
        "collection_date",
        "last_execution_date"
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # -----------------------------
    # 4. Convert numeric columns
    # -----------------------------
    numeric_cols = [
        "masked_deal_value",
        "revenue_billed",
        "collection_amount"
    ]

    for col in numeric_cols:
        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.replace("₹", "")
            )

            df[col] = pd.to_numeric(df[col], errors="coerce")

    # -----------------------------
    # 5. Clean sector names
    # -----------------------------
    if "sector_service" in df.columns:

        df["sector_service"] = (
            df["sector_service"]
            .astype(str)
            .str.strip()
            .str.title()
        )

    # -----------------------------
    # 6. Normalize status columns
    # -----------------------------
    status_cols = [
        "execution_status",
        "deal_stage",
        "collection_status"
    ]

    for col in status_cols:
        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
            )

    return df

def data_quality_report(df):

    report = {}

    report["rows"] = len(df)
    report["missing_values"] = df.isna().sum().to_dict()
    report["duplicates"] = df.duplicated().sum()

    return report