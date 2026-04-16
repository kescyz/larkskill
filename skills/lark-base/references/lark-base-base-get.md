# base-get

> **Prerequisite:** Read [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) for auth, global flags, and safety rules.

Read details of a Base.

## Recommended call

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/base/v3/bases/{base_token}

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `base_token` | Yes | Base token (path param) |

## API request details

```
GET /open-apis/base/v3/bases/{base_token}
```

## Response highlights

- Returns `base`, usually including `base_token / name / url`.

## Pitfalls

- ⚠️ Confirm input is `base_token`, not `workspace_token`.
- ⚠️ If input comes from `/wiki/...`, do not pass `wiki_token` directly as `base_token`.
  If you get `param baseToken is invalid` or `base_token invalid`, first call
  `lark_api GET /open-apis/wiki/v2/spaces/get_node` to get `node.obj_token`, then retry.

## References

- [lark-base-workspace.md](lark-base-workspace.md) - base index
