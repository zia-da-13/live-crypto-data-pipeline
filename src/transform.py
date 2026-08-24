def transform_crypto_data(crypto_data):
    cleaned_data = []

    for coin in crypto_data:
        cleaned_coin = {
            "id": coin["id"],
            "symbol": coin["symbol"],
            "name": coin["name"],
            "current_price": coin["current_price"],
            "market_cap": coin["market_cap"],
            "total_volume": coin["total_volume"],
            "high_24h": coin["high_24h"],
            "low_24h": coin["low_24h"],
            "price_change_percentage_24h": coin["price_change_percentage_24h"],
            "last_updated": coin["last_updated"]
        }

        cleaned_data.append(cleaned_coin)

    return cleaned_data