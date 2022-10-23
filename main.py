import os
import asyncio
import aiohttp
from fastapi import FastAPI, Request, Response, status

app = FastAPI()
webhook = os.getenv('DISCORD_WEBHOOK_URL')
token = os.getenv('GITHUB_ACCESS_TOKEN', None)
base_url = 'https://api.github.com/repos/{}/commits/{}'
headers = {'Authorization' : 'Bearer {}'.format(token)} if token else None

@app.get('/')
async def root():
  return 'Hello World!'

def chunk_items(items, n): 
  for i in range(0, len(items), n):
    yield items[i:i+n]
    
def chunk_text(texts, n):
  chars = 0
  start = 0
  for i, text in enumerate(texts):
    chars += len(text)
    if chars > n:
      yield texts[start:i]
      chars = len(text)
      start = i
  yield texts[start:]

def grammar_text(n, name):
  if n == 1:
    name = name.rstrip('s')
  return '{:,} {}'.format(n, name)

def short_text(text):
  if len(text) > 50:
    return text[:47] + '...'
  return text

async def get_commit(session, user_repo, commit_id):
  url = base_url.format(user_repo, commit_id)
  async with session.get(url, headers = headers) as resp:
    data = await resp.json()
  return {
    'id' : data['sha'],
    'message' : data['commit']['message'],
    'author' : data['author']['login'],
    'author_url' : data['author']['html_url'],
    'link' : data['html_url'],
    'files' : len(data['files']),
    'additions' : data['stats']['additions'],
    'deletions' : data['stats']['deletions']
  }
  
@app.post('/github')
async def github(request : Request, response : Response):
  data = await request.json()
  
  user_repo = data['repository']['full_name']
  branch = data['ref'].split('/')[-1]
  head_url = data['head_commit']['url']
  commit_ids = [
    commit['id']
    for commit in data['commits']
  ]
  
  async with aiohttp.ClientSession() as session:
    commits = await asyncio.gather(*[
      get_commit(session, user_repo, commit_id)
      for commit_id in commit_ids
    ])

    entries = [
      '\n'.join([
        '{} {} - {}',
        '⤷ {} changed with {} and {}.'
      ]).format(
        '[`{}`]({})'.format(commit['id'][:7], commit['link']),
        short_text(commit['message']),
        '[{}]({})'.format(commit['author'], commit['author_url']),
        grammar_text(commit['files'], 'files'),
        grammar_text(commit['additions'], 'additions'),
        grammar_text(commit['deletions'], 'deletions')
      )
      for commit in commits
    ]

    # order by latest, max 4096 chars in embed desc
    entries.reverse()
    chunks = list(chunk_text(entries, 4096))

    embeds = [
      {
        'title' : '[{}:{}] {} new commits {}'.format(
          user_repo, 
          branch, 
          len(entries),
          (
            '' if len(chunks) == 1
            else '({}/{})'.format(i + 1, len(chunks))
          )
        ),
        'url' : head_url + (
          '' if len(chunks) == 1
          else '?{}'.format(i) # prevent embeds merging
        ),
        'description' : '\n'.join(entry for entry in chunk),
        'color' : 0x7289da
      }
      for i, chunk in enumerate(chunks)
    ]

    # max 10 embeds per message
    chunks = chunk_items(embeds, 10)
    
    payloads = [
      {
        'embeds' : embeds
      }
      for embeds in chunks
    ]

    resps = [
      (await session.post(webhook, json = payload)).status
      for payload in payloads
    ]
    
  if all(resp == 204 for resp in resps):
    response.status_code = status.HTTP_200_OK
  else:
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
