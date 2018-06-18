import sys
import json
import pandas as pd
import time
from sqlalchemy import create_engine
engine = create_engine('sqlite:///GAMEDATA.db', echo=False)

name = {'first_name': 'Dnaiel', 'surname': 'Poulsen', 'yes': 12154.5565}
name_list =[]
for i in range(6):
    name_list.append(name)

team_initials = "hihi"
team_initials[0] = 'l'
print(team_initials)
#print(name_list)5

#df = pd.DataFrame(name_list)
#print(df)

#a = [3,4,5,6,7,8]

#print (a)
#print(time.asctime())

#df.to_sql('game_data', con=engine, if_exists='append')
#df.to_sql('game_data', con=engine, if_exists='append')
#token = engine.execute("SELECT * FROM game_data").fetchall()
#databoy = pd.DataFrame(token)
#databoy.to_excel(excel_writer='blanksheet.xlsx', sheet_name='Sheet1')
#print(databoy)

#print(token)
"""
dummy = [2, 4, 6]
pos = 2
pos_cp = pos
for i in range(pos):
    print(i)
    dummy.insert(i, dummy[-pos])
    pos -= 1
    print(dummy)
    time.sleep(0.5)
del(dummy[-pos_cp:])

print(dummy)
"""
