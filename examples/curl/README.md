# curl example
This folder shows how to send a payload to IP Copilot's Ingestion Endpoint using curl.

## IP Copilot Payload Breakdown
Please see the [top level README's section for more details](../../README.md#IP-Copilot-Payload-Breakdown)

## Running the commnd
1. Replace values in the example curl command in `curl_command.sh`

    * Replace `<IPCOPILOT_INGESTION_ENDPOINT>` with ingestion api link

    * Replace `<IPCOPILOT_ORG_API_KEY>` with your IP Copilot generated API key

    * Replace the values within the payload in the command with desired values

2. Copy and paste the command into your terminal

3. Set `curl_command.sh` as an executable:
`chmod +x curl_command.sh`

4. Run command: `./curl_command.sh`
