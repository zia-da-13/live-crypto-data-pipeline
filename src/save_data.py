import os
import pandas as pd
from datetime import datetime, timezone


def save_crypto_data(crypto_data):
    data_frame = pd.DataFrame(crypto_data)

    # Add the time when our pipeline collected the data
    data_frame["collected_at"] = datetime.now(timezone.utc)

    file_path = "data/crypto_market_data.csv"

    # Check if the CSV already exists
    file_exists = os.path.exists(file_path)

    data_frame.to_csv(
        file_path,
        mode="a",
        header=not file_exists,
        index=False
    )

    print("Crypto data saved successfully.")