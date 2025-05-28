# integration-examples
This repository provides example scripts for sending text-based data from popular tools to a IP Copilot's ingestion API endpoint. These scripts are designed to support workflows for capturing ideas—helping your organization foster a culture of continuous innovation.

## Setup
1. clone the repo
```
<Insert clone command here>
```
2. install requirements
```
pip install requirements.txt
```
3. Follow the instruction of the README.md file of your required application integration


## IP Copilot Payload breakdown
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