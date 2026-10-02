import urllib.request, json

raed_url = 'https://raw.githubusercontent.com/SallaApp/theme-raed/master/twilight.json'
raed = json.loads(urllib.request.urlopen(raed_url).read().decode('utf-8'))

with open('twilight.json', 'r', encoding='utf-8') as f:
    local = json.load(f)

print("Top-level keys comparison:")
print("Raed:", list(raed.keys()))
print("Local:", list(local.keys()))

print("\nDifferences in top-level keys:")
print("In local but not in Raed:", set(local.keys()) - set(raed.keys()))
print("In Raed but not in local:", set(raed.keys()) - set(local.keys()))

print("\nFeatures difference:")
print("In local not Raed:", set(local.get('features', [])) - set(raed.get('features', [])))
print("In Raed not local:", set(raed.get('features', [])) - set(local.get('features', [])))

print("\nComponents comparison:")
print("Raed component paths:", [c.get('path') for c in raed.get('components', [])])
print("Local component paths:", [c.get('path') for c in local.get('components', [])])

# Check required component keys in Raed vs Local
raed_c_keys = set().union(*(c.keys() for c in raed.get('components', [])))
local_c_keys = set().union(*(c.keys() for c in local.get('components', [])))
print("\nRaed component field keys:", raed_c_keys)
print("Local component field keys:", local_c_keys)

for idx, c in enumerate(local.get('components', [])):
    missing = {'key', 'title', 'icon', 'path', 'fields'} - set(c.keys())
    if missing:
        print(f"Component {idx} ({c.get('path')}) missing required keys: {missing}")
