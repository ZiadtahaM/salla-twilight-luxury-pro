import urllib.request, re

req = urllib.request.Request('https://docs.salla.dev/doc-422580', headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'\"content\":\"(.*?)\"', html)
    if match:
        content = match.group(1).replace(r'\n', '\n')
        print(content[:2000])
    else:
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        print(text[:2000])
except Exception as e:
    print(e)
