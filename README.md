# integration-examples
This repository provides example scripts for sending text-based data from popular tools to IP Copilot's Ingestion Endpoint. These scripts are designed to support workflows for capturing ideas—helping your organization foster a culture of continuous innovation.

## Setup
1. clone the repo

```bash
git clone https://github.com/IP-Copilot/integration-examples.git
```

2. Follow the instruction of the README.md file of your required application integration
  * [Simple example README](examples/simple/README.md)
  * [Curl example README](examples/curl/README.md)
  * [Coda example README](examples/coda/README.md)

## IP Copilot Payload Breakdown
A payload can be in a dictionary format or a list of dictionaries with the following structure
```
{
    "author": # The ID of the user submitting the comment.
    "source": # The origin/source of the comment (e.g. coda, slack, jira).
    "email": # The email address associated with the comment's author.
    "comment_text": # The text content (markdown) of the comment.
    "comment_link": # A URL linking directly to the comment in its original context.
    "content_title": # The title of the content being commented on, if applicable.
    "content_link": # Link to the content being commented on.
    "discussion_link": # A URL to the broader discussion thread or page.
    "context_link": # A supporting link to the context to which the comment is grouped in.
    "created_at": # The timestamp when the comment was created (format: %Y-%m-%d %H:%M:%S).
}
```
