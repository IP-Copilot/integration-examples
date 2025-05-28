# curl example
This folder shows how to send a payload  to IP Copilot's ingestion API endpoint using curl

## [IP Copilot Payload breakdown](../../README.md#IP-Copilot-Payload-breakdown)

## Running the commnd
1. Replace values in the example curl command in `curl_command.txt`
  a. Replace <IPCOPILOT_API_URL> with ingestion api link
  b. Replace <IPCOPILOT_ORG_API_KEY> with your IP Copilot generated API key
  c. Replace the values within the payload in the command with desired values
2. copy and paste the command into your terminal

Upon successful send the response will contain a json formatted string with info about what was stored within the the IPCopilot system.