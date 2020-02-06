from Infrastructure.wrappertft_requests import *

name_to_accounts = json.loads(open("Infrastructure/player_db/name_to_accounts.json","r").read())
matches_downloaded = json.loads(open("Infrastructure/player_db/matches_downloaded.json","r").read())
def register_recent_matches(player_name):
    puuid_list = name_to_accounts[player_name]
    db_f = open("Infrastructure/player_db/"+player_name+".json")
    db = json.loads(db_f.read())
    for puuid in puuid_list:
        matches = matches_by_PUUID(puuid)
        for match_id in matches:
            if match_id not in matches_downloaded[player_name] and match_id!="status":
                db.append(match_by_id(match_id))
                matches_downloaded[player_name].append(match_id)
                save = open("Infrastructure/player_db/matches_downloaded.json","w")
                save.write(json.dumps(matches_downloaded))
    db_f = open("Infrastructure/player_db/"+player_name+".json","w")
    db_f.write(json.dumps(db))

def add_player_to_db(player_name,account_names):
    if player_name in name_to_accounts.keys():
        print("Player already in db")
        return False
    
    db = open("Infrastructure/player_db/"+player_name+".json","w+")
    print(db)
    db.write("[]")
    db.close()
    matches_downloaded[player_name] = []

    name_to_accounts[player_name] = []
    for account_name in account_names:
        puuid = summoner_by_name(account_name)["puuid"]
        name_to_accounts[player_name].append(puuid)
        db = open("Infrastructure/player_db/name_to_accounts.json","w")
        db.write(json.dumps(name_to_accounts))
    
    print("Added "+player_name+" to database")
    return True

def add_account_to_player(player_name,account_name):
        puuid = summoner_by_name(account_name)["puuid"]
        if puuid in name_to_accounts[player_name]:
            return False
        name_to_accounts[player_name].append(puuid)
        db = open("players database/name_to_accounts.json","w")
        db.write(json.dumps(name_to_accounts))
        return True

def get_players_match_ids(player_name):
    db = open("players database/"+player_name+".json")
    return json.loads(db.read())

def get_player_puuid_list(player_name):
    return name_to_accounts[player_name]

def update_database():
    for player_name in name_to_accounts.keys():
        register_recent_matches(player_name)
    print("Db successfully updated!")

def get_player_games(player_name):
    assert(player_name in name_to_accounts.keys())
    db = open("Infrastructure/player_db/"+player_name+".json")
    return json.loads(db.read())