# workflow-disable

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Disable an automated workflow in Base.

## Recommended call

Call MCP tool `lark_api`:
- method: PATCH
- path: /open-apis/base/v3/bases/{base_token}/workflows/{workflow_id}/disable
- body:
  ```json
  {}
  ```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |
| `workflow_id` | Yes | Workflow ID starting with `wkf` (path param) |

## API request details

```
PATCH /open-apis/base/v3/bases/{base_token}/workflows/{workflow_id}/disable
```

Note: Pass an empty JSON body `{}` — a nil body may cause a server timeout.

## Key return fields

| Field | Description |
|-------|-------------|
| `workflow_id` | Workflow unique identifier |
| `status` | Always `disabled` after this operation |

## Workflow

This is a write operation; confirm with the user before execution.

1. Confirm `base_token` and `workflow_id` with the user.
2. Execute the call.
3. Confirm the returned `status` is `disabled`.

## Pitfalls

- `workflow_id` starts with `wkf`; do not confuse it with `table_id` (starts with `tbl`) — this causes `[2200] Internal Error`.
- `/disable` is the last path segment, not a body field.
- PATCH body must not be nil; pass `{}`.

## References

- [lark-base-workflow-enable.md](lark-base-workflow-enable.md) — enable workflow
- [lark-base-workflow-list.md](lark-base-workflow-list.md) — list all workflows
