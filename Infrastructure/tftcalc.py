from Infrastructure.wrappertft_requests import *
xp_to_level = [0,2,2,6,10,20,32,50,66]
total_xp_to_level = [0,0,2,4,10,20,40,72,122,188]

def match_analysis(participant_match):
    toRet = {}
    toRet["Xp bought"] = xp_bought(participant_match)
    toRet["Top"] = result(participant_match)
    toRet["Core"] = core(participant_match)
    toRet["Composition"] = compo(participant_match)
    toRet["Items picked"] = items_picked(participant_match)
    toRet["Traits"] = raw_traits_activated(participant_match)
    toRet["Level"] = level(participant_match)
    return toRet

def level(match):
    return match["level"]

def xp_bought(match):
    passive_xp = match["last_round"]*2
    return total_xp_to_level[match["level"]]-passive_xp

def result(match):
    return match["placement"]

def raw_traits_activated(match):
    toRet = []
    for trait in match["traits"]:
        if trait["tier_current"]>0:
            toRet.append(trait["name"].replace("Set2_",""))
    return toRet

def core(match):
    toRet = []
    raw_traits = raw_traits_activated(match)
    for unit in match["units"]:
        try:
            champion = get_champion(unit["name"])
        except:
            champion = get_champion(unit["character_id"].replace("TFT2_",""))
        
        is_core = True
        for trait in champion["traits"]:
            
            if trait not in raw_traits:
                is_core = False
        if is_core:
            toRet.append(unit["name"])
    toRet.sort()
    return toRet

def compo(match):
    toRet = []
    for unit in match["units"]:
        if unit["name"] != "":
            toRet.append(unit["name"])
        else:
            toRet.append(unit["character_id"].replace("TFT2_",""))
    return toRet

def items_picked(match):
    toRet = [0,0,0,0,0,0,0,0,0,0]
    for unit in match["units"]:
        for item_id in unit["items"]:
            if item_id<=10000:
                if item_id>=10:
                    toRet[int(item_id/10)]+=1
                    toRet[int(item_id%10)]+=1
                else:
                    toRet[item_id]+=1
    dictToRet = {}
    dictToRet["B.F. Sword"] = toRet[1]
    dictToRet["Chain Vest"] = toRet[5]
    dictToRet["Giant's Belt"] = toRet[7]
    dictToRet["Needlessly Large Rod"] = toRet[3]
    dictToRet["Negatron Cloak"]=toRet[6]
    dictToRet["Recurve Bow"]=toRet[2]
    dictToRet["Spatula"]=toRet[8]
    dictToRet["Sparring Gloves"]=toRet[9]
    dictToRet["Tear of the Goddess"]=toRet[4]
    return dictToRet

def get_participant_result(match,puuidlist):
    for puuid in puuidlist:
        for participant_match in match["info"]["participants"]:
            if participant_match["puuid"]==puuid:
                return participant_match

def analyze_matchlist(matches,puuidlist):
    toRet = []
    for match in matches:
        p_match = get_participant_result(match,puuidlist)
        toRet.append(match_analysis(p_match))
    return toRet
