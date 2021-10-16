import requests
import pandas as pd
import numpy as np


team_id='3833351'
current_week = str(1)

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

players_in_squad_names = []
players_in_squad__gw_points = []
id_store_1 = []
id_store_2 = []

new_name = {}
new_points = {}

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
r = requests.get(url)
json = r.json()
json.keys()
for j in range(612):
  elements_id = json['elements'][j]['id']
  elements_name = json['elements'][j]['web_name']
  elements_points = json['elements'][j]['event_points']
  if elements_id in players_in_squad_data:
    players_in_squad_names.append(elements_name)
    id_store_1.append(elements_id)
    new_name[str(elements_id)] = elements_name
    #print(elements_name+", "+str(elements_points))


url_live = "https://fantasy.premierleague.com/api/event/"+current_week+"/live/"
r_live = requests.get(url_live)
json_live = r_live.json()
json_live.keys()
for k in range(550):
  id_live = json_live['elements'][k]['id']
  points_live = json_live['elements'][k]['stats']['total_points']
  if id_live in players_in_squad_data:
    players_in_squad__gw_points.append(str(json_live['elements'][k]['stats']['total_points']))
    new_points[str(id_live)] = points_live



print(new_name)
print(new_points)

print(new_name['69'])