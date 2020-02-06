import requests
import json
from PIL import Image
api_key = "RGAPI-85dd2459-ab73-49c5-a6eb-26d22956d4de"

champions = json.loads(open("Infrastructure/static_data/champions.json","r").read())
hexes = json.loads(open("Infrastructure/static_data/hexes.json","r").read())
items = json.loads(open("Infrastructure/static_data/items.json","r").read())
#traits = json.loads(open("Infrastructure/static_data/traits.json","r").read())
root_items_list = [
            "B.F. Sword",
            "Chain Vest",
            "Giant's Belt",
            "Needlessly Large Rod",
            "Negatron Cloak",
            "Recurve Bow",
            "Spatula",
            "Sparring Gloves",
            "Tear of the Goddess"
        ]
        
def match_by_id(id):
    query = "https://europe.api.riotgames.com/tft/match/v1/matches/"+str(id)+"?api_key="+api_key
    return get_json_query(query)

def matches_by_PUUID(puuid):
    query = "https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/"+str(puuid)+"/ids"+"?api_key="+api_key
    return get_json_query(query)

def summoner_by_name(name):
    query = "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/"+str(name)+"?api_key="+api_key
    toRet= get_json_query(query)
    try:
        toRet["puuid"]
        return toRet
    except:
        print(toRet)
        print("Exception when getting "+name)
        raise NameError

def summoner_by_PUUID(puuid):
    query = "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/"+str(puuid)+"?api_key="+api_key
    toRet= get_json_query(query)
    try:
        toRet["puuid"]
        return toRet
    except:
        print(toRet)
        print("Exception when getting "+name)
        raise NameError

def stop_if_404(json_request):
    if(type(json_request)==dict and "status" in json_request.keys()):
        print("\n\n Request failed \n\n")
        print(json_request)
        raise NameError

def get_json_query(query):
    print(query)
    r = requests.get(query)
    toRet = json.loads(r.content)
    stop_if_404(toRet)
    return toRet

def matchlist_by_name(name):
    summoner = summoner_by_name(name)
    puuid = summoner["puuid"]
    return matches_by_PUUID(puuid)

def matches_from_list(liststr):
    toRet = []
    for match_id in liststr:
        toRet.append(match_by_id(match_id))
    return toRet

def matches_by_name(name):
    l = matchlist_by_name(name)
    return matches_from_list(l)

def matches_complete_by_PUUID(puuid):
    l = matches_by_PUUID(puuid)
    return matches_from_list(l)

def get_champion(champion_name):
    for champion in champions:
        if champion["champion"].lower()==champion_name.lower():
            return champion
    #print("Can't find "+champion_name)
    raise NameError


    

