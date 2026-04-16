# minutes — download

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first for authentication, global parameters, and safety rules.

Get a media download link for a minute's audio/video file (link valid for 1 day), or retrieve metadata to initiate download. Read-only operation.

## MCP tool call — get download link

```
Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/minutes/v1/minutes/{minute_token}/media
- params: { "minute_token": "obcnq3b9jl72l83w4f149w9c" }
- as: user
```

The response contains a `download_url` field with a pre-signed link valid for 1 day.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `minute_token` (path) | Yes | Minute token extracted from the minutes URL |

## Key Constraints

### 1. Minutes Must Have Completed Transcription

Audio/video files are only available for download after transcription is complete. If the minute is not ready, the API returns error `2091003`.

### 2. Download Link Valid for 1 Day

The `download_url` returned is valid for 1 day; obtain a new link after expiration.

### 3. Rate Limiting

API rate limit is 5 requests/second; be mindful of frequency when batch requesting.

### 4. Required Permissions

| Identity | Required Permission |
|----------|-------------------|
| user / bot | `minutes:minutes.media:export` |

## Response fields

| Field | Description |
|-------|-------------|
| `download_url` | Media file download link (valid for 1 day) |

## How to Get minute_token

| Source | Method |
|--------|--------|
| Minutes URL | Extract from the end of the URL, e.g. `https://sample.feishu.cn/minutes/obcnq3b9jl72l83w4f149w9c` → `obcnq3b9jl72l83w4f149w9c` |
| Minutes metadata query | Call `GET /open-apis/minutes/v1/minutes/{minute_token}` |
| Meeting notes query | Use lark-vc notes operation with `meeting_id` — the associated `minute_token` is in the response |

## Common Errors and Troubleshooting

| Symptom | Error Code | Root Cause | Solution |
|---------|-----------|------------|----------|
| Invalid parameter | 2091001 | minute_token format is incorrect | Check that the token is complete (24 characters) |
| Resource does not exist | 2091002 | Token does not exist | Confirm minute_token is correct |
| Minutes not ready | 2091003 | Transcription not complete | Wait for transcription to complete and retry |
| Resource deleted | 2091004 | Minutes has been deleted | Confirm the minutes file still exists |
| Insufficient permissions | 2091005 | No read access | Check access permissions for this minutes record |
| `missing required scope(s)` | — | App missing required scope | Authorize with scope `minutes:minutes.media:export` via `lark_auth_login` |

## Tips

- To get minutes note content (transcript, AI summary, etc.), use the [lark-vc notes operation](../../lark-vc/references/lark-vc-notes.md).
- When no specific output is requested, return the `download_url` to the user rather than attempting to stream the file through Claude.

## References

- [lark-minutes](../SKILL.md) — All Minutes operations
- [lark-vc-notes](../../lark-vc/references/lark-vc-notes.md) — Meeting notes query
- [lark-shared](../../lark-shared/SKILL.md) — Authentication and global parameters
