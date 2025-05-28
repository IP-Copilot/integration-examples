# coda integration
This coda is used to pull and relay data from pages within a coda environment to the IP Copilots ingestion API

## Setup
1. Create your `.env` file
  ```
  # IP Copilot API Config
  IPCOPILOT_API_URL = <IPCOPILOT_API_URL>
  IPCOPILOT_ORG_API_KEY = <IPCOPILOT_ORG_API_KEY>

  # Coda Config
  CODA_API_TOKEN = <CODA_API_TOKEN>
  ```

## Running the script
Run command:
`python coda_ingestion.py`

Run with optional parameters:
```
python coda_ingestion.py --ipcopilot-api-url <IPCOPILOT_API_URL> --ipcopilot-org-api-key <IPCOPILOT_ORG_API_KEY> --coda-api-token <CODA_API_TOKEN>
```

