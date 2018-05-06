import sys
import json

name = {'first_name': 'Jakob', 'surname': 'Kristiansen'}
dumped_name = json.dumps(name)
decoded_name = dumped_name.encode()
print(decoded_name, type(decoded_name))
what_happens = json.loads(decoded_name)
print(what_happens, type(what_happens))