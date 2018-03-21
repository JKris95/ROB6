import json

coneInformation = [{"Role": 'False', "Content": 'questionmark'}]

enConeInformation = json.dumps(coneInformation[0])
print(range(1))
print(type(coneInformation[0]))
print(type(coneInformation))
print(type(enConeInformation))
print (enConeInformation)
