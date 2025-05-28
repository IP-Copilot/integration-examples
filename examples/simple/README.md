# simple integration
This script shows how to create a general payload to send to IP Copilot's ingestion API endpoint

## IP Copilot Payload breakdown
Please see the [top level README's section for more details](../../README.md#IP-Copilot-Payload-breakdown)

## Setup
1. Create your `.env` file
  ```
  # IP Copilot API Config
  IPCOPILOT_API_URL = <IPCOPILOT_API_URL>
  IPCOPILOT_ORG_API_KEY = <IPCOPILOT_ORG_API_KEY>
  ```

## Running the script
Run command:
`python simple_ingestion.py`

Run with optional parameters:
```
python simple_ingestion.py --ipcopilot-api-url <IPCOPILOT_API_URL> --ipcopilot-org-api-key <IPCOPILOT_ORG_API_KEY>
```