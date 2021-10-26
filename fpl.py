import requests
import pandas as pd
import numpy as np
import sys

team_id_var='3833351'
current_week = str(9)
length = 0

players_in_squad_data = []
players_in_squad_names = []
players_in_squad_gw_points = []
id_store_1 = []
id_store_2 = []


new_name = {}
new_points = {}

all_players_names = {}
all_players_points = {}


player_data = {}

def get_live_points(team_id, current_week):
  all_players_data = {}
  players_in_squad_data = []
  url = "https://fantasy.premierleague.com/api/entry/"+str(team_id)+"/event/"+str(current_week)+"/picks/"
  r = requests.get(url)
  json = r.json()
  json.keys()
  return json['entry_history']['points']

# def team_ids_from_league(league_id):
#   url = 'https://fantasy.premierleague.com/api/leagues-classic/'+str(league_id)+'/standings/?page_new_entries=1&page_standings=1&phase=1'
#   r = requests.get(url)
#   json = r.json()
#   players_in_league = []
#   for i in range(30):
#     try:
#       players_in_league.append(json['standings']['results'][i]['entry'])
#     except:
#       pass
#   return players_in_league

def get_players_league_data(league_id, current_week):
  url = 'https://fantasy.premierleague.com/api/leagues-classic/'+str(league_id)+'/standings/?page_new_entries=1&page_standings=1&phase=1'
  r = requests.get(url)
  json = r.json()
  players_in_league = []
  for i in range(30):
    try:
      players_in_league.append(json['standings']['results'][i]['entry'])
      player_data[str(json['standings']['results'][i]['entry'])] = get_live_points(str(json['standings']['results'][i]['entry']), current_week), str(json['standings']['results'][i]['player_name']), json['standings']['results'][i]['total'] 
    except:
      pass

  print('{:22s} {:2s}{:4s} {:12s}'.format("Name", "GW", current_week, "Total Points"))
  print("------------------------------------------")
  for x in players_in_league:
    try:
      print('{:17s} {:8d} {:10d}'.format(player_data[str(x)][1], player_data[str(x)][0], player_data[str(x)][2]))
    except:
      print(x," joined the league after this GW.")
  print("------------------------------------------")


def get_players_in_squad_ids(team_id, current_week):
  players_ids = []
  url = "https://fantasy.premierleague.com/api/entry/"+team_id+"/event/"+current_week+"/picks/"
  r = requests.get(url)
  json = r.json()
  json.keys()

  for i in range(15):
    t = json['picks'][i]['element']
    players_ids.append(t)

  return players_ids

def get_squad_data(player_ids, current_week):
  squad_player_name = {}
  squad_player_live_points = {}
  squad_data = {}

  url = "https://fantasy.premierleague.com/api/bootstrap-static/"
  r = requests.get(url)
  json = r.json()
  json.keys()
  num_players = len(json['elements'])
  for j in range(num_players):
    elements_id = json['elements'][j]['id']
    elements_name = json['elements'][j]['web_name']

    if elements_id in player_ids:
      squad_player_name[str(elements_id)] = elements_name
  

  live_url = "https://fantasy.premierleague.com/api/event/"+str(current_week)+"/live/"
  live_r = requests.get(live_url)
  live_json = live_r.json()
  num_players = len(live_json['elements'])
  for k in range(num_players):
    live_elements_id = live_json['elements'][k]['id']
    live_elements_points = live_json['elements'][k]['stats']['total_points']

    if live_elements_id in player_ids:
      squad_player_live_points[str(live_elements_id)] = live_elements_points

  for x in player_ids:
    squad_data[str(x)] = squad_player_name[str(x)], squad_player_live_points[str(x)]  
  return squad_data


def main():
  #load components in
  team_id = '3833351'
  current_week = '9'
  league_id = '619202'

  get_players_league_data(league_id, current_week)

  last_place_id = sorted(player_data, key=lambda item:(player_data[str(item)][0]))[0]
  print(player_data[str(last_place_id)][1]+" "+str(get_live_points(last_place_id, current_week)))


  print(get_squad_data(get_players_in_squad_ids(team_id, current_week), current_week))

if __name__ == "__main__":
    sys.exit(main())

