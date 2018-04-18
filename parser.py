#coding=utf-8

import time
import datetime

def cal_day(base_date = None, dest_date = None):
    date1 = time.strptime(base_date, "%Y-%m-%d")
    date2 = time.strptime(dest_date, "%Y-%m-%d")
    date1=datetime.datetime(date1[0],date1[1],date1[2])
    date2=datetime.datetime(date2[0],date2[1],date2[2])
    days = (date2-date1).days

    return days

def extract_info(input_=None):
    print "[PARSER] Extracting info..."
    ps_cpu_num = 0 
    ps_mem_num = 0 #GB
    ps_disk_num = 0 #GB
    flavors = []
    target = ""
    predict_start_date = ""
    predict_end_date = ""
    flavor_num = 0

    counter = 0
    target_line_number = 0
    startDate_line_number = 0
    endDate_line_number = 0
    for line in input_:
        if flavor_num != 0:
            values = line.split(" ")
            flavor_name = values[0]
            flavor_cpu_num = int(values[1])
            flavor_mem_num = int(values[2])/1024
            flavors.append((flavor_name, flavor_cpu_num, flavor_mem_num))
            flavor_num = flavor_num - 1

        if counter == 0:
            values = line.split(" ")
            ps_cpu_num = int(values[0])
            ps_mem_num = int(values[1])
            ps_disk_num = int(values[2])
        elif counter == 2:
            flavor_num = int(line)
            target_line_number = counter + flavor_num + 2
            startDate_line_number = target_line_number + 2
            endDate_line_number = startDate_line_number + 1
        elif counter == target_line_number:
            target = line.split("\r\n")[0]
        elif counter == startDate_line_number:
            line = line.split('\r\n')[0]
            t = time.mktime(time.strptime(line, "%Y-%m-%d %H:%M:%S"))
            localtime = time.localtime(t)
            predict_start_date = time.strftime("%Y-%m-%d", localtime)
        elif counter == endDate_line_number:
            line = line.split('\r\n')[0]
            t = time.mktime(time.strptime(line, "%Y-%m-%d %H:%M:%S"))
            localtime = time.localtime(t)
            predict_end_date = time.strftime("%Y-%m-%d", localtime)

        counter = counter + 1


    print "[PARSER/] Info has been extracted."

    return ps_cpu_num, ps_mem_num, ps_disk_num, flavors, target, predict_start_date, predict_end_date

def extract_data(input_=None, VM_ID_array=[], flavor_array=[], timestamp_array=[]):
    print "[PARSER] Extracting data..."

    for line in input_:
        if line == "":
            continue
        element_array = line.split('\t')
        VM_ID_array.append(element_array[0])
        flavor_array.append(element_array[1])
        element_array[2] = element_array[2].split('\r\n')[0]
        t = time.mktime(time.strptime(element_array[2], "%Y-%m-%d %H:%M:%S"))
        localtime = time.localtime(t)
        timestamp = time.strftime("%Y-%m-%d", localtime)
        timestamp_array.append(timestamp)

    print "[PARSER/] Data has been extracted."

def get_tData(flavor_array = None, timestamp_array = None):
    print "[PARSER] Getting time-num data..."
    tData={} 
    for flavor, time in zip(flavor_array, timestamp_array):
        #print "%s, %s"%(time, flavor)
        #if flavor != 'flavor11':
        #    continue
        try:
            f = tData[flavor]
        except KeyError:
            tData[flavor] = []
            f = tData[flavor]
        
        if len(f) == 0:
            f.append((time, 1))
        else:
            num = f[-1][1] + 1
            if time == f[-1][0]:
                f[-1] = (time, num)
            else:
                f.append((time, num))

    print "[PARSER/] Time-num data got."
    return tData

def convert2xy(tData = None, base_date = None):
    print "[PARSER] Converting time-num data to xy data..."
    tData_xy = {}
    for key, f in tData.items():
        for i in range(len(f)):
            date = f[i][0]
            num = f[i][1]
            date = cal_day(base_date, date)
            f[i] = (date, num)
        tData_xy[key]=f

    print "[PARSER/] Time-num data have been converted to  xy data."
    return tData_xy






