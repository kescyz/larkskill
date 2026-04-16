# larkskill

> LarkSkill — Lark/Feishu workspace skills for Claude Code via MCP.
> One plugin, all domains.

## Install

**Step 1: Set up MCP** (if not done already)

```bash
npx larkskill install
```

Or visit https://larkskill-portal.pages.dev/setup for manual config.

**Step 2: Add the skill registry and install**

```bash
/plugin marketplace add kescyz/larkskill
/plugin install larkskill
```

That's it — all Lark domains are available immediately.

## Domains Covered (11 skills)

| Skill | Description |
|---|---|
| `lark-base` | Bitable database management — tables, records, fields, views, permissions |
| `lark-base-formula` | Bitable formula reference and advanced field calculations |
| `lark-calendar` | Calendar events, attendees, scheduling |
| `lark-comment` | Document and Bitable comments |
| `lark-contacts` | Org directory, departments, user profiles |
| `lark-docs` | Lark Docs — create, read, update, block management |
| `lark-drive` | Drive files, folders, permissions, upload/download |
| `lark-messenger` | IM messages, group chats, notifications |
| `lark-sheets` | Spreadsheet data, formulas, styling |
| `lark-task` | Tasks, tasklists, subtasks, assignments |
| `lark-wiki` | Wiki spaces, nodes, content |

## Download (ZIP)

Download the latest skills bundle from the [releases page](https://github.com/kescyz/larkskill/releases/latest):

```
https://github.com/kescyz/larkskill/releases/latest/download/larkskill-skills-latest.zip
```

## Migration from v1 (kescyz/lark-skill-marketplace)

V1 continues to work. V2 requires MCP setup first — the key difference:

| | V1 | V2 |
|---|---|---|
| Auth | `lark-token-manager` MCP per app | Single `lsk_*` key, MCP handles tokens |
| Install | `/plugin install lark-base@lark-skill` | `/plugin install larkskill` (all skills) |
| Setup | Manual token flow | `npx larkskill install` |

V2 MCP setup: https://larkskill-portal.pages.dev/setup

## Contributing

1. Fork this repo
2. Edit the relevant `skills/lark-*/SKILL.md` or scripts
3. Open a PR — include a short description of the change and which Lark API it affects

## License

MIT
