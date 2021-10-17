import requests
import pandas as pd
import numpy as np
import sys

team_id='3833351'
current_week = str(4)
length = 0

players_in_squad_data = []
players_in_squad_names = []
players_in_squad__gw_points = []
id_store_1 = []
id_store_2 = []


new_name = {}
new_points = {}

all_players_names = {}
all_players_points = {}

def get_players_in_squad():
  url = "https://fantasy.premierleague.com/api/entry/"+team_id+"/event/"+current_week+"/picks/"
  r = requests.get(url)
  json = r.json()
  json.keys()

  for i in range(14):
    t = json['picks'][i]['element']
    players_in_squad_data.append(t)
  
#also populates the names for the top5 scorers of the current GW
def get_players_in_squad_names():
  url = "https://fantasy.premierleague.com/api/bootstrap-static/"
  r = requests.get(url)
  json = r.json()
  json.keys()
  for j in range(612):
    elements_id = json['elements'][j]['id']
    elements_name = json['elements'][j]['web_name']
    elements_points = json['elements'][j]['event_points']

    #all players are in this matched with their id
    all_players_names[str(elements_id)] = elements_name

    if elements_id in players_in_squad_data:
      players_in_squad_names.append(elements_name)
      id_store_1.append(elements_id)
      new_name[str(elements_id)] = elements_name

#also populates the all_players for the top5 scorers of the GW
def get_current_week_points():
  url_live = "https://fantasy.premierleague.com/api/event/"+current_week+"/live/"
  r_live = requests.get(url_live)
  json_live = r_live.json()
  json_live.keys()
  length = len(json_live['elements'])
  for k in range(length):
    id_live = json_live['elements'][k]['id']
    points_live = json_live['elements'][k]['stats']['total_points']

    #this matches the id to the players points
    all_players_points[str(id_live)] = points_live
    if id_live in players_in_squad_data:
      players_in_squad__gw_points.append(str(json_live['elements'][k]['stats']['total_points']))
      new_points[str(id_live)] = points_live


id_store_2 = []

url_live = "https://fantasy.premierleague.com/api/event/"+current_week+"/live/"
r_live = requests.get(url_live)
json_live = r_live.json()
json_live.keys()
# for i in range(len(json_live['elements'])):
#   print(json_live['elements'][i]['stats']['total_points'])

def top_5_points():
  print("="*5+" Top 5 in GW"+current_week+" "+"="*5)
  sorted1 = sorted(all_players_points, key=lambda item: (all_players_points[str(item)]))
  for i in range(-1, -11, -1):
    if i > -10:
      print("Rank  "+str(i*-1)+": "+all_players_names[str(sorted1[i])]+", "+str(all_players_points[str(sorted1[i])]))
    else:
      print("Rank "+str(i*-1)+": "+all_players_names[str(sorted1[i])]+", "+str(all_players_points[str(sorted1[i])]))



def main():
  #load components in
  get_players_in_squad()
  get_players_in_squad_names()
  get_current_week_points()
  top_5_points()

  print("="*5+" GW"+current_week+" ("+team_id+") "+"="*5)
  for i in range(len(id_store_1)):
    print(new_name[str(id_store_1[i])]+", "+str(new_points[str(id_store_1[i])]))

if __name__ == "__main__":
    sys.exit(main())

