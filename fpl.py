import requests
import pandas as pd
import numpy as np


team_id='7072838'
current_week = str(7)

url = "https://fantasy.premierleague.com/api/entry/"+team_id+"/event/"+current_week+"/picks/"
r = requests.get(url)
json = r.json()
json.keys()

players_in_squad_data = []
for i in range(14):
  t = json['picks'][i]['element']
  players_in_squad_data.append(t)
# t = list(t)[0]
# print(t)

print(players_in_squad_data)

print()

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
r = requests.get(url)
json = r.json()
json.keys()
# t = json['picks']
# t = list(t)[0]
# print(t)
for j in range(612):
  elements_id = json['elements'][j]['id']
  elements_name = json['elements'][j]['web_name']
  if elements_id in players_in_squad_data:
    print(elements_name)


# current_week = 0
# while current_week < 50:
#   current_week += 1
#   url = "https://fantasy.premierleague.com/api/entry/"+team_id+"/event/"+str(current_week)+"/picks/"
#   #url = 'fantasy.premierleague.com/api/entry/'+team_id+'/picks/'+str(current_week)+'/'
#   r = requests.get(url)
#   if r.status_code != 200:
#     break
#   json = r.json()
#   json.keys()
#   #print(json.keys())
#   print(current_week, json['entry_history']['points'])