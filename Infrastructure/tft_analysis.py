from Infrastructure.wrappertft_requests import *

def get_cores(matches_analysed):
    toRet = []
    for match in matches_analysed:
        index = is_core_in_list(toRet,match["Core"])
        if index==-1:
            toRet.append(coredict(match["Core"]))
        else:
            toRet[index]["Total games"]+=1
    return toRet

def coredict(core):
    toRet = {}
    toRet["Champions"] = core
    toRet["Traits"]=getTraitsFromCore(core)
    toRet["Total games"] = 1
    return toRet

def getTraitsFromCore(core):
    toRet = []
    for champion in core:
        traits = get_champion(champion)["traits"]
        for trait in traits:
            if trait not in toRet:
                toRet.append(trait)

    return toRet

def is_core_in_list(list_core_dict,core):
    index = 0
    for core_dict in list_core_dict:
        if core_dict["Champions"]==core:
            return index
        index+=1
    return -1

def places_for_core(core, matches_analysed):
    toRet = {el:0 for el in range(1,9)}
    
    for match in matches_analysed:
        if match["Core"]==core:
            position = match["Top"]
            toRet[position]+=1
    return toRet

def xp_bought_for_core(core, matches_analysed):
    toRet = 0
    for match in matches_analysed:
        if match["Core"]==core:
            toRet+=match["Xp bought"]
    return toRet/len(matches_analysed)

def empty_items_dict():
    dictToRet = {}
    dictToRet["B.F. Sword"] = 0
    dictToRet["Chain Vest"] = 0
    dictToRet["Giant's Belt"] = 0
    dictToRet["Needlessly Large Rod"] = 0
    dictToRet["Negatron Cloak"]=0
    dictToRet["Recurve Bow"]=0
    dictToRet["Spatula"]=0
    dictToRet["Sparring Gloves"]=0
    dictToRet["Tear of the Goddess"]=0
    return dictToRet

def items_for_core(core,matches_analysed):
    toRet = empty_items_dict()
    for match in matches_analysed:
        if match["Core"]==core:
            for item in match["Items picked"].keys():
                toRet[item]+=match["Items picked"][item]
    return toRet

def level_for_core(core,matches_analysed):
    toRet = [0,0,0,0,0,0,0,0,0,0,0]
    for match in matches_analysed:
        if match["Core"]==core:
            toRet[match["Level"]]+=1
    return toRet
    #This is useless, but done to calculate the average
    total_lvl = 0
    total_games = 0
    for index in range(1,10):
        total_games += toRet[index]
        total_lvl += toRet[index]*index
    return total_lvl/total_games

def analyse_core(core, matches_analysed):
    toRet = {}
    toRet["Items"] = items_for_core(core, matches_analysed)
    toRet["Avg level"] = level_for_core(core,matches_analysed)
    toRet["Avg xp"] = xp_bought_for_core(core, matches_analysed)
    toRet["Tops"] = places_for_core(core,matches_analysed)
    return toRet

def extract_cores_analysis_from_matches(matches):
    cores = get_cores(matches)
    for core_dict in cores:
        core_dict["Stats"] = analyse_core(core_dict["Champions"],matches)
    return cores

def extract_mattering_cores_only(matches, nb_games_minimum):
    analysis = extract_cores_analysis_from_matches(matches)
    toRet = []
    for core_analysis in analysis:
        if core_analysis["Total games"]>nb_games_minimum:
            toRet.append(core_analysis)
    return toRet


def get_subcores(matches):
    cores = get_cores(matches)
    toRet = []
    for core in cores:
        for core_b in cores:
            if core!=core_b:
                subcore = list(set(core["Champions"]).intersection(core_b["Champions"]))
                if subcore!=[]:
                    index = is_core_in_list(toRet,subcore)
                    if index == -1: 
                            subcoredict = coredict(subcore)
                            subcoredict["Total games"] = core["Total games"] + core_b["Total games"]
                            subcoredict["Cores using this"] = [core,core_b]
                            toRet.append(subcoredict)
                    else:
                        if core not in toRet[index]["Cores using this"]:
                            toRet[index]["Total games"] += core["Total games"]
                            toRet[index]["Cores using this"].append(core)
                        if core_b not in toRet[index]["Cores using this"]:
                            toRet[index]["Total games"] += core_b["Total games"]
                            toRet[index]["Cores using this"].append(core_b)
    return toRet

def extract_subcorescores_analysis_from_matches(matches):
    cores = get_subcores(matches)
    for core_dict in cores:
        core_dict["Stats"] = analyse_core(core_dict["Champions"],matches)
    return cores

def extract_mattering_subcores_only(matches, nb_games_minimum):
    analysis = extract_subcorescores_analysis_from_matches(matches)
    toRet = []
    for core_analysis in analysis:
        if core_analysis["Total games"]>nb_games_minimum:
            toRet.append(core_analysis)
    return toRet

def empty_champions_dict():
    toRet = {}
    for champion in champions:
        toRet[champion["champion"].lower().capitalize()] = 0
    return toRet

def get_priorities(matches):
    toRet = {}
    toRet["Champions priorities"] = empty_champions_dict()
    toRet["Items priorities"] = empty_items_dict()
    for match in matches():
        for champion in match["Composition"]:
            toRet["Champions priorities"][champion]+=1
        for champion in match["Items picked"]:
            toRet["Items priorities"][champion]+=1
    
    total_items = get_total_for_int_dict(toRet["Items priorities"])
    total_champions = get_total_for_int_dict(toRet["Champions priorities"])
    toRet["Champions priorities"] = averagyze_int_dict(toRet["Champions priorities"],total_champions)
    toRet["Items priorities"] = averagyze_int_dict(toRet["Items priorities"],total_items)
    return toRet

def get_total_for_int_dict(int_dict):
    toRet = 0
    for key in int_dict.keys():
        toRet+=int_dict[key]
    return toRet

def averagyze_int_dict(int_dict,total):
    toRet = int_dict
    for key in int_dict.keys():
        toRet[key] = int_dict[key]/total
    return toRet

def add_int_dict(int_dict_1,int_dict_2):
    for key in int_dict_1.keys():
        int_dict_1[key]+=int_dict_2[key]
    return int_dict_1