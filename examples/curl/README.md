# curl example
This folder shows how to send a payload  to IP Copilot's ingestion API endpoint using curl

## IP Copilot Payload breakdown
Please see the [top level README's section for more details](../../README.md#IP-Copilot-Payload-breakdown)

## Running the commnd
1. Replace values in the example curl command in `curl_command.txt`

    * Replace `<IPCOPILOT_API_URL>` with ingestion api link

    * Replace `<IPCOPILOT_ORG_API_KEY>` with your IP Copilot generated API key

    * Replace the values within the payload in the command with desired values

2. copy and paste the command into your terminal
3. Run command

Upon successful send the response will contain a json formatted string with info about what was stored within the the IPCopilot system.