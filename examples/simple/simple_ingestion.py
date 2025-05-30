import argparse
import datetime
import os
import time

import requests
from dotenv import load_dotenv


# setup environment
load_dotenv()


#################### CONFIG ####################
# API Config
IPCOPILOT_ORG_API_KEY = os.environ.get("IPCOPILOT_ORG_API_KEY", None)
IPCOPILOT_INGESTION_ENDPOINT = os.environ.get(
    "IPCOPILOT_INGESTION_ENDPOINT", None
)

# General Config
MAX_RETRIES = 5
###############################################


# api params
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {IPCOPILOT_ORG_API_KEY}",
}


payloads = [
    {
        "author": "fake_user_id",
        "source": "fake_source",
        "email": "fake_email@email.com",
        "comment_text": "fake comment test",
        "comment_link": "https://fake-url.com",
        "content_title": "",
        "content_link": None,
        "discussion_link": None,
        "context_link": "https://another-fake-url.com",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    },
]


def validate_args_and_env():
    """Validates all global vars required for the script are set

    Raises:
        ValueError: A value is missing from one or more required vars
    """
    missing_values = []
    if IPCOPILOT_ORG_API_KEY is None:
        missing_values.append("IPCOPILOT_ORG_API_KEY")
    if IPCOPILOT_INGESTION_ENDPOINT is None:
        missing_values.append("IPCOPILOT_INGESTION_ENDPOINT")

    if missing_values:
        raise ValueError(
            "The following vars are not set: "
            f"{', '.join([str(env_var_name) for env_var_name in missing_values])}\n"
            "Please set in environment vars or pass in via script arguments"
        )


def main():
    """
    Sends payloads to IP Copilot's Ingestion API for processing
    """
    validate_args_and_env()

    response = None
    retries = 0
    n_payloads = len(payloads)
    default_retry_wait_time = 15  # seconds
    for idx, payload in enumerate(payloads):
        response = None
        retries = 0
        while response is None or (
            response.status_code == 429 and MAX_RETRIES > retries
        ):
            response = requests.post(
                IPCOPILOT_INGESTION_ENDPOINT, json=payload, headers=headers
            )
            # Handle the response
            status_msg = f"Payload {idx} of {n_payloads} processed sucessfully"
            if response.status_code == 429:
                print(
                    f"Request failed with rate limit status {response.status_code}: {response.text}"
                )
                retry_sleep_time = response.headers.get(
                    "Retry-After", default_retry_wait_time
                )
                print(f"retrying in {retry_sleep_time} seconds")
                time.sleep(int(retry_sleep_time))
                retries += 1

            elif response.status_code >= 400:
                status_msg = f"Request failed with status {response.status_code}: {response.text}"

        if MAX_RETRIES <= retries:
            status_msg = (
                f"Max retries exceeded for Payload {idx} of {n_payloads}"
            )

        print(status_msg)


if __name__ == "__main__":
    _parser = argparse.ArgumentParser(
        description="Set API tokens and URL if not already set in environment variables."
    )

    _parser.add_argument(
        "--ipcopilot-org-api-key",
        type=str,
        default=None,
        help=(
            "ipcopilot org api key, alternatively can be set with "
            "env IPCOPILOT_ORG_API_KEY"
        ),
    )
    _parser.add_argument(
        "--ipcopilot-ingestion-endpoint",
        type=str,
        default=None,
        help=(
            "ipcopilot api url, alternatively can be set with "
            "env IPCOPILOT_INGESTION_ENDPOINT"
        ),
    )

    _args = _parser.parse_args()

    # Use argparse values if they are passed in, otherwise use environment variables
    if _args.ipcopilot_org_api_key:
        IPCOPILOT_ORG_API_KEY = _args.ipcopilot_org_api_key
    if _args.ipcopilot_ingestion_endpoint:
        IPCOPILOT_INGESTION_ENDPOINT = _args.ipcopilot_ingestion_endpoint

    main()
