import os
from datetime import datetime, timezone

import pandas as pd

from config import CSV_FILE_PATH
from database_service import get_database_connection


def save_crypto_data(crypto_data):
    data_frame = pd.DataFrame(crypto_data)

    # Add pipeline collection timestamp
    data_frame["collected_at"] = datetime.now(timezone.utc)

    # Make sure the data folder exists
    data_directory = os.path.dirname(CSV_FILE_PATH)

    if data_directory:
        os.makedirs(
            data_directory,
            exist_ok=True
        )

    # ============================================
    # Save to CSV without duplicates
    # ============================================

    if os.path.exists(CSV_FILE_PATH):

        existing_data = pd.read_csv(
            CSV_FILE_PATH
        )

        combined_data = pd.concat(
            [existing_data, data_frame],
            ignore_index=True
        )

        combined_data = combined_data.drop_duplicates(
            subset=["id", "last_updated"],
            keep="first"
        )

        combined_data.to_csv(
            CSV_FILE_PATH,
            index=False
        )

    else:

        data_frame.to_csv(
            CSV_FILE_PATH,
            index=False
        )

    # ============================================
    # Save to PostgreSQL
    # ============================================

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
                    ON CONFLICT (coin_id, last_updated)
                    DO NOTHING;
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
                        row[
                            "price_change_percentage_24h"
                        ],
                        row["last_updated"],
                        row["collected_at"]
                    )
                )