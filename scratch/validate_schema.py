import urllib.request, json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

raed_url = 'https://raw.githubusercontent.com/SallaApp/theme-raed/master/twilight.json'
raed = json.loads(urllib.request.urlopen(raed_url).read().decode('utf-8'))

with open('twilight.json', 'r', encoding='utf-8') as f:
    local = json.load(f)

print("=== CHECKING TOP LEVEL ===")
for k in local:
    if k not in raed:
        print(f"Key in local but not in Raed: {k}")

# Check author_email, support_url, repository
for f in ['name', 'repository', 'author_email', 'support_url', 'description']:
    print(f"{f}: local={type(local.get(f))}, raed={type(raed.get(f))}")
    print(f"  local val: {local.get(f)}")
    print(f"  raed val: {raed.get(f)}")

print("\n=== CHECKING SETTINGS ===")
print(f"Local settings count: {len(local.get('settings', []))}")
print(f"Raed settings count: {len(raed.get('settings', []))}")

for i, s in enumerate(local.get('settings', [])):
    if not isinstance(s, dict):
        print(f"Setting {i} is not a dict!")
    elif 'id' not in s or 'type' not in s:
        print(f"Setting {i} missing id or type: {s}")

print("\n=== CHECKING COMPONENTS ===")
print(f"Local components count: {len(local.get('components', []))}")
print(f"Raed components count: {len(raed.get('components', []))}")

for i, c in enumerate(local.get('components', [])):
    path = c.get('path')
    fields = c.get('fields', [])
    print(f"Component {i}: path={path}, fields_count={len(fields)}, has_icon={'icon' in c}, has_title={'title' in c}")
    for j, fld in enumerate(fields):
        if not isinstance(fld, dict):
            print(f"  Field {j} in {path} is not a dict!")
        elif 'type' not in fld:
            print(f"  Field {j} in {path} missing type: {fld}")
