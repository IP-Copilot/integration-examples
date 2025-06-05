# Coda Integration Examples
This folder provides examples of pulling data from Coda, preparing it for ingestion, and sending it to the IP Copilot Ingestion API.

## Setup

### Dependencies
Coda example requires:

- Python (>= 3.10)

### Installation
1. Install requirements
  ```bash
  pip install requirements.txt
  ```

2. (optional) Create your `.env` file
  ```
  # IP Copilot API Config
  IPCOPILOT_INGESTION_ENDPOINT = <IPCOPILOT_INGESTION_ENDPOINT>
  IPCOPILOT_ORG_API_KEY = <IPCOPILOT_ORG_API_KEY>

  # Coda Config
  CODA_API_TOKEN = <CODA_API_TOKEN>
  ```


## Running the script
Run command:
`python coda_ingestion.py`

Run with optional parameters:
```bash
python coda_ingestion.py \
  --ipcopilot-ingestion-endpoint "<IPCOPILOT_INGESTION_ENDPOINT>" \
  --ipcopilot-org-api-key "<IPCOPILOT_ORG_API_KEY>" \
  --coda-api-token "<CODA_API_TOKEN>"
```
