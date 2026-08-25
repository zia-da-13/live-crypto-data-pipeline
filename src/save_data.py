import os
import pandas as pd
from datetime import datetime, timezone

from database_service import get_database_connection


def save_crypto_data(crypto_data):
    data_frame = pd.DataFrame(crypto_data)

    data_frame["collected_at"] = datetime.now(timezone.utc)

    os.makedirs("data", exist_ok=True)

    file_path = "data/crypto_market_data.csv"

    file_exists = os.path.exists(file_path)

    data_frame.to_csv(
        file_path,
        mode="a",
        header=not file_exists,
        index=False
    )

    save_to_database(data_frame)

    print("Crypto data saved successfully.")


def save_to_database(data_frame):
    connection = get_database_connection()

    with connection:
        with connection.cursor() as cursor:
            for _, row in data_frame.iterrows():
                cursor.execute(
                    """
                    INSERT INTO crypto_market_data (
                        coin_id,
                        symbol,
                        name,
                        current_price,
                        market_cap,
                        total_volume,
                        high_24h,
                        low_24h,
                        price_change_percentage_24h,
                        last_updated,
                        collected_at
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        row["id"],
                        row["symbol"],
                        row["name"],
                        row["current_price"],
                        row["market_cap"],
                        row["total_volume"],
                        row["high_24h"],
                        row["low_24h"],
                        row["price_change_percentage_24h"],
                        row["last_updated"],
                        row["collected_at"]
                    )
                )