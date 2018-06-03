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
#print(name_list)5

#df = pd.DataFrame(name_list)
#print(df)

#a = [3,4,5,6,7,8]

#print (a)
#print(time.asctime())

#df.to_sql('game_data', con=engine, if_exists='append')
#df.to_sql('game_data', con=engine, if_exists='append')
token = engine.execute("SELECT * FROM game_data").fetchall()
databoy = pd.DataFrame(token)
#databoy.to_excel(excel_writer='blanksheet.xlsx', sheet_name='Sheet1')
print(databoy)