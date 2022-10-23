## Information
This is a relay server that shows more commit info for Discord webhooks.

The webhook is exactly like the [Discord's Github-Compatible webhook](https://discord.com/developers/docs/resources/webhook#execute-githubcompatible-webhook) but includes:
- `x` file changes, `x` additions, `x` deletions per commit.
- Hyperlink for commit author.
- Can show info for up to [around 5000 commits](https://docs.github.com/en/developers/apps/building-github-apps/rate-limits-for-github-apps) instead of max 5 per push.
- Repository's owner name in the embed's title.

## Demo
![](https://i.imgur.com/nyqJfSx.png)

## Deploy
Click the following button to deploy this Micro in your own Deta project:

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy)
