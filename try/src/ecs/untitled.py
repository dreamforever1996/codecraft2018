def dp_distribute(predict_flavors=None, ps_cpu_num=None, ps_mem_num=None, target=None, flavor_names=None, flavors=None):
    pServers = []
    pServers_Res = []

    current_pServer = {}
    current_pServer_Res = (ps_cpu_num, ps_mem_num)
    print "TARGET is %s"%target

    # remove flavors predicted whose number is 0
    fk = [] #flavors to be removed
    for f in predict_flavors:
        if f[1] == 0:
            fk.append(f)
    for f in fk:
        predict_flavors.remove(f)
        flavor_names.remove(f[0])
    
    fn_dict={}
    goods = []
    total_cpu = 0
    total_mem = 0
    for f in predict_flavors:
        for ff in flavors:
            if f[0] == ff[0]:
                fn_dict[f[0]]=(f[1],ff[1],ff[2])
                total_mem+=f[1]*ff[2]
                total_cpu+=f[1]*ff[1]
                for i in range(f[1]):
                    goods.append((f[0],ff[1],ff[2]))
                break
    num_goods = len(goods)
    newgoods = []
    while(len(newgoods)!=num_goods):
        max_cpu = 0
        best_good = None
        for good in goods:
            if good[1]>max_cpu:
                max_cpu = good[1]
                best_good = good
        newgoods.append(best_good)
        goods.remove(best_good)
    for good in newgoods:
        print good
    goods = newgoods

    while(goods):
        bag = [ [ [(0,0) for o in range(ps_mem_num)] for j in range(ps_cpu_num)] for i in range(num_goods)]
        bag_f = [ [ [[] for o in range(ps_mem_num)] for j in range(ps_cpu_num)] for i in range(num_goods)]
        for i in range(len(goods)):
            #print "%d/%d iteration"%(i, len(goods))
            for c in range(ps_cpu_num):
                for m in range(ps_mem_num):
                    if i==0:
                        if goods[i][1]<c+1 and goods[i][2]<m+1:
                            #if target=="MEM":
                            #    bag[i][c][m] = goods[i][2]
                            #elif target == "CPU":
                            #    bag[i][c][m] = goods[i][1]
                            bag[i][c][m] = (goods[i][1],goods[i][2])
                            bag_f[i][c][m].append(goods[i][0])
                    else:
                        if goods[i][1]<c+1 and goods[i][2]<m+1:
                            t = 0
                            #if target=="MEM":
                            #    t = goods[i][2]
                            #elif target == "CPU":
                            #    t = goods[i][1]
                            t = (goods[i][1],goods[i][2])
                            if bag[i-1][c-goods[i][1]][m-goods[i][2]][0] + t[0] > bag[i-1][c][m][0]:
                                bag[i][c][m] = (bag[i-1][c-goods[i][1]][m-goods[i][2]][0] + t[0], bag[i-1][c-goods[i][1]][m-goods[i][2]][1] + t[1])
                                index = 1
                            elif bag[i-1][c-goods[i][1]][m-goods[i][2]][0] + t[0] < bag[i-1][c][m][0]:
                                bag[i][c][m] = (bag[i-1][c][m][0],bag[i-1][c][m][1])
                                index = 2
                            elif bag[i-1][c-goods[i][1]][m-goods[i][2]][0] + t[0] == bag[i-1][c][m][0]:
                                if bag[i-1][c-goods[i][1]][m-goods[i][2]][1] + t[1] < bag[i-1][c][m][1]:
                                    bag[i][c][m] = (bag[i-1][c][m][0],bag[i-1][c][m][1])
                                    index = 2
                                elif bag[i-1][c-goods[i][1]][m-goods[i][2]][1] + t[1] >= bag[i-1][c][m][1]:
                                    bag[i][c][m] = (bag[i-1][c-goods[i][1]][m-goods[i][2]][0] + t[0], bag[i-1][c-goods[i][1]][m-goods[i][2]][1] + t[1])
                                    index = 1
                            bag[i][c][m], index = max(bag[i-1][c][m], bag[i-1][c-goods[i][1]][m-goods[i][2]]+t)
                            if index == 1:
                                bag_f[i][c][m] = bag_f[i-1][c][m][:]
                            elif index == 2:
                                bag_f[i][c][m] = bag_f[i-1][c-goods[i][1]][m-goods[i][2]][:]
                                bag_f[i][c][m].append(goods[i][0])
                        else:
                            bag[i][c][m] = bag[i-1][c][m]
                            bag_f[i][c][m] = bag_f[i-1][c][m][:]
        current_pServer = {}
        print "============"
        for g in bag_f[len(goods)-1][ps_cpu_num-1][ps_mem_num-1]:
            gc = fn_dict[g][1]
            gm = fn_dict[g][2]
            #print "remove (%s, %d, %d)"%(g, gc, gm)
            goods.remove((g,gc,gm))
            try:
                current_pServer[g]+=1
            except KeyError:
                current_pServer[g] = 1
        pServers.append(current_pServer)

    return pServers, pServers_Res



def dp_distribute(predict_flavors=None, ps_cpu_num=None, ps_mem_num=None, target=None, flavor_names=None, flavors=None):
    pServers = []
    pServers_Res = []

    current_pServer = {}
    current_pServer_Res = (ps_cpu_num, ps_mem_num)
    print "TARGET is %s"%target

    # remove flavors predicted whose number is 0
    fk = [] #flavors to be removed
    for f in predict_flavors:
        if f[1] == 0:
            fk.append(f)
    for f in fk:
        predict_flavors.remove(f)
        flavor_names.remove(f[0])
    
    fn_dict={}
    goods = []
    total_cpu = 0
    total_mem = 0
    for f in predict_flavors:
        for ff in flavors:
            if f[0] == ff[0]:
                fn_dict[f[0]]=(f[1],ff[1],ff[2])
                total_mem+=f[1]*ff[2]
                total_cpu+=f[1]*ff[1]
                for i in range(f[1]):
                    goods.append((f[0],ff[1],ff[2]))
                break
    num_goods = len(goods)

    while(goods):
        bag = [ [ [0 for o in range(ps_mem_num+1)] for j in range(ps_cpu_num+1)] for i in range(num_goods)]
        bag_f = [ [ [[] for o in range(ps_mem_num+1)] for j in range(ps_cpu_num+1)] for i in range(num_goods)]
        for i in range(len(goods)):
            #print "%d/%d iteration"%(i, len(goods))
            for c in range(ps_cpu_num+1):
                for m in range(ps_mem_num+1):
                    if i==0:
                        if goods[i][1]<=c and goods[i][2]<=m:
                            if target=="MEM":
                                bag[i][c][m] = goods[i][2]
                                #print "INIT: put in %s"%(goods[i][0])
                            elif target == "CPU":
                                bag[i][c][m] = goods[i][1]
                            bag_f[i][c][m].append(goods[i][0])
                    else:
                        if goods[i][1]<=c and goods[i][2]<=m:
                            t = 0
                            if target=="MEM":
                                t = goods[i][2]
                            elif target == "CPU":
                                t = goods[i][1]
                            bag[i][c][m], index = max(bag[i-1][c][m], bag[i-1][c-goods[i][1]][m-goods[i][2]]+t)
                            if index == 1:
                                bag_f[i][c][m] = bag_f[i-1][c][m][:]
                            elif index == 2:
                                bag_f[i][c][m] = bag_f[i-1][c-goods[i][1]][m-goods[i][2]][:]
                                bag_f[i][c][m].append(goods[i][0])
                        else:
                            bag[i][c][m] = bag[i-1][c][m]
                            bag_f[i][c][m] = bag_f[i-1][c][m][:]
        counter = 0
#        for i in range(len(bag)):
#            for j in range(len(bag[0])):
#                for o in range(len(bag[0][0])):
#                    print bag[i][j][o],
#            print '\r\n'
#        aa
        current_pServer = {}
        print "============"
        for g in bag_f[len(goods)-1][ps_cpu_num][ps_mem_num]:
            gc = fn_dict[g][1]
            gm = fn_dict[g][2]
            print "remove (%s, %d, %d)"%(g, gc, gm)
            goods.remove((g,gc,gm))
            try:
                current_pServer[g]+=1
            except KeyError:
                current_pServer[g] = 1
        pServers.append(current_pServer)

    return pServers, pServers_Res