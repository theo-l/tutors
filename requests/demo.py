# coding: utf-8
"""
base demo for requests
"""

import requests

r = requests.get('https://api.github.com/user', auth=('theo-l', 'hongboc@06'))
print(r.status_code)
print(r.headers)
print(r.encoding)
print(r.text)
print(r.json())
