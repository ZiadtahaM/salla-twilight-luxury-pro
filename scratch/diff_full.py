import urllib.request, json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

raed_url = 'https://raw.githubusercontent.com/SallaApp/theme-raed/master/twilight.json'
raed = json.loads(urllib.request.urlopen(raed_url).read().decode('utf-8'))

gh_url = 'https://raw.githubusercontent.com/ZiadtahaM/salla-twilight-luxury-pro/master/twilight.json'
gh = json.loads(urllib.request.urlopen(gh_url).read().decode('utf-8'))

print("=== SETTINGS CHECK ===")
print("Raed settings len:", len(raed['settings']))
print("GH settings len:", len(gh['settings']))

for i in range(min(len(raed['settings']), len(gh['settings']))):
    rs = raed['settings'][i]
    gs = gh['settings'][i]
    if rs != gs:
        print(f"Setting {i} ({rs.get('id')}) differs!")
        print("  Raed keys:", list(rs.keys()))
        print("  GH keys:", list(gs.keys()))
        for k in rs:
            if rs[k] != gs.get(k):
                print(f"    Diff in '{k}': Raed={rs[k]!r} vs GH={gs.get(k)!r}")

print("\n=== COMPONENTS CHECK ===")
print("Raed components len:", len(raed['components']))
print("GH components len:", len(gh['components']))

# Check the Raed components that are inside GH
for idx, rc in enumerate(raed['components']):
    match = next((c for c in gh['components'] if c.get('path') == rc.get('path')), None)
    if not match:
        print(f"Raed component {rc.get('path')} NOT in GH!")
    else:
        # compare keys
        if set(rc.keys()) != set(match.keys()):
            print(f"Component {rc.get('path')} keys differ: Raed={set(rc.keys())} vs GH={set(match.keys())}")

# Now check the custom component in GH
custom = next((c for c in gh['components'] if c.get('path') == 'home.luxury-hero-banner'), None)
if custom:
    print("\nCustom component 'home.luxury-hero-banner':")
    print("Keys:", list(custom.keys()))
    print("Missing from Raed standard keys:", set(raed['components'][0].keys()) - set(custom.keys()))
