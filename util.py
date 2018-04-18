#coding=utf-8
from __future__ import division
import parser
import random
import time
import matrix_
import math

def calcAB(x,y):
    n = len(x)
    sumX,sumY,sumXY,sumXX =0,0,0,0
    for i in range(0,n):
        sumX  += x[i]
        sumY  += y[i]
        sumXX += x[i]*x[i]
        sumXY += x[i]*y[i]
    a = (n*sumXY -sumX*sumY)/(n*sumXX -sumX*sumX)
    b = (sumXX*sumY - sumX*sumXY)/(n*sumXX-sumX*sumX)
    return a,b,

#xi = [1,2,3,4,5,6,7,8,9,10]
#yi = [10,11.5,12,13,14.5,15.5,16.8,17.3,18,18.7]
#a,b=calcAB(xi,yi)
#print("y = %10.5fx + %10.5f" %(a,b))
#x = np.linspace(0,10)
#y = a * x + b

def ls_predict(tData_xy=None, base_date=None, end_date=None, predict_start_date=None, predict_end_date=None, flavor_names=None):
    predict_flavors = []

    tDays = parser.cal_day(base_date, end_date)
    pDays = parser.cal_day(base_date, predict_end_date) - parser.cal_day(base_date, predict_start_date)
    

#    print tData_xy
    new_tData_xy = {}
    for each in flavor_names:
        x = []
        y = []
        new_tData_xy[each] = tData_xy[each][-7:]
        for t in new_tData_xy[each]:
            x.append(t[0])
            y.append(t[1])
        a, b = calcAB(x, y)
        print a, b
        num = a * (tDays+pDays)*1.0274 + b - tData_xy[each][-1][1] 
        if num == 0:
            num = 2
        #num = int(round(num*pDays/tDays))
        predict_flavors.append((each, int(num)))

    print predict_flavors
    
    return predict_flavors

def scale1(x, begin=-1, end=1):
    retx = []
    l = len(x)
    mid = (x[0]+x[-1])/2
    half = mid - x[0]
    for i in x:
        retx.append((i - mid)/half)

    return retx, x[0],x[-1]

def restore_scale1(x, begin=-1, end=1):
    retx = []
    l = len(x)
    mid = (begin + end)/2
    half = mid - begin
    for i in x:
        retx.append(i*half + mid)

    return retx

def eig(in_matrix):
    a = in_matrix[0][0]
    b = in_matrix[0][1]
    c = in_matrix[1][0]
    d = in_matrix[1][1]
    ans = [0, 0]
    if pow(a+d,2) - (4*(a*d) - 4*(b*c)) < 0:
        print 'invalid matrix, none re character number'
        return ans
    else:
        ans[0] = (a+d + math.sqrt((pow(a+d,2) - (4*(a*d) - 4*(b*c)))))/2
        ans[1] = (a+d - math.sqrt((pow(a+d,2) - (4*(a*d) - 4*(b*c)))))/2
    if ans[0] > ans[1]:
        namuda = ans[1]
    else :
        namuda = ans[0]
    tmp = b/(namuda - a)
    x1 = tmp/math.sqrt(1 + pow(tmp,2))
    x2 = 1/math.sqrt(1 + pow(tmp, 2))
    return ans, [x1, x2]


def calcAB2(xx,yy):
    x, x_begin, x_end = scale1(xx)
    y, y_begin, y_end = scale1(yy)

    n = len(x)

    sumX, sumY = 0, 0
    tmpx, tmpy = [], []
    for i in range(n):
        sumX += x[i]
        sumY += y[i]
        tmpx.append(x[i])
        tmpy.append(y[i])

    x_n = sumX/n
    y_n = sumX/n

    for i in range(n):
        tmpx[i] -= x_n
        tmpy[i] -= y_n
    X = [tmpx,tmpy]
    X_t = matrix_.transpose(X)

    prd = matrix_.mul(X, X_t)
    W, V = eig(prd)
    a = V[0]
    b = V[1]

    c = (-1*a*x_n)+(-1*b*y_n)
    a = -1*(a/b)
    b = -1*(c/b)

    return a,b, y_begin, y_end

def tls_predict(tData_xy=None, base_date=None, end_date=None, predict_start_date=None, predict_end_date=None, flavor_names=None):
    predict_flavors = []

    tDays = parser.cal_day(base_date, end_date)
    pDays = parser.cal_day(base_date, predict_end_date) - parser.cal_day(base_date, predict_start_date)
    

#    print tData_xy
    new_tData_xy = {}
    for each in flavor_names:
        x = []
        y = []
        new_tData_xy[each] = tData_xy[each][-7:]
        for t in new_tData_xy[each]:
            x.append(t[0])
            y.append(t[1])
        a, b, y_begin, y_end = calcAB2(x, y)
        print a, b
        
        mid = (x[0]+x[-1])/2
        half = mid - x[0]
        emm = (tDays+pDays - mid)/half

        py = a * (emm) * 1.0273 + b
        py = restore_scale1([py], y_begin, y_end)[0]
        if py < tData_xy[each][-1][1]:
            num = tData_xy[each][-1][1]
            num = int(round(num*pDays/tDays))
        else:
            num = py - tData_xy[each][-1][1] 
        #num = int(round(num*pDays/tDays))
        predict_flavors.append((each, int(num)))

    print predict_flavors
    
    return predict_flavors
'''
 3. Make prediction by averaging
 @param: tData_xy. xy denoted training data. x denotes date
 @param: base_date
 @param: end_date
 @param: predict_start_date
 @param: predict_end_date

 @output: predict_flavors. Array of (flavor_name, flavor_num) tuples
'''
def average_predict(tData_xy=None, base_date=None, end_date=None, predict_start_date=None, predict_end_date=None, flavor_names=None):
    predict_flavors = []

    tDays = parser.cal_day(base_date, end_date)
    pDays = parser.cal_day(base_date, predict_end_date) - parser.cal_day(base_date, predict_start_date)
    for each in flavor_names:
        num = tData_xy[each][-1][1]
        num = num*pDays/tDays
        predict_flavors.append((each, num))

    return predict_flavors

def selectFlavor(flavors=None, flavor_names=None, predict_flavors=None, target=None):
    biggest_f_name = ""
    biggest_f_num = 0
    biggest_f_cpu = 0
    biggest_f_mem = 0
    biggest_f_id = 0
    for f in flavors:
        if f[0] in flavor_names:
            if target == "CPU":
                if f[1] > biggest_f_cpu:
                    biggest_f_cpu = f[1]
                    biggest_f_mem = f[2]
                    biggest_f_name = f[0]
            elif target == "MEM":
                if f[2] > biggest_f_mem:
                    biggest_f_cpu = f[1]
                    biggest_f_mem = f[2]
                    biggest_f_name = f[0]

            for i in range(len(predict_flavors)):
                if predict_flavors[i][0] == biggest_f_name:
                    biggest_f_id = i
                    biggest_f_num = predict_flavors[i][1]

    #print "select %s as the flavor to load, \ncurrent number of it is %d, \nwe need %d cpu and %d MB of memory."%(biggest_f_name, biggest_f_num, biggest_f_cpu, biggest_f_mem)

    return biggest_f_name, biggest_f_num, biggest_f_cpu, biggest_f_mem, biggest_f_id


def ratio_selectFlavor(flavors=None, flavor_names=None, predict_flavors=None, target=None, current_ratio=None, cpu_remaining=None, mem_remaining=None):
    #print "SELECTING"
    best_f_name = ""
    best_f_num = 0
    best_f_cpu = 0
    best_f_mem = 0
    best_f_id = 0
    biggest = 0
    m = 1
    #print "Ratio is %f"%current_ratio
    for f in flavors:
        if f[0] in flavor_names:
            #print f[1], cpu_remaining, f[2], mem_remaining
            if f[1] <= cpu_remaining and f[2] <= mem_remaining:
                #print "%s requires %d cpu and %dGB of memory, we have %d cpu and %d GB of memory mem_remaining"%(f[0], f[1], f[2], cpu_remaining, mem_remaining)
                if target == "CPU":
                    if f[1] < biggest:
                        print ''
                        #print "%s has too little cpu to be selected"%f[0]
                    elif f[1] > biggest:
                        biggest = f[1]
                        best_f_cpu = f[1]
                        best_f_mem = f[2]
                        best_f_name = f[0]
                        m = abs(current_ratio - f[1]/f[2])
                        #print "%s has the most cpu. Take it as the best answer temporarily. and it's ratio is %f"%(f[0], m)
                elif target == "MEM":
                    if f[2] < biggest:
                        print ''
                        #print "%s has too little memory to be selected"%f[0]
                    elif f[2] > biggest:
                        biggest = f[2]
                        best_f_cpu = f[1]
                        best_f_mem = f[2]
                        best_f_name = f[0]
                        m = abs(current_ratio - f[1]/f[2])
                        #print "%s has the most mem. Take it as the best answer temporarily. and it's ratio is %f"%(f[0], m)
                tmpm = abs(current_ratio - f[1]/f[2])
                #print "tmpm is %f"%tmpm
                if tmpm < m:
                    m = tmpm
                    best_f_cpu = f[1]
                    best_f_mem = f[2]
                    best_f_name = f[0]
                    #print "tmpm is the least. Take %s as the best answer, and it's ratio is %f"%(best_f_name, m)
        #print "[[[[[[",predict_flavors
        for i in range(len(predict_flavors)):
            if predict_flavors[i][0] == best_f_name:
                best_f_id = i
                best_f_num = predict_flavors[i][1]

    #print "select %s as the flavor to load, \ncurrent number of it is %d, \nwe need %d cpu and %d MB of memory."%(best_f_name, best_f_num, best_f_cpu, best_f_mem)
    #print "[DEBUG] biggest_f_name: %s"%best_f_name
    return best_f_name, best_f_num, best_f_cpu, best_f_mem, best_f_id
'''
 Distribution
 @author: ainassine

 @param: ps_cpu_num.
 @param: ps_mem_num.
 @param: predict_flavors
 @param: flavor_names
 @param: flavors
 @param: target
 @param: pServers. Array of Required Physical Server. Array of dict of flavors
 @param: pServers_Res. Array of Resouces of required physical server. Array of (cpu, mem) tuples
 
 @Output: pServers
 @Output: pServers_Res
'''
def distribute(predict_flavors=None, ps_cpu_num=None, ps_mem_num=None, target=None, flavor_names=None, flavors=None):
    pServers = []
    pServers_Res = [] #pServers_Res[n] = (cpu, mem)

    finished = 0
    h = 0

    #print "TARGET is CPU"

    # remove flavors predicted whose number is 0
    fk = [] #flavors to be removed
    for f in predict_flavors:
        if f[1] == 0:
            fk.append(f)
    for f in fk:
        predict_flavors.remove(f)
        flavor_names.remove(f[0])

    '''
    For each flavor, try pServers in order to get distributed
    '''
    while(len(predict_flavors)):
        #print "Number of predict_flavors is %d"%len(predict_flavors)
        if len(pServers) == 0:
            #print "Add the first Physical server"
            dic = {}
            pServers.append(dic)
            pServers_Res.append((ps_cpu_num, ps_mem_num))

        biggest_f_name, biggest_f_num, biggest_f_cpu, biggest_f_mem, biggest_f_id = selectFlavor(flavors, flavor_names, predict_flavors, target)
        
        '''
        choose physical server to distribute flavor
        '''
        counter = 0
        for i in range(len(pServers_Res)):
            for counter in range(biggest_f_num):
                if pServers_Res[i][0]>biggest_f_cpu and pServers_Res[i][1]>biggest_f_mem:
                    #print "[LOAD]Counter: %d, loading a %s to pServer %d"%(counter,biggest_f_name, i)
                    pServers_Res[i] = (pServers_Res[i][0]-biggest_f_cpu, pServers_Res[i][1]-biggest_f_mem)
                    try:
                        pServers[i][biggest_f_name] = pServers[i][biggest_f_name] + 1
                    except KeyError:
                        pServers[i][biggest_f_name] = 1
                    #print "[pServer]pServer %d remains %d cpu %d MB of memory."%(i, pServers_Res[i][0],pServers_Res[i][1])
                else:
                    counter = counter - 1
                    break
            #print "biggest_f_num: %d, counter: %d"%(biggest_f_num, counter)
            biggest_f_num = biggest_f_num - counter - 1
            predict_flavors[biggest_f_id] = (biggest_f_name, biggest_f_num)
        if biggest_f_num == 0:
            #print len(predict_flavors)
            #print "%s has been loaded up."%biggest_f_name
            predict_flavors.remove((biggest_f_name, 0))
            flavor_names.remove(biggest_f_name)
            #print len(predict_flavors)
        else:
            dic = {}
            pServers.append(dic)
            pServers_Res.append((ps_cpu_num, ps_mem_num))
            #print "Added a physical server, we have %d pServers."%len(pServers)
        h = h + 1
        if h == 2:
            print ""

    return pServers, pServers_Res

def ratio_distribute(predict_flavors=None, ps_cpu_num=None, ps_mem_num=None, target=None, flavor_names=None, flavors=None):
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
    counter = 0
    while(len(predict_flavors)):
        
        cpu_num, mem_num = current_pServer_Res
        current_ratio = cpu_num/mem_num
        biggest_f_name, biggest_f_num, biggest_f_cpu, biggest_f_mem, biggest_f_id = ratio_selectFlavor(flavors, flavor_names, predict_flavors, target, current_ratio, cpu_num, mem_num)
        if biggest_f_name != "": # distributing
            try:
                current_pServer[biggest_f_name] = current_pServer[biggest_f_name] + 1
            except KeyError:
                current_pServer[biggest_f_name] = 1
            cpu_num = cpu_num - biggest_f_cpu
            mem_num = mem_num - biggest_f_mem

            current_pServer_Res = (cpu_num, mem_num)
            #print "[[[[%d"%biggest_f_num
            biggest_f_num = biggest_f_num - 1
            if biggest_f_num == 0:
                #print len(predict_flavors)
                #print "%s has been loaded up."%biggest_f_name
                predict_flavors.remove((biggest_f_name, 1))
                flavor_names.remove(biggest_f_name)
                #print len(predict_flavors)
            else:
                predict_flavors[biggest_f_id] = (biggest_f_name, biggest_f_num)
                #print predict_flavors[biggest_f_id]
            if (cpu_num == 0 or mem_num == 0) and len(predict_flavors) != 0:
                #print "CREATE A NEW PHYSICAL SERVER DUE TO RESOUCES RUN UP."
                pServers.append(current_pServer)
                pServers_Res.append(current_pServer_Res)
                current_pServer = {}
                current_pServer_Res = (ps_cpu_num, ps_mem_num)
        else:
            #print "CREATE A NEW PHYSICAL SERVER"
            pServers.append(current_pServer)
            pServers_Res.append(current_pServer_Res)
            current_pServer = {}
            current_pServer_Res = (ps_cpu_num, ps_mem_num)
    
    pServers.append(current_pServer)
    pServers_Res.append(current_pServer_Res)

    return pServers, pServers_Res

def max(a,b):
    if a>b:
        return a, 1
    else:
        return b, 2

def conti(current_pServer, goods):
    #print current_pServer
    #print "hhhhhh"
    ret = 0
    counter = len(current_pServer)
    #print counter
    for f, n in current_pServer.items():
        nn = 0
        for g in goods:
            if g[0] == f:
                nn +=1
        if nn >= n:
            ret+=1
        #print f, n, nn, ret
    return ret == counter

def dp_distribute(predict_flavors=None, ps_cpu_num=None, ps_mem_num=None, target=None, flavor_names=None, flavors=None):
    pServers = []

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
    init_num_goods = len(goods)
    newgoods = []
    while(len(newgoods)!=init_num_goods):
        max_cpu = 0
        max_mem = 0
        best_good = None
        for good in goods:
            if target == "CPU":
                if good[2]>max_mem:
                    max_cpu = good[1]
                    max_mem = good[2]
                    best_good = good
            elif target == "MEM":
                if good[1]>max_cpu:
                    max_cpu = good[1]
                    max_mem = good[2]
                    best_good = good
        newgoods.append(best_good)
        goods.remove(best_good)
    goods = newgoods
    
    print "创建数组：",
    tt1 = time.time()
    bag = [ [ [(0,0) for o in range(ps_mem_num+1)] for j in range(ps_cpu_num+1)] for i in range(init_num_goods)]
    bag_f = [ [ [[] for o in range(ps_mem_num+1)] for j in range(ps_cpu_num+1)] for i in range(init_num_goods)]
    tt2 = time.time()
    print tt2-tt1
    
    while(goods):
        num_goods = len(goods)
        best = False
        print "迭代："
        tt3 = time.time()
        for i in range(num_goods):
            if best:
                break
            #print "%d/%d iteration"%(i, num_goods), 
            t1 = time.time()
            for c in range(1,ps_cpu_num+1):
                for m in range(1,ps_mem_num+1):
                    good=goods[i]
                    if i==0:
                        if good[1]<=c and good[2]<=m:
                            #if target=="MEM":
                            #    bag[i][c][m] = goods[i][2]
                            #elif target == "CPU":
                            #    bag[i][c][m] = goods[i][1]
                            bag[i][c][m] = (good[1],good[2])
                            bag_f[i][c][m].append(good[0])
                    else:
                        if good[1]<=c and good[2]<=m:
                            t = (good[1],good[2])
                            putc = bag[i-1][c-t[0]][m-t[1]][0] + t[0]
                            putm = bag[i-1][c-t[0]][m-t[1]][1] + t[1]
                            nputc = bag[i-1][c][m][0]
                            nputm = bag[i-1][c][m][1]
                            # 1: not put, 2: put
                            if target == "CPU":
                                if putc > nputc:
                                    bag[i][c][m] = (putc, putm)
                                    index = 2
                                elif putc < nputc:
                                    bag[i][c][m] = (nputc,nputm)
                                    index = 1
                                elif putc == nputc:
                                    if putm < nputm:
                                        bag[i][c][m] = (nputc, nputm)
                                        index = 1
                                    elif putm >= nputm:
                                        bag[i][c][m] = (putc, putm)
                                        index = 2
                            elif target == "MEM":
                                if putm > nputm:
                                    bag[i][c][m] = (putc, putm)
                                    index = 2
                                elif putm < nputm:
                                    bag[i][c][m] = (nputc,nputm)
                                    index = 1
                                elif putm == nputm:
                                    if putc < nputc:
                                        bag[i][c][m] = (nputc, nputm)
                                        index = 1
                                    elif putc >= nputc:
                                        bag[i][c][m] = (putc, putm)
                                        index = 2
                            #bag[i][c][m], index = max(bag[i-1][c][m], bag[i-1][c-goods[i][1]][m-goods[i][2]]+t)
                            if index == 1:
                                bag_f[i][c][m] = bag_f[i-1][c][m][:]
                            elif index == 2:
                                bag_f[i][c][m] = bag_f[i-1][c-goods[i][1]][m-goods[i][2]][:]
                                bag_f[i][c][m].append(goods[i][0])
                        else:
                            bag[i][c][m] = bag[i-1][c][m]
                            bag_f[i][c][m] = bag_f[i-1][c][m][:]

                        if bag[i][c][m][0]==ps_cpu_num and bag[i][c][m][1]==ps_mem_num:
                            print "BOOM!!!"
                            bag[num_goods-1][ps_cpu_num][ps_mem_num] = bag[i][c][m]
                            bag_f[num_goods-1][ps_cpu_num][ps_mem_num] = bag_f[i][c][m]
                            best = True
                        #print bag_f[i][c][m]
            t2=time.time()
            #print t2-t1,
            tt4 = time.time()
            #print tt4-tt3
            
            #print t2-t1
            if i == -1:
                aa
        current_pServer = {}
#        for i in range(len(bag)):
#            for j in range(len(bag[0])):
#                for o in range(len(bag[0][0])):
#                    print bag[i][j][o],
#            print '\r\n'
#        aa
        print "============"
        best_c = 0
        best_m = 0
        best_cc = 0
        best_mm = 0
        for c in range(ps_cpu_num+1):
            for m in range(ps_mem_num+1):
                #print c,m,bag[len(goods)-1][c][m][0], bag[len(goods)-1][c][m][1]
                if bag[len(goods)-1][c][m][0]>best_cc:
                    best_c = c
                    best_m = m
                    best_cc = bag[len(goods)-1][c][m][0]
                    best_mm = bag[len(goods)-1][c][m][1]
                if bag[len(goods)-1][c][m][0]==best_cc:
                    if bag[len(goods)-1][c][m][1]>best_mm:
                        best_c = c
                        best_m = m
                        best_cc = bag[len(goods)-1][c][m][0]
                        best_mm = bag[len(goods)-1][c][m][1]
        #best_c = ps_cpu_num
        #best_m = ps_mem_num
        for g in bag_f[num_goods-1][best_c][best_m]:
            gc = fn_dict[g][1]
            gm = fn_dict[g][2]
            #print "remove (%s, %d, %d)"%(g, gc, gm)
            goods.remove((g,gc,gm))
            try:
                current_pServer[g]+=1
            except KeyError:
                current_pServer[g] = 1
        pServers.append(current_pServer)

        while(conti(current_pServer, goods)):
            for g in bag_f[num_goods-1][best_c][best_m]:
                gc = fn_dict[g][1]
                gm = fn_dict[g][2]
                #print "remove (%s, %d, %d)"%(g, gc, gm)
                goods.remove((g,gc,gm))
            pServers.append(current_pServer)

        print "遍历数组重置",
        ttt1= time.time()
        for i in range(num_goods):
            for j in range(ps_cpu_num+1):
                for o in range(ps_mem_num+1):
                    bag[i][j][o] = (0,0)
                    bag_f[i][j][o] = []
        ttt2= time.time()
        print ttt2-ttt1
        


    return pServers
