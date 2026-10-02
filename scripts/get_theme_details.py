import requests
import json

with open(r'C:\Users\DevUser\.salla\config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

token = cfg['salla']['access_token']
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json',
    'User-Agent': 'Salla-CLI'
}

url = 'https://api.salla.dev/partners/v1/theme/1252059893'
print('Fetching theme info from:', url)
res = requests.get(url, headers=headers)
print('Status:', res.status_code)
if res.status_code == 200:
    data = res.json()
    print('Theme Info Keys:', list(data.get('data', {}).keys()))
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print('Error response:', res.text)
