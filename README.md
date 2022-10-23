## Information
This is a relay server that shows more commit info for Discord webhooks.

The webhook is exactly like the [Discord's Github-Compatible webhook](https://discord.com/developers/docs/resources/webhook#execute-githubcompatible-webhook) but includes:
- `x` file changes, `x` additions, `x` deletions per commit.
- Hyperlink for commit author.
- Can show info for up to [around 5000 commits](https://docs.github.com/en/developers/apps/building-github-apps/rate-limits-for-github-apps) instead of max 5 per push.
- Repository's owner name in the embed's title.

Demo: https://i.imgur.com/nyqJfSx.png

## Running
1. Make a new project on [Deta](https://web.deta.sh/home).
2. Click the 'Deploy to Deta' button on this repo.
3. Select your project and enter the environment variables.
   - `DISCORD_WEBHOOK_URL` is https://discord.com/api/webhooks/{id}/{token}
      - Edit Discord channel -> Integrations -> New webhook -> Copy webhook URL
   - `GITHUB_ACCESS_TOKEN` is text that looks like `github_pat_{token}`, required if repo's are private.
      - Github settings -> Developer settings -> Personal access tokens -> Generate new token -> Set `Contents` permission to read-only -> Click generate -> Copy the token text.
4. Once deployed, set the repo's `push` event webhook to point to this page of the Micro's URL: [https://{id}.deta.dev/github](https://deta.sh)
     - Repo settings -> Webhooks -> Add new webhook -> Write in `Payload URL`

## Deploy
Click the following button to deploy this Micro in your own Deta project:

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy)
