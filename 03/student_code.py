from expand import expand
def a_star_search(dis_map, time_map, start, end):

    path = []
    tree = {}
    access = {}
    expanded = {}
    detect = {}
    following = [start,0,dis_map[start][end]]
    found = False
    priority_dict = []
    agla_no = []
    while(found ==False):
        ij = following[0]
        #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PEHLA ij is --> {}".format(ij))
        agla_no.append(ij)
        access[following[0]] = following[1]
        #print("visited is --->{}".format(access))
        #print("detect is ----->{}".format(detect))
        #print("score is ---->{}".format(tree))
        #print("visited is ---->{}".format(access))
        #print("expanded is -----> {}".format(expanded))
        if ij in detect:
            #print("LOL checking if ij in detect, if present popping. Current detect ---> {}".format(detect))
            detect.pop(ij,None)
            #print("LOL checking if ij in detect, if present popping. After Pop detect ---> {}".format(detect))

        #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&The current path is -----> {}".format(path))
        temp_dict = {}
        #print("temp_dict before checking into time_map --> {}".format(temp_dict))
        for p in time_map[ij]:

            if (time_map[ij][p]!= None):
                temp_dict[p] = following[1]+time_map[ij][p]+dis_map[p][end]
                #print("current value of p is ------>{}".format(p))
                #print("current value of ij is ------>{}".format(ij))
                #print("AFTER UPDATE temp_dict ---> {}".format(temp_dict))
        tree[ij] = temp_dict
        #print("updated score dictionary is ---> {}".format(tree))
        #print("updated temp_dict dictionary is  ----> {}".format(temp_dict))
        #print("!! updated detect dictionary is ---> {}".format(detect))
        #print("!! updated visited dictionary is --->{}".format(access))
        #print("Current temp_dict is -> {}".format(temp_dict))
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ LOOP STARTING @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        for p in temp_dict:

            if p in detect:
                #print("# James Bond")
                #print("@@@@@ current p is  -> {}".format(p))
                if (access[ij]+time_map[ij][p]+dis_map[p][end] < detect[p]):
                    detect[p] = access[ij]+time_map[ij][p]+dis_map[p][end]
                    expanded[p] = access[ij]+time_map[ij][p]
                    #print("james bond loop updates the detect to --> {}".format(detect))
                ik = min(detect, key = detect.get)
                following = [ik, detect[ik]-dis_map[ik][end], dis_map[ik][end]]
                #print("minimum of ik in james bond loop is -->{}".format(ik))
                #print("next best in james bond loop is -->{}".format(following))


            if ((p not in access) and (p not in detect)):
                #print("$$$$$$$$$$$$$ LOOP mein ghusa hain -----> {}".format(p))
                if not detect:
                    detect[p] = access[ij]+time_map[ij][p]+dis_map[p][end]
                    #print("INLOOP detect is updated to ---> {}".format(detect[p]))
                    expanded[p] = access[ij]+time_map[ij][p]
                    #print("INLOOP expanded is updated to ---> {}".format(expanded[p]))
                #print("AFTER INLOOP detect is --> {}".format(detect))
                ik = min(detect, key = detect.get)
                #print("INLOOP ik updated to  --> {}".format(ik))
                i_j = access[ij]+time_map[ij][p]+dis_map[p][end]
                #print("** After choosing minimum i_j is now ---> {}".format(i_j))

                if(i_j > detect[ik]):
                    #print("# PAUL WALKER")
                    following = [ik, expanded[ik], dis_map[ik][end]]
                    #print("next best via paul walker is --> {}".format(following))
                    detect[p] = i_j
                    expanded[p] = access[ij]+time_map[ij][p]
                    #print("the expanded list in PAUL WALKER is ----> {}".format(expanded))
                    #print("its length is ----> {}".format(len(expanded)))

                if (i_j < detect[ik]):
                    #print("# VIN DIESEL")
                    following = [p, access[ij]+time_map[ij][p], dis_map[p][end]]
                    #print("next best via vin diesel is --> {}".format(following))
                    detect[p] = i_j
                    expanded[p] = access[ij]+time_map[ij][p]

                if (i_j == detect[ik]):
                    #print("WALHALLA")
                    #print("The visited node for the condition is -->{}".format(access[ij]))
                    #print("The time from visited node to p is --->{}".format(time_map[ij][p]))
                    #print("The detect value is --->{}".format(detect[ik]))
                    #print("The dismap value is --->{}".format(dis_map[ik][end]))
                    if (access[ij]+time_map[ij][p] < detect[ik] - dis_map[ik][end]):
                        following = [p, access[ij]+time_map[ij][p], dis_map[p][end]]
                        #print("NEXT BEST is updated to from <if> --> {}".format(following))
                    else:
                        following = [ik, expanded[ik], dis_map[ik][end]]
                        #print("NEXT BEST is updated to from <else>--> {}".format(following))

            if (p == end):
                #print("#teja","p is ---> {}".format(p))
                #print("^^^FINAL visited is --->{}".format(access))
                #print("^^^FINAL detect is ----->{}".format(detect))
                #print("^^^FINAL score is ---->{}".format(tree))
                #print("^^^FINAL expanded is -----> {}".format(expanded))
                found = True
                break




    path = get_path(tree,start,end)
    #print("@ path is @ --> {}".format(path))
    #print("@ length of expanded is ---> {}".format(len(expanded)))
    #print("@ length of visited is ---> {}".format(len(access)))
    #print("@ length of scores is ----> {}".format(len(tree)))
    #print("@length of detect is -----> {}".format(len(detect)))
    #print("@length of agla_no is ---> {}".format(len(agla_no)))

    for k,v in expanded.items():
        a0 = v
        a11 = k
    for k,v in detect.items():
        b0 = v
        b11 = k

    if a0 == b0:
        for e in expanded:
            expand(e,dis_map)

    else:
        expanded.pop(a11)
        for e in expanded:
            expand(e,dis_map)

    return path



def get_path(tree,start,end):
    ppath = []
    q = len(tree)
    for k,v in tree.items():
        if end in v:
            #print(k)
            curr_key = k
            ppath.append(end)
            ppath.append(curr_key)
    helper_path(tree,ppath,curr_key,start)
    ppath.reverse()
    return(ppath)


def helper_path(tree,ppath,curr_key,start):
    a_list = []
    for k,v in tree.items():
        if curr_key in v:
            for k1,v1 in v.items():
                if k1 == curr_key:
                    a_list.append(v1)
    a1 = min(a_list)
    for k,v in tree.items():
        for k2,v2 in v.items():
            if v2 == a1:
                ppath.append(k)
                new_key = k

    if new_key == start :
        return
    else:
        helper_path(tree,ppath,new_key,start)
