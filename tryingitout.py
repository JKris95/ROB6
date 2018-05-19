import sys
import json
import pandas as pd
import time
name = {'first_name': 'Jakob', 'surname': 'Kristiansen', 'yes': 12154.5565}
name_list =[]
for i in range(6):
    name_list.append(name)
#print(name_list)

df = pd.DataFrame(name_list)
print(df)

a = [3,4,5,6,7,8]

print (a)
print(time.asctime())