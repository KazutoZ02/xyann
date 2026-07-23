import urllib.request, json

req = urllib.request.Request('https://openrouter.ai/api/v1/models', headers={'User-Agent': 'Antigravity'})
resp = urllib.request.urlopen(req)
models = json.loads(resp.read())['data']

for m in models:
    name = m.get('name', '').lower()
    id_str = m.get('id', '')
    if 'gemma' in name or 'gemma' in id_str or 'nemotron' in name or 'nemotron' in id_str or 'laguna' in name or 'laguna' in id_str or 'gpt-oss' in name or 'gpt-oss' in id_str or 'north-mini' in name or 'north-mini' in id_str:
        print(f"{id_str} : {name}")
