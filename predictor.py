#coding=utf8
from __future__ import division
import parser
import util
import time

InputInfo = 0

def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []

    
    '''
     1. Extract info
     @input: input_lines. Array of strings

     @param: ps_cpu_num. It is the number of cpu in a Physical Machine
     @param: ps_mem_num. It is the capacity of the memory of a Physical Machine
     @param: ps_disk_num. It is the capacity of the disk of a Physical Machine. Note that currently it's of no use
     @param: flavors is the flavors we're concerned about. For a certain flavor, 
                                            flavors[n][0] is the name of the flavor
                                            flavors[n][1] is the cpu num of the flavor
                                            flavors[n][2] is the mem of the flavor
     @param: flavor_num. Total number of flavors we're concerned about
     @param: target. It is the target resouce that we should make the most use of.
     @param: predict_start_date. Start date of the predicting period
     @param: predict_end_date. End date of the predicting period

     @output: params above
    '''
    ps_cpu_num = 0 
    ps_mem_num = 0 #GB
    ps_disk_num = 0 #GB
    flavors = []
    flavor_num = 0
    target = ""
    predict_start_date = ""
    predict_end_date = ""

    ps_cpu_num, ps_mem_num, ps_disk_num, flavors, target, predict_start_date, predict_end_date = parser.extract_info(input_lines)
    flavor_num = len(flavors)
    if InputInfo == 1:
        print "[Info]"
        print "Physical Server:"
        print "\tnumber of CPU: %d"%ps_cpu_num
        print "\tcapacity of MEM: %d"%ps_mem_num
        print "\tcapacity of DISK: %d"%ps_disk_num
        print "Flavor:"
        print "\tnumber of flavors: %d"%flavor_num
        print "Target:"
        print "\t%s"%target
        print "Date start: %s"%predict_start_date
        print "Date start: %s"%predict_end_date

    
    '''
     2. Extract data
     @input: ecs_lines. Array of strings

     @param: VM_ID_array: Array of id of Virtual Machines in training data set. Note that currently it's of no use.
     @param: flavor_array: Array of flavors appeared in training data set, and it's ordered by the seqence of appearance.
     @param: timestamp_array: Array of timestamp in training data set, and it's ordered by the seqence of appearance.
     @param: base_date: Start date of training data.
     @param: end_date: End date of training data.
     @param: flavor_names: names of flavors we're concerned about
    '''
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result

    VM_ID_array = []
    flavor_array = []
    timestamp_array = []
    parser.extract_data(ecs_lines, VM_ID_array, flavor_array, timestamp_array)
    base_date = timestamp_array[0]
    end_date = timestamp_array[-1]
    flavor_names = []
    for each in flavors:
        flavor_names.append(each[0])

    '''
     data for training 
     tData is a dict,
     tData['flavorname'] is an array of a certain flavor
     tData['flavorname'][] contains a tuple (time, number), number is the number of flavor that day
    '''
    tData = parser.get_tData(flavor_array, timestamp_array)
    #tData = util.rm_noise(tData)
    tData_xy = parser.convert2xy(tData, base_date)
    #print tData['flavor11']
    #print tData_xy['flavor11']
    
    '''
     3. Make prediction
     @param: tData_xy. xy denoted training data. x denotes date
     @param: base_date
     @param: end_date
     @param: predict_start_date
     @param: predict_end_date

     @output: predict_flavors. Array of (flavor_name, flavor_num) tuples
    '''
    predict_flavors = util.ls_predict(tData_xy, base_date, end_date, predict_start_date, predict_end_date, flavor_names)
    #predict_flavors = util.p1SLR_predict(tData_xy, base_date, end_date, predict_start_date, predict_end_date, flavor_names)

    print predict_flavors
    # record prediction
    predict_flavors_total_num = 0
    for f, n in predict_flavors:
        predict_flavors_total_num = predict_flavors_total_num + n
    result.append(predict_flavors_total_num)
    for f, n in predict_flavors:
        s = "%s %d"%(f,n)
        result.append(s)
    result.append("")

    '''
     4. Distribution
     @param: predict_flavors
     @param: flavor_names
     @param: flavors
     @param: ps_cpu_num.
     @param: ps_mem_num.
     @param: target
     @param: pServers. Array of Required Physical Server. Array of dict of flavors
     @param: pServers_Res. Array of Resouces of required physical server. Array of (cpu, mem) tuples
     
     @Output: pServers
     @Output: pServers_Res
    '''
    if 0:
        total_cpu_num = 0
        total_mem_num = 0
        for f in predict_flavors:
            fname, num = f
            n = 0
            for i in range (len(flavors)):
                if fname == flavors[i][0]:
                    n = i
                    break
            total_cpu_num = total_cpu_num + num * flavors[n][1]
            total_mem_num = total_mem_num + num * flavors[n][2]

        print "We need %d cpu in total."%total_cpu_num
        print "We need %dMB of mem in total"%total_mem_num
    
    num_vs = 0
    for pf in predict_flavors:
        fname, fnum = pf
        num_vs += fnum
    print num_vs

    pServers = []
    #pServers_Res = [] #pServers_Res[n] = (cpu, mem)
    #pServers, pServers_Res = util.dp_distribute(predict_flavors, ps_cpu_num, ps_mem_num, target, flavor_names, flavors)
    if num_vs >= 600:
        pServers, _ = util.ratio_distribute(predict_flavors, ps_cpu_num, ps_mem_num, target, flavor_names, flavors)
    else:
        pServers = util.dp_distribute(predict_flavors, ps_cpu_num, ps_mem_num, target, flavor_names, flavors)
    # 5. Record the result
    print "recording the result"
    
    result.append(len(pServers))
    for i in range(len(pServers)):
        s = ""
        for f, n in pServers[i].items():
            tmp = "%s %d "%(f, n)
            s = s + tmp
        s = "%d %s"%(i+1, s)
        result.append(s)
    for each in result:
        print each
    return result








