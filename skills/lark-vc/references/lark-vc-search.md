# vc — search

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) first for authentication, global parameters, and safety rules.

Search ended historical meeting records by keyword, time range, organizer, participants, and room filters. Read-only operation.

Calls `POST /open-apis/vc/v1/meetings/search`.

## Typical triggers

Prefer `vc search` for requests like:
- meetings held today
- what meetings happened today
- recent meetings I attended
- meetings I held this week
- ended meetings
- historical meeting records

## MCP tool call

Keyword search:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/vc/v1/meetings/search
- body:
  {
    "query": "weekly meeting",
    "page_size": 15
  }
- as: user
```

Time range search:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/vc/v1/meetings/search
- body:
  {
    "start_time": "2026-03-10T00:00:00+08:00",
    "end_time": "2026-03-17T00:00:00+08:00",
    "page_size": 15
  }
- as: user
```

Filter by organizer, participant, or room:

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/vc/v1/meetings/search
- body:
  {
    "organizer_id": "ou_a",
    "start_time": "2026-03-10T00:00:00+08:00",
    "page_size": 15
  }
- as: user
```

Pagination (next page):

```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/vc/v1/meetings/search
- body:
  {
    "query": "weekly meeting",
    "page_size": 15,
    "page_token": "<PAGE_TOKEN>"
  }
- as: user
```

## Parameters (body)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | No | Keyword query |
| `start_time` | No | Start time (ISO 8601) |
| `end_time` | No | End time (ISO 8601) |
| `organizer_id` | No | Organizer open_id |
| `participant_id` | No | Participant open_id |
| `room_id` | No | Room ID |
| `page_size` | No | Page size, default 15, max 30 |
| `page_token` | No | Pagination token |

## Constraints

1. At least one filter must be provided.
2. Only ended historical meetings are searchable.
3. User identity only (`as: "user"`); requires `vc:meeting.search:read`.
4. Use `has_more` + `page_token` for pagination.
5. Max searchable window per query is one month. Split longer ranges into monthly queries.

## Time formats

`start_time` and `end_time` accept ISO 8601:
- With timezone: `2026-03-10T14:00:00+08:00`
- Without timezone: `2026-03-10T14:00:00`
- Date only: `2026-03-10`

## Output

Response JSON contains `items`, `total`, `has_more`, and `page_token`.

## Pagination guidance

- If `has_more=true`, continue with returned `page_token`.
- Do not assume larger `page_size` means full result coverage.
- If `total < 50`, auto-paginate all results.
- If `total > 50`, confirm with user before full traversal.

## Next step from results

Use returned `meeting_id` to query notes — see [lark-vc-notes](lark-vc-notes.md).

## Common errors

| Error | Cause | Resolution |
|-------|-------|------------|
| must provide filter | no filters supplied | add at least one filter |
| invalid time format | malformed time field | use ISO 8601 |
| no future meetings found | vc search only covers ended meetings | use lark-calendar for schedules |
| insufficient scope | missing `vc:meeting.search:read` | re-authorize with required scope |

## References

- [lark-vc](../SKILL.md)
- [lark-vc-notes](lark-vc-notes.md)
- [lark-shared](../../lark-shared/SKILL.md)
