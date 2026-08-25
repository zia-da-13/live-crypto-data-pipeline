import time

from crypto_api import get_crypto_data
from transform import transform_crypto_data
from save_data import save_crypto_data
from logger_config import logger


def run_pipeline():
    try:
        logger.info("Crypto pipeline started.")

        crypto_data = get_crypto_data()
        cleaned_data = transform_crypto_data(crypto_data)
        save_crypto_data(cleaned_data)

        logger.info("Crypto pipeline completed successfully.")

    except Exception as error:
        logger.exception(f"Crypto pipeline failed: {error}")
        print(f"Pipeline failed: {error}")


def main():
    print("Live crypto pipeline started.")

    try:
        while True:
            print("\nRunning crypto pipeline...")

            run_pipeline()

            print("Waiting 5 minutes...")
            time.sleep(300)

    except KeyboardInterrupt:
        print("\nCrypto pipeline stopped by user.")
        logger.info("Crypto pipeline stopped by user.")


if __name__ == "__main__":
    main()