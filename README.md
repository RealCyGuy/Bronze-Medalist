# Bronze Medalist

[![Codacy Badge](https://img.shields.io/codacy/grade/fa948ef2806a4d379f7079a4ce9e938b?style=for-the-badge)](https://www.codacy.com/gh/RealCyGuy/Bronze-Medalist/dashboard)
[![Notion](https://img.shields.io/badge/Notion-:\)-cd7f32?style=for-the-badge&logo=notion)](https://www.notion.so/3bbde558b1dd4a0e8f708b8a91efde01?v=977cb57992614180b0538865a679b8d0)

> Discord economy bot with slash commands made with discord.py.

## Invite link

You can find a public instance of the
bot [here](https://discord.com/api/oauth2/authorize?client_id=820018018490646538&permissions=2048&scope=applications.commands%20bot)!

## Hosting

You can host on heroku or locally. In any case, you need to have a `.env` with `TOKEN` (from discord developer portal)
and `DETA_KEY` (from <https://deta.sh>).

Make sure to enable all priviliged intents.

Then you can run `bot.py` to start the bot.

## Other `.env`s

- `TESTING_GUILD_ID` - For development to add slash commands quicker.
- `DETABASE_NAME` - Name of deta base for multiple bases in one deta project.
- `EVENT_STARTER_IDS` - Ids for event starters. To start events, the bot needs the manage messages and manage roles
  permissions.
- `PREFIX` - Custom prefix for starting events and using the jishaku module. Defaults to b.
- `JISHAKU_NO_UNDERSCORE` - Don't use underscores for jishaku's repl if set to true.
- `INVITE` - Custom invite link (like <https://bronzemedalist.netlify.app/invite>) for the invite command.

## Events

Events are free medals that `EVENT_STARTER_IDS` can start. To start an event, use `(prefix)(event_name)` The events
are `last` and `react`. The bot will need extra permissions such as `send messages`, `delete messages`, etc.

## License

[MIT](https://github.com/RealCyGuy/Bronze-Medalist/blob/main/LICENSE.md) :)
