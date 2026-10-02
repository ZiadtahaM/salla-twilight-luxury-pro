import requests
import json
import io

with open('node_modules/.salla-cli', 'r', encoding='utf-8') as f:
    cli_data = json.load(f)

upload_url = cli_data['upload_url']
draft_id = cli_data['draft_id']
store_id = cli_data['store_id']

headers = {'Store-Identifier': str(store_id), 'User-Agent': 'Salla-CLI'}

# 1. Test uploading ar.json
with open('src/locales/ar.json', 'rb') as f_in:
    files = {'file': ('ar.json', f_in, 'application/json')}
    data = {'path': 'src/locales', 'draft_id': draft_id}
    res = requests.post(upload_url, files=files, data=data, headers=headers)
    print(f'Upload ar.json -> Status {res.status_code}: {res.text}')

# 2. Test uploading index.twig
with open('src/views/pages/index.twig', 'rb') as f_in:
    files = {'file': ('index.twig', f_in, 'text/plain')}
    data = {'path': 'src/views/pages', 'draft_id': draft_id}
    res = requests.post(upload_url, files=files, data=data, headers=headers)
    print(f'Upload index.twig -> Status {res.status_code}: {res.text}')

# 3. Test uploading minimal master.twig
minimal_twig = """<!DOCTYPE html>
<html lang="{{ user.language.code }}" dir="{{ user.language.dir }}">
<head>
    <meta charset="UTF-8">
    <title>{{ store.name }}</title>
    {{ theme.head|raw }}
</head>
<body class="{{ user.language.dir }}">
    {% block content %}{% endblock %}
    {{ theme.foot|raw }}
</body>
</html>"""

files = {'file': ('master.twig', io.BytesIO(minimal_twig.encode('utf-8')), 'text/plain')}
data = {'path': 'src/views/layouts', 'draft_id': draft_id}
res = requests.post(upload_url, files=files, data=data, headers=headers)
print(f'Upload minimal master.twig -> Status {res.status_code}: {res.text}')
