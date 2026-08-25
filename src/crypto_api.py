import requests

from transform import transform_crypto_data
from save_data import save_crypto_data
from logger_config import logger


def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"

    parameters = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana",
        "order": "market_cap_desc",
        "sparkline": "false"
    }

    response = requests.get(url, params=parameters, timeout=10)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    try:
        logger.info("Crypto pipeline started.")

        crypto_data = get_crypto_data()
        cleaned_data = transform_crypto_data(crypto_data)
        save_crypto_data(cleaned_data)

        logger.info("Crypto pipeline completed successfully.")

    except Exception as error:
        logger.exception(f"Crypto pipeline failed: {error}")
        print(f"Pipeline failed: {error}")