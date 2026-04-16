# im reactions

> **Prerequisite:** Read [../lark-shared/SKILL.md](../../lark-shared/SKILL.md) first. LarkSkill MCP server must be connected.

This reference covers the IM reaction MCP calls:

- `im.reactions.create` → `POST /open-apis/im/v1/messages/{message_id}/reactions`
- `im.reactions.list` → `GET /open-apis/im/v1/messages/{message_id}/reactions`
- `im.reactions.delete` → `DELETE /open-apis/im/v1/messages/{message_id}/reactions/{reaction_id}`
- `im.reactions.batch_query` → `POST /open-apis/im/v1/messages/reactions/batch_query`

## Common Notes

- `message_id` is always an IM message ID such as `om_xxx`
- `reaction_id` is the unique record ID returned after a reaction is added
- `reaction_type.emoji_type` is the enum-like emoji identifier used by both write and read APIs
- Reaction APIs return **reaction records**, not only aggregated counts

## create

Add a reaction to one message.

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/{message_id}/reactions
- body:
  ```json
  { "reaction_type": { "emoji_type": "SMILE" } }
  ```

### Response

```json
{
  "reaction_id": "ZCaCIjUBVVWSrm5L-3ZTw_xxx",
  "operator": { "operator_id": "ou_xxx", "operator_type": "user" },
  "action_time": "1663054162546",
  "reaction_type": { "emoji_type": "SMILE" }
}
```

## list

List reaction records on one message.

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages/{message_id}/reactions
- params: `{ "page_size": 50 }`

Filter by emoji type:

Call MCP tool `lark_api`:
- method: GET
- path: /open-apis/im/v1/messages/{message_id}/reactions
- params: `{ "reaction_type": "SMILE", "user_id_type": "open_id" }`

### Request Parameters (query)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `reaction_type` | No | Filter by one emoji type such as `SMILE` or `LAUGH` |
| `page_size` | No | Number of records per page. Default is 20 |
| `page_token` | No | Pagination token from the previous page |
| `user_id_type` | No | Returned operator ID type when `operator_type=user`: `open_id`, `union_id`, or `user_id` |

## delete

Delete one specific reaction record from one message.

Call MCP tool `lark_api`:
- method: DELETE
- path: /open-apis/im/v1/messages/{message_id}/reactions/{reaction_id}

## batch_query

Query reactions for multiple messages in one request.

Call MCP tool `lark_api`:
- method: POST
- path: /open-apis/im/v1/messages/reactions/batch_query
- params: `{ "user_id_type": "open_id" }`
- body:
  ```json
  {
    "queries": [
      { "message_id": "om_xxx" },
      { "message_id": "om_yyy", "page_token": "<PAGE_TOKEN>" }
    ],
    "page_size_per_message": 10,
    "reaction_type": "LAUGH"
  }
  ```

### Request body fields

| Field | Required | Description |
|-------|----------|-------------|
| `queries` | Yes | Array of target messages |
| `queries[].message_id` | No | Message ID to query |
| `queries[].page_token` | No | Continuation token for that message |
| `page_size_per_message` | No | Max reactions returned per message |
| `reaction_type` | No | Filter by one emoji type |

## `emoji_type` Field

- `im.reactions.create`: request and response use `reaction_type.emoji_type`
- `im.reactions.list`: request filter uses `reaction_type`, response uses `reaction_type.emoji_type`
- `im.reactions.batch_query`: request filter uses top-level `reaction_type`

## Complete `emoji_type` List

Current count: 185. Source: `https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message-reaction/emojis-introduce`

```text
OK, THUMBSUP, THANKS, MUSCLE, FINGERHEART, APPLAUSE, FISTBUMP, JIAYI
DONE, SMILE, BLUSH, LAUGH, SMIRK, LOL, FACEPALM, LOVE
WINK, PROUD, WITTY, SMART, SCOWL, THINKING, SOB, CRY
ERROR, NOSEPICK, HAUGHTY, SLAP, SPITBLOOD, TOASTED, GLANCE, DULL
INNOCENTSMILE, JOYFUL, WOW, TRICK, YEAH, ENOUGH, TEARS, EMBARRASSED
KISS, SMOOCH, DROOL, OBSESSED, MONEY, TEASE, SHOWOFF, COMFORT
CLAP, PRAISE, STRIVE, XBLUSH, SILENT, WAVE, WHAT, FROWN
SHY, DIZZY, LOOKDOWN, CHUCKLE, WAIL, CRAZY, WHIMPER, HUG
BLUBBER, WRONGED, HUSKY, SHHH, SMUG, ANGRY, HAMMER, SHOCKED
TERROR, PETRIFIED, SKULL, SWEAT, SPEECHLESS, SLEEP, DROWSY, YAWN
SICK, PUKE, BETRAYED, HEADSET, EatingFood, MeMeMe, Sigh, Typing
Lemon, Get, LGTM, OnIt, OneSecond, VRHeadset, YouAreTheBest, SALUTE
SHAKE, HIGHFIVE, UPPERLEFT, ThumbsDown, SLIGHT, TONGUE, EYESCLOSED, RoarForYou
CALF, BEAR, BULL, RAINBOWPUKE, ROSE, HEART, PARTY, LIPS
BEER, CAKE, GIFT, CUCUMBER, Drumstick, Pepper, CANDIEDHAWS, BubbleTea
Coffee, Yes, No, OKR, CheckMark, CrossMark, MinusOne, Hundred
AWESOMEN, Pin, Alarm, Loudspeaker, Trophy, Fire, BOMB, Music
XmasTree, Snowman, XmasHat, FIREWORKS, 2022, REDPACKET, FORTUNE, LUCK
FIRECRACKER, StickyRiceBalls, HEARTBROKEN, POOP, StatusFlashOfInspiration, 18X, CLEAVER, Soccer
Basketball, GeneralDoNotDisturb, Status_PrivateMessage, GeneralInMeetingBusy, StatusReading, StatusInFlight, GeneralBusinessTrip, GeneralWorkFromHome
StatusEnjoyLife, GeneralTravellingCar, StatusBus, GeneralSun, GeneralMoonRest, MoonRabbit, Mooncake, JubilantRabbit
TV, Movie, Pumpkin, BeamingFace, Delighted, ColdSweat, FullMoonFace, Partying
GoGoGo, ThanksFace, SaluteFace, Shrug, ClownFace, HappyDragon
```

## References

- [lark-im](../SKILL.md) - all IM commands
- [lark-shared](../../lark-shared/SKILL.md) - authentication and global parameters
- Official emoji doc: `https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message-reaction/emojis-introduce`
