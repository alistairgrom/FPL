import requests
import pandas as pd
import numpy as np
import sys

from flask import Flask, render_template, request, redirect

team_id_var='3833351'
current_week = str(9)
length = 0

# players_in_squad_data = []
# players_in_squad_names = []
# players_in_squad_gw_points = []
# id_store_1 = []
# id_store_2 = []


# new_name = {}
# new_points = {}

# all_players_names = {}
# all_players_points = {}


player_data = {}
captain = {}
auto_sub_in = []
auto_sub_out = []

def get_live_points(team_id, current_week):
  all_players_data = {}
  players_in_squad_data = []
  url = "https://fantasy.premierleague.com/api/entry/"+str(team_id)+"/event/"+str(current_week)+"/picks/"
  r = requests.get(url)
  json = r.json()
  return json['entry_history']['points']


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

  for k in range(len(json['automatic_subs'])):
    id = json['automatic_subs'][k]['element_out']
    auto_sub_out.append(id)

  for l in range(len(json['automatic_subs'])):
    id = json['automatic_subs'][l]['element_in']
    auto_sub_in.append(id)

  for i in range(15):
    t = json['picks'][i]['element']
    players_ids.append(t)

  for j in range(len(json['picks'])):
    captain[str(json['picks'][j]['element'])] = json['picks'][j]['is_captain']
  return players_ids


def get_squad_data(player_ids, current_week, team_id):
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
    squad_data[str(x)] = squad_player_name[str(x)], squad_player_live_points[str(x)], captain[str(x)]
  return squad_data

def get_total_points(squad_data, ids):
  sum = 0
  for x in ids[:11]:
    if squad_data[str(x)][2] == True:
      sum += 2*(squad_data[str(x)][1])
    else:
      sum += squad_data[str(x)][1]

  #print(sum)
  # if len(auto_sub_in) != 0 and len(auto_sub_in) != 0:
  #   for j in range(len(auto_sub_out)):
  #     sum -= squad_data[str(auto_sub_out[j])][1]
  #   for i in range(len(auto_sub_in)):
  #     sum += squad_data[str(auto_sub_in[i])][1]
  
  return sum

def main():
  #load components in
  team_id = '3378116'
  current_week = '8'
  league_id = '619202'

  get_players_league_data(league_id, current_week)

  last_place_id = sorted(player_data, key=lambda item:(player_data[str(item)][0]))[0]
  print("GW"+current_week+"'s biggest loser is "+
    player_data[str(last_place_id)][1]+" with "+str(get_live_points(last_place_id, current_week)))

  print("------------------------------------------")

  ids = get_players_in_squad_ids(team_id, current_week)
  squad_data = get_squad_data(ids, current_week, team_id)

  for x in ids:
    print(squad_data[str(x)])

  print("------------------------------------------")

  print(get_total_points(squad_data, ids))
  
  print(str(auto_sub_in)+" "+str(auto_sub_out))

if __name__ == "__main__":
    sys.exit(main())


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')



# if __name__ == "__main__":
#     app.run(debug=True)