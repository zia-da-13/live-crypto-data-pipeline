import requests

from config import API_URL, CRYPTO_COINS, CURRENCY
from transform import transform_crypto_data
from save_data import save_crypto_data
from logger_config import logger


def get_crypto_data():
    parameters = {
        "vs_currency": CURRENCY,
        "ids": ",".join(CRYPTO_COINS),
        "order": "market_cap_desc",
        "sparkline": "false"
    }

    response = requests.get(
        API_URL,
        params=parameters,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def run_pipeline():
    try:
        logger.info("Crypto pipeline started.")

        # Extract
        crypto_data = get_crypto_data()

        # Transform
        cleaned_data = transform_crypto_data(crypto_data)

        # Load
        save_crypto_data(cleaned_data)

        logger.info(
            "Crypto pipeline completed successfully."
        )

    except Exception as error:
        logger.exception(
            f"Crypto pipeline failed: {error}"
        )

        print(
            f"Pipeline failed: {error}"
        )


if __name__ == "__main__":
    run_pipeline()