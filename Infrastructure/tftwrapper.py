import requests
import json
import arrow 
from Infrastructure.wrappertft_requests import *
from Infrastructure.playerdb import *
from Infrastructure.tftcalc import *
from Infrastructure.tft_analysis import *
import pandas as pd
import arrow

patch_timestamp = 1580889600
class tft_match():
    def __init__(self,id):
        try:
            f = open("/Infrastructure/matches_db/"+id).read()
            self.data = json.loads(f)
        except:
            query = "https://europe.api.riotgames.com/tft/match/v1/matches/"+str(id)+"?api_key="+api_key
            self.data = get_json_query(query)
        self.date = arrow.get(self.data["info"]["game_datetime"])
        self.participants = participants(self.data["info"]["game_datetime"]["participants"])
        self.game_length = self.data["info"]["game_datetime"]["game_length"]
        self.queue = self.data["info"]["game_datetime"]["game_version"]

class participants(list):
    def __init__(self,l):
        self = []
        for p in l:
            self.append(participant(p))

class participant():
    def __init__(self,pdict):
        self.place = pdict["placement"]
        self.level = pdict["level"]
        self.last_round = pdict["last_round"]
        self.traits = traits(pdict["traits"])
        self.total_damage_to_players = pdict["total_damage_to_players"]
        self.units = units(pdict["units"])
        self.gold_left = pdict["gold_left"]

class traits(list):
    def __init__(self, ltraits):
        self = [trait(x) for x in ltraits]

class trait():
    def __init__(self, tdict):
        self.tier_total = tdict["tier_total"]
        self.name = tdict["name"]
        self.tier_current = tdict["tier_current"]
        self.num_units = tdict["num_units"]


class units(list):
    def __init__(self, units):
        self = [unit(x) for x in units]

class unit():
    def __init__(self,udict):
        self.tier = udict["tier"]
        self.items = udict["items"]
        self.character_id = udict["character_id"]
        self.name = udict["name"]
        self.rarity = udict["rarity"]

class player_history():
    def __init__(self,name,accounts=None,on_patch=False):
        if name in name_to_accounts.keys():
            self.history = get_player_games(name)
            self.accounts = name_to_accounts[name]
        else:
            self.accounts = accounts
            super().__init__([])
        self.name = name
        self.games_on_patch = []
        if on_patch:
            self.games_on_patch = []
            for game in get_player_games(name):
                if game["info"]["game_datetime"]>patch_timestamp*1000:
                    print("Adding game on ",arrow.Arrow.fromtimestamp(game["info"]["game_datetime"]/1000).datetime)
                    self.games_on_patch.append(game)
            
        for game in self.games_on_patch:
            print(arrow.Arrow.fromtimestamp(game["info"]["game_datetime"]/1000).datetime)
        #assert(len(list(self.games_on_patch)) != len(self.history))


class tft_summoner():
    def __init__(self,account = None,puuid = None):
        if account!=None:
            self.data = summoner_by_name(account)
        if puuid!=None:
            self.data = summoner_by_PUUID(account)
        self.name = self.data["name"]
        self.puuid = self.data["puuid"]

class tft_player():
    def __init__(self,name):
        self.name = name
        if name in name_to_accounts.keys():
            self.accounts = name_to_accounts[name]
        else:
            print("Player not in db - please add him to db first")
            raise BrokenPipeError
        self.match_history = player_history(name,on_patch=True).games_on_patch
        for game in self.match_history:
            print(arrow.Arrow.fromtimestamp(game["info"]["game_datetime"]/1000).datetime)
        print("Found ",len(self.match_history)," games in current patch for",self.name)
        
        self.matches_reduced = analyze_matchlist(self.match_history,self.accounts)
    
    def get_stats(self):
        unit_graph = {"Units": list(empty_champions_dict().keys()),"Nb games" : [0] * len(list(empty_champions_dict().keys())),"Wins" : [0]* len(list(empty_champions_dict().keys())),"Top 1" : [0]* len(list(empty_champions_dict().keys()))}
        tops_graphs = {"Nb top" : [0,0,0,0,0,0,0,0] , "Tops" : [1,2,3,4,5,6,7,8]}
        items_graphs = {"Items":list(empty_items_dict().keys()),"Times picked" : [0] * len(list(empty_items_dict().keys()))}
        for game in self.matches_reduced:
            for item_picked in game["Items picked"]:
                index = items_graphs["Items"].index(item_picked)
                items_graphs["Times picked"][index]+=game["Items picked"][item_picked]
            for unit in game["Composition"]:
                index = unit_graph["Units"].index(unit.lower().capitalize())
                unit_graph["Nb games"][index]+=1
                if game["Top"] <= 4:
                    unit_graph["Wins"][index]+=1
                if game["Top"] ==1:
                    unit_graph["Top 1"][index]+=1
            index = tops_graphs["Tops"].index(game["Top"])
            tops_graphs["Nb top"][index] +=1

        pl = pd.DataFrame(unit_graph)
        pl = pl.plot(kind='bar',x='Units',y=['Nb games','Wins','Top 1'],fontsize = 6)
        fig = pl.get_figure()
        filename_champions = "Infrastructure/plots/"+self.name+ "-units.png"
        fig.savefig(filename_champions)

        pl = pd.DataFrame(tops_graphs)
        pl = pl.plot(kind='bar',x='Tops',y=['Nb top'],fontsize = 6)
        fig = pl.get_figure()
        filename_champions = "Infrastructure/plots/"+self.name+ "-tops.png"
        fig.savefig(filename_champions)

        pl = pd.DataFrame(items_graphs)
        pl = pl.plot(kind='bar',x="Items",y=["Times picked"],fontsize = 6)
        fig = pl.get_figure()
        filename_champions = "Infrastructure/plots/"+self.name+ "-items.png"
        fig.savefig(filename_champions)







