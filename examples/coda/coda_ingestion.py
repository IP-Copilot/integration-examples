import argparse
import copy
import datetime
import os
import time
from typing import Generator

import requests


# ipcopilot api params
IPCOPILOT_ORG_API_KEY = os.environ.get("IPCOPILOT_ORG_API_KEY", None)
IPCOPILOT_API_URL = os.environ.get("IPCOPILOT_API_URL", None)
IPCOPILOT_MAX_RETRIES = 5


# coda api params
CODA_API_TOKEN = os.environ.get("CODA_API_TOKEN", None)
CODA_BASE_URL = "https://coda.io/apis/v1"


# General params
PAGE_RESULTS_BORDER = "*" * 50
DOC_RESULTS_BORDER = "-" * 50


def get_coda_headers():
    return {
        "Authorization": f"Bearer {CODA_API_TOKEN}",
        "X-Coda-Doc-Version": "latest",  # Ensures the latest copy of the data pulled
    }


def get_ipcopilot_headers():
    return {
        "Content-Type": "application/json",  # Tell the server to expect JSON
        "authorization": f"Bearer {IPCOPILOT_ORG_API_KEY}",
    }


def initiate_coda_page_content_export_request(
    url: str,
) -> str:
    """Sends a request to coda to generate a content export link (downloadLink)

    Args:
        url (str): The url to request a pages content export
            (/docs/{doc_id}/pages/{page_id}/export)

    Raises:
        RuntimeError: There was an issue with exporting the page content

    Returns:
        str: A request id to pull the metadata of a content export request
    """
    payload = {
        "outputFormat": "markdown",
    }
    response = requests.post(
        url, headers=get_coda_headers(), json=payload, allow_redirects=False
    )
    response.raise_for_status()
    if response.status_code >= 300:
        raise RuntimeError(
            f"ERROR: Recieved {response.status_code} when pulling page "
            f"content from url: {url}"
        )
    return response.json()["id"]


def pull_exported_coda_page_content(
    url: str,
    max_content_pull_retries: int = 10,
    seconds_to_wait_after_status_check: int = 2,
) -> str | None:
    """Pulls the exported content from a pages downloadLink

    Args:
        url (str): The url to check the status of a pages content export
            (/docs/{doc_id}/pages/{page_id}/export/{request_id})
        max_content_pull_retries (int, optional): The number of retry attempts
            for checking the status of a content export before timing out.
            Defaults to 10.
        seconds_to_wait_after_status_check (int, optional): The amount of time
            in seconds to wait between status check retries. Defaults to 2.

    Raises:
        RuntimeError: An error other than 404 has occured upon status check

    Returns:
        str | None: Either the cotent str (in markdown) exported by coda
            or null if the pull of content has timed out
    """
    status_res_dict = None
    retries = 0
    # Wait for status of content downloadLink to be "complete"
    while (
        status_res_dict is None or status_res_dict.get("status") != "complete"
    ):
        status_res = requests.get(
            url, headers=get_coda_headers(), allow_redirects=False
        )

        # Somtimes coda takes a while to generate the download link
        # so it will return a 404 if we request too quickly
        if status_res.status_code == 404:
            retries += 1
            print(f"Waiting for downloadLink to exist")
            time.sleep(seconds_to_wait_after_status_check)
            continue
        elif status_res.status_code >= 300:
            status_res.raise_for_status()

            # Raises if raise_for_status does not occur
            raise RuntimeError(
                f"ERROR: Recieved {status_res.status_code} when pulling page "
                f"content from url: {url}"
            )

        status_res_dict = status_res.json()
        if status_res_dict.get("status") != "complete":
            retries += 1
            print(
                f"Waiting for downloadLink status complete. Is currently: {status_res_dict.get('status')}"
            )
            time.sleep(seconds_to_wait_after_status_check)

        if retries > max_content_pull_retries:
            print(
                f"Max retries exceeded {max_content_pull_retries}, failed to pull content from {url}"
            )
            return

    print(f"downloadLink status complete. Downloading...")
    page_content_download_link = status_res_dict.get("downloadLink", None)
    if not page_content_download_link:
        print(f"Issue with download url: {url}")
        return

    page_content_response = requests.get(
        page_content_download_link, allow_redirects=False
    )
    if page_content_response.status_code != 200 or not hasattr(
        page_content_response, "text"
    ):
        print(
            f"Page content download failed with status_code {page_content_response.status_code}"
        )
        return
    print(f"Page content pull complete")
    return page_content_response.text


def get_page_content_from_coda(
    doc_id: str,
    page: str,
    max_content_pull_retries: int = 10,
    seconds_to_wait_after_status_check: int = 2,
) -> str | None:
    """Exports then pulls a pages content using the coda rest API

    Args:
        doc_id (str): The id of the doc that contains the targeted page
            for content pull
        page (dict): The metadata of the page targeted for content pull
        max_content_pull_retries (int, optional): The number of retry attempts
            for checking the status of a content export before timing out.
            Defaults to 10.
        seconds_to_wait_after_status_check (int, optional): The amount of time
            in seconds to wait between status check retries. Defaults to 2.

    Returns:
        str | None: Either the cotent str (in markdown) exported by coda
            or null if the pull of content has timed out
    """
    # Export page to downloadLink
    page_id = page["id"]
    export_url = f"{CODA_BASE_URL}/docs/{doc_id}/pages/{page_id}/export"
    try:
        print(f"Exporting {page['name']} contents...")
        request_id = initiate_coda_page_content_export_request(
            export_url,
        )
    except Exception as e:
        print(e)
        return

    # Pull page contents from downloadLink
    try:
        print(f"Pulling exported {page['name']} contents...")
        return pull_exported_coda_page_content(
            url=f"{export_url}/{request_id}",
            max_content_pull_retries=max_content_pull_retries,
            seconds_to_wait_after_status_check=seconds_to_wait_after_status_check,
        )
    except Exception as e:
        print(e)
        return


def iter_content_metadata_pulled_from_coda(
    url: str,
) -> Generator[dict[any], None, None]:
    """Create a generator for a url that has the potential to have multiple
        returns per endpoint call

    Args:
        url (str): The url to the endpoint you wish to generate data from

    Yields:
        Generator[dict[any]]: iterable of coda item dict in responses
            from endpoints
    """
    headers = copy.deepcopy(get_coda_headers())
    headers["pageToken"] = None
    while True:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code != 200:
            print(f"Failure pulling docs from {url}: {response.status_code}")
            break

        response_dict = response.json()
        for item in response_dict["items"]:
            yield item

        headers["pageToken"] = response_dict.get("nextPageToken")
        if not headers["pageToken"]:
            break


def is_processable_coda_page(page: dict) -> bool:
    """Verifies the page being pulled is valid for content pull

    Args:
        page (dict): The metadata of the page targeted for content pull

    Returns:
        bool: Whether the page is valid for content pull
    """
    is_page_valid = True
    author_email = page.get("updatedBy", {}).get("email")

    # Page pulled without a way for us to identify a user to link ideas to
    if not author_email:
        print(f"Email not found for page author")
        is_page_valid = False

    # Default page pulled which should not be checked for ideas
    if author_email == "codaquickstarts@gmail.com":
        print(f"Skipping page created by coda default environments")
        is_page_valid = False

    # Contents of page not extractable
    if page.get("contentType") != "canvas":
        print(
            f"is of type {page.get('contentType')} and content cannot be extracted"
        )
        is_page_valid = False

    return is_page_valid


def iter_all_processable_pages_in_doc(
    doc_id: str,
) -> Generator[dict, None, None]:
    """Creates a generator for the list pages endpoint of coda

    Args:
        doc (dicstrt): The id of the doc from which pages are listed

    Yields:
        Generator[dict[any]]: iterable of coda page dicts in responses
            from the endpoint
    """
    for page in iter_content_metadata_pulled_from_coda(
        url=f"{CODA_BASE_URL}/docs/{doc_id}/pages",
    ):
        print(f"Page: {page['name']}")
        if not is_processable_coda_page(page):
            print(PAGE_RESULTS_BORDER)
            continue

        yield page


def iter_all_docs() -> Generator[dict, None, None]:
    """Creates a generator for the list docs endpoint of coda

    Yields:
        Generator[dict]: iterable of coda doc dicts in responses
            from the endpoint
    """
    for doc in iter_content_metadata_pulled_from_coda(
        url=f"{CODA_BASE_URL}/docs",
    ):
        print(f"Retrieved Doc: {doc['name']}")
        yield doc


def create_ipcopilot_ingestion_payload_from_coda_page(
    page_dict: dict,
    doc_dict: dict,
    content: str,
) -> dict:
    """Create a payload in the payload format expected by IP Copilot's
        ingest endpoint

    Args:
        page_dict (dict): dict that contains required information about a
            targeted page in coda
        doc_dict (dict): dict that contains required information about a
            targeted doc in coda
        content (str): exported page content from codas export page process

    Returns:
        dict: dict in the format expected by IP Copilot's ingest endpoint
    """
    print(f"Creating {page_dict['name']}'s ingestion payload...")
    updatedAt_dt = datetime.datetime.strptime(
        page_dict["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    updatedAt_dt_str_formatted = updatedAt_dt.strftime("%Y-%m-%d %H:%M:%S")
    nlp_payload = {
        "author": page_dict["updatedBy"][
            "email"
        ],  # This is the latest author at the time of ingestion
        "source": "coda",
        "email": page_dict["updatedBy"]["email"],
        "comment_text": content,
        "comment_link": page_dict["browserLink"],
        "content_title": "",
        "content_link": None,
        "discussion_link": page_dict["browserLink"],
        "context_link": doc_dict["browserLink"],
        "response_flag": True,
        "created_at": updatedAt_dt_str_formatted,
    }
    print(f"Sending {page_dict['name']} ingestion payload to IP Copilot...")
    return nlp_payload


def send_to_ipcopilot_ingestion_endpoint(payloads: list[dict]):
    """Sends a list of payloads to IP Copilot's ingest endpoint

    Args:
        payloads (list[dict]): The list of formatted payloads containing
            ingestable markdown for idea extraction
    """
    response = None
    retries = 0
    n_payloads = len(payloads)
    default_retry_wait_seconds = 15
    ingest_api_path =
    try:
        for idx, payload in enumerate(payloads):
            while response is None or (
                response.status_code == 429 and IPCOPILOT_MAX_RETRIES > retries
            ):
                response = requests.post(
                    ingest_api_path,
                    json=payload,
                    headers=get_ipcopilot_headers(),
                    allow_redirects=False,
                )
                # Handle the response
                status_msg = (
                    f"Payload {idx + 1} of {n_payloads} processed successfully"
                )
                if response.status_code == 429:
                    print(
                        f"Request failed with rate limit status {response.status_code}: {response.text}"
                    )
                    retry_sleep_time = response.headers.get(
                        "Retry-After", default_retry_wait_seconds
                    )
                    print(f"retrying in {retry_sleep_time} seconds")
                    time.sleep(int(retry_sleep_time))
                    retries += 1

                elif response.status_code >= 400:
                    status_msg = f"Request failed with status {response.status_code}: {response.text}"

            if IPCOPILOT_MAX_RETRIES < retries:
                status_msg = f"Max retries exceeded for Payload {idx + 1} of {n_payloads}"

            print(status_msg)
    except Exception as e:
        error_msg = f"An error occured with IP Copilot processing {e}"
        print(error_msg)


def validate_args_and_env():
    """Validates all global vars required for the script are set

    Raises:
        ValueError: A value is missing from one or more required vars
    """
    missing_values = []
    if IPCOPILOT_ORG_API_KEY is None:
        missing_values.append("IPCOPILOT_ORG_API_KEY")
    if CODA_API_TOKEN is None:
        missing_values.append("CODA_API_TOKEN")
    if IPCOPILOT_API_URL is None:
        missing_values.append("IPCOPILOT_API_URL")

    if missing_values:
        raise ValueError(
            "The following vars are not set: "
            f"{', '.join([str(env_var_name) for env_var_name in missing_values])}\n"
            "Please set in environment vars or pass in via script arguments"
        )


def main():
    """
    Pulls page data from conda and sends it to IP Copilot's Ingest API
        for processing
    """
    validate_args_and_env()

    total_docs_processed = 0
    total_pages_pulled = 0
    total_pages_processed = 0
    print(DOC_RESULTS_BORDER)
    for doc in iter_all_docs():
        total_docs_processed += 1
        print(DOC_RESULTS_BORDER)
        doc_id = doc["id"]
        for page in iter_all_processable_pages_in_doc(doc_id):
            total_pages_pulled += 1

            # Extract page contents
            page_content = get_page_content_from_coda(doc_id, page)

            # Send page contents to IP Copilot ingestion payload
            if page_content is not None:
                nlp_payload = create_ipcopilot_ingestion_payload_from_coda_page(
                    page_dict=page, doc_dict=doc, content=page_content
                )
                send_to_ipcopilot_ingestion_endpoint(payloads=[nlp_payload])
                total_pages_processed += 1
            print(PAGE_RESULTS_BORDER)
        print(DOC_RESULTS_BORDER)
    print(
        "\n"
        + DOC_RESULTS_BORDER
        + f"\nTotal docs processed: {total_docs_processed}\n"
        + f"Total pages processed/pulled: {total_pages_processed}/{total_pages_pulled}\n"
        + DOC_RESULTS_BORDER
    )


if __name__ == "__main__":
    _parser = argparse.ArgumentParser(
        description="Set API tokens and domain if not already set in environment variables."
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
        "--coda-api-token",
        type=str,
        default=None,
        help=(
            "coda api token, alternatively can be set with "
            "env CODA_API_TOKEN"
        ),
    )
    _parser.add_argument(
        "--ipcopilot-api-url",
        type=str,
        default=None,
        help=(
            "ipcopilot api url, alternatively can be set with "
            "env IPCOPILOT_API_URL"
        ),
    )

    _args = _parser.parse_args()

    # Use argparse values if they are passed in, otherwise use environment variables
    if _args.ipcopilot_org_api_key:
        IPCOPILOT_ORG_API_KEY = _args.ipcopilot_org_api_key
    if _args.coda_api_token:
        CODA_API_TOKEN = _args.coda_api_token
    if _args.ipcopilot_api_url:
        IPCOPILOT_API_URL = _args.ipcopilot_api_url
    main()
