import tft_analysis
import wrappertft
import playerdb
import tftcalc
import tft_analysis

def get_lobby_priorities(lobby_names):
    toRet = {}
    toRet["Items priority"]=tft_analysis.empty_items_dict()
    toRet["Champions priority"] = tft_analysis.empty_champions_dict()
    for player_name in lobby_names:
        accounts = playerdb.name_to_accounts[player_name]
        matches = []
        for account in accounts:
            matches.append(playerdb.matches_complete_by_PUUID(account))
        matches = tftcalc.analyze_matchlist(matches,accounts)
        player_analysis = tft_analysis.get_priorities(matches)
        toRet["Items priority"] = tft_analysis.add_int_dict(toRet["Items priority"],player_analysis["Items priority"])
        toRet["Champions priority"] = tft_analysis.add_int_dict(toRet["Champions priority"],player_analysis["Champions priority"])
    total1 = tft_analysis.get_total_for_int_dict(toRet["Items priority"])
    total2 = tft_analysis.get_total_for_int_dict(toRet["Champions priority"])
    toRet["Items priority"] = tft_analysis.averagyze_int_dict(toRet["Items priority"],total1)
    toRet["Champions priority"] = tft_analysis.averagyze_int_dict(toRet["Champions priority"],total2)
    return toRet

get_lobby_priorities(["Crvor"])