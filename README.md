## Information
This is a relay server that shows more commit info for Discord webhooks.

The webhook is exactly like the [Discord's Github-Compatible webhook](https://discord.com/developers/docs/resources/webhook#execute-githubcompatible-webhook) but includes:
- `x` file changes, `x` additions, `x` deletions per commit.
- Hyperlink for commit author.
- Can show info for up to [around 5000 commits](https://docs.github.com/en/developers/apps/building-github-apps/rate-limits-for-github-apps) instead of max 5 per push.
- Repository's owner name in the embed's title.

Demo: https://i.imgur.com/nyqJfSx.png

## Running
1. Run `git clone https://github.com/imptype/github-discord-webhook` to clone this repository.
2. Run `cd github-discord-webhook` to go into the right folder.
3. Run `curl -fsSL https://get.deta.dev/space-cli.sh | sh` in Terminal to install Space CLI.
4. Run `space login` and enter your access token when prompted.
    - Access Tokens can be generated from https://deta.space -> Settings.
5. Run `space new` and enter an app name.
6. Run `space push` to upload the files to Deta Space.
8. Go to https://deta.space and update the environemnt variables in your app's settings.
   - `DISCORD_WEBHOOK_URL` is https://discord.com/api/webhooks/{id}/{token}
      - Edit Discord channel -> Integrations -> New webhook -> Copy webhook URL
   - `GITHUB_ACCESS_TOKEN` is text that looks like `github_pat_{token}`, required if repo's are private.
      - Github settings -> Developer settings -> Personal access tokens -> Generate new token -> Set `Contents` permission to read-only -> Click generate -> Copy the token text.
8. Set the repo's `push` event webhook to point to this page of the aoo's URL: [https://{app_name}-1-{a1234567}.deta.space](https://deta.soace)
   - Repo settings -> Webhooks -> Add new webhook -> Write in `Payload URL`
   - URL can be found/opened by clicking on your app in https://deta.space.
     
## Deploy
Coming soon to Discovery...?
