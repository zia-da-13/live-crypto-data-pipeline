import time

from config import COLLECTION_INTERVAL_SECONDS
from crypto_api import run_pipeline
from logger_config import logger


def main():
    print("Live crypto pipeline started.")

    logger.info("Live crypto pipeline started.")

    try:
        while True:
            print("\nRunning crypto pipeline...")

            run_pipeline()

            minutes = COLLECTION_INTERVAL_SECONDS / 60

            print(
                f"Waiting {minutes:g} minutes "
                "for the next collection..."
            )

            time.sleep(COLLECTION_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nCrypto pipeline stopped by user.")

        logger.info(
            "Crypto pipeline stopped by user."
        )


if __name__ == "__main__":
    main()
    