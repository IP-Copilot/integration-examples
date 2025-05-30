#!/bin/bash

curl -X POST <IPCOPILOT_INGESTION_ENDPOINT> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <IPCOPILOT_ORG_API_KEY>" \
  -d '[
    {
      "author": "fake_user_id",
      "source": "fake_source",
      "email": "fake_email@email.com",
      "comment_text": "fake comment test",
      "comment_link": "https://fake-url.com",
      "content_title": "",
      "content_link": null,
      "discussion_link": null,
      "context_link": "https://another-fake-url.com",
      "created_at": <datetime in "%Y-%m-%d %H:%M:%S" format>
    }
  ]'