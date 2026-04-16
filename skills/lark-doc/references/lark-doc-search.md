# docs +search (Cloud search: Docs / Wiki / Sheets)

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

Search cloud objects using Search v2 API as a **user** identity.

Although the endpoint is named `doc_wiki/search`, results can include `SHEET` objects too. Use it as a discovery entrypoint for cloud objects - locate documents, wiki nodes, spreadsheets, and objects users describe as "tables / reports" - then switch to the corresponding domain skill for object-level operations.

## Recommended call

Keyword search:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/search/v2/doc_wiki/search
- body:
  {
    "query": "quarterly summary",
    "doc_filter": {},
    "wiki_filter": {},
    "count": 15
  }
- as: user
```

Filter by last opened time:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/search/v2/doc_wiki/search
- body:
  {
    "query": "proposal",
    "doc_filter": {
      "open_time": {
        "start_time": "1727136000",
        "end_time": "1735084799"
      }
    },
    "wiki_filter": {
      "open_time": {
        "start_time": "1727136000",
        "end_time": "1735084799"
      }
    },
    "count": 15
  }
- as: user
```

Empty search (return recent browsing):
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/search/v2/doc_wiki/search
- body:
  {
    "doc_filter": {},
    "wiki_filter": {},
    "count": 15
  }
- as: user
```

Paginate:
```
Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/search/v2/doc_wiki/search
- body:
  {
    "query": "proposal",
    "doc_filter": {},
    "wiki_filter": {},
    "count": 15,
    "page_token": "<PAGE_TOKEN>"
  }
- as: user
```

## API request details

```
POST /open-apis/search/v2/doc_wiki/search
```

## Parameters (body)

| Parameter | Required | Description |
|------|----------|-------------|
| `query` | No | Keyword query. Default is keyword matching. Empty or omitted means blank search. **Whenever there is a keyword, pass it via `query`; do not use positional arguments.** |
| `doc_filter` | No | Filter object applied to doc results |
| `wiki_filter` | No | Filter object applied to wiki results |
| `count` | No | Page size (default 15, max 20) |
| `page_token` | No | Pagination token (use with `has_more`) |

> **Key constraint: search keywords must be passed via `query`.**
> Correct: `{ "query": "proposal" }`
> Wrong: placing the keyword directly without the `query` key.

## Result Routing

- `result_meta.doc_types == SHEET`: spreadsheet, continue with `lark-sheets`
- Other types: continue with the matching skill or API

## Decision Rules

- Query intent: treat input as keyword search by default. When the user says "title is `X`", return API results directly first; only do client-side exact title filtering when the user explicitly asks for "title exactly equals `X`". Before doing exact matching, strip highlight tags from `title_highlighted`.
- Entrypoint choice: when the user says "find spreadsheet title" or "search for a report", default to `docs +search`. Do not misuse `sheets +find` for cross-file searches.
- Pagination: return first page by default. Only continue paginating when the user explicitly asks for all results.
- Full scan cap: even when the user asks for all results, fetch up to **5 pages** per round first (approximately 100 results max). Report current progress and let the user decide whether to continue.
- Relative time: convert expressions like "3 to 6 months ago" into explicit absolute Unix timestamps before writing them into filter.
- Cross-skill handoff: for spreadsheet targets, return title/URL/token and continue in `lark-sheets`.

## Permissions

| Operation | Required scope |
|-----------|----------------|
| Search cloud objects (Docs / Wiki / Sheets discovery) | `search:docs:read` |
