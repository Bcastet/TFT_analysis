from Infrastructure.tftwrapper import *
from Infrastructure.playerdb import *

update_database()
lobby = ["Crvor","Un33d","Torlk","Toon"]
for player in lobby:
    player_profile = tft_player(player)
    player_profile.get_stats()
