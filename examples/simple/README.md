# simple integration
This folder provides a generic python script to send payload to IP Copilot's Ingestion Endpoint.

## IP Copilot Payload breakdown
Please see the [top level README's section for more details](../../README.md#IP-Copilot-Payload-breakdown)

## Setup
1. Install requirements
  ```bash
  pip install requirements.txt
  ```

2. (optional) Create your `.env` file
  ```
  # IP Copilot API Config
  IPCOPILOT_INGESTION_ENDPOINT = <IPCOPILOT_INGESTION_ENDPOINT>
  IPCOPILOT_ORG_API_KEY = <IPCOPILOT_ORG_API_KEY>
  ```

## Running the script
Run command:
`python simple_ingestion.py`

Run with optional parameters:
```bash
python simple_ingestion.py \
  --ipcopilot-ingestion-endpoint "<IPCOPILOT_INGESTION_ENDPOINT>" \
  --ipcopilot-org-api-key "<IPCOPILOT_ORG_API_KEY>"
```
