import requests

from transform import transform_crypto_data
from save_data import save_crypto_data


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

    crypto_data = response.json()

    return crypto_data


if __name__ == "__main__":
    crypto_data = get_crypto_data()

    cleaned_data = transform_crypto_data(crypto_data)

    save_crypto_data(cleaned_data)