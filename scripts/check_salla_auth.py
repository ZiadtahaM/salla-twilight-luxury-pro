import requests
import json
import os

# Salla CLI stores access token in ~/.salla or %USERPROFILE%/.salla or registry
user_profile = os.environ.get('USERPROFILE', '')
token_path = os.path.join(user_profile, '.salla')

print('Checking .salla path:', token_path, 'Exists:', os.path.exists(token_path))
if os.path.exists(token_path):
    with open(token_path, 'r', encoding='utf-8') as f:
        print('Token file:', f.read()[:200])

# Let's also check D:\nodejs\node_global\node_modules\@salla.sa\cli configuration
