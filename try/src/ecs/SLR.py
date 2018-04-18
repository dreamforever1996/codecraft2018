#coding=utf8
#（SLR）使用最小二乘法预测,截距b等于训练样本y的平均值减去训练样本x的平均值乘以斜率w
#并且斜率w等于训练样本x乘以对应的y的和减去x的平均值乘以y的平均值乘以样本个数n，
#然后结果再除以样本每个x的值的平方减去个数n乘以x的平均值的平方
#slope为斜率w,intercept为截距b，结果返回为slope和intercept的值


#slope:预测的直线的斜率
def getXY(dataSet):
    x = [];y = []
    dict_flavors_xy = {}
    dict_keys = dataSet.keys()
    for each_key in dict_keys:
        dict_flavors_xy[each_key] = [[],[]]
        for x, y in dataSet[each_key]:
          #  if (len(dict_flavors_xy[each_key]) == 0):
           #     dict_flavors_xy[each_key] = [[],[]]
            dict_flavors_xy[each_key][0].append(x)
            dict_flavors_xy[each_key][1].append(y)
    return dict_flavors_xy

def SLR(x, y):
    slope = 0.0 
    intercept = 0
    len_x = len(x)

    sumX = 0.0
    sumY = 0.0
    #sumX2 = 0.0

    #循环一次得到平均值
    for i in range(len_x):
        sumX  += int(x[i])
        sumY  += int(y[i])
     #   sumX2 += x[i]*x[i]

    if len_x == 0:
	average_x = 0
	average_y = 0
    else:
        average_x = sumX/len_x
        average_y = sumY/len_x
    sumXX  = 0
    sumXY  = 0
    

    
    #循环一次得到方差
    for i in range(len_x):
	sumXX += (x[i] - average_x) * (x[i] - average_x)
	sumXY += (x[i] - average_x) * (y[i] - average_y)

    #计算斜率和截距b
    if sumXX > 0:
        slope = sumXY / sumXX
    else :
        slope = 0
    intercept = average_y - slope*average_x
    
    return slope, intercept

def get_flavors_wb(dataSet):
    dict_flavors_xy = getXY(dataSet)
    dict_flavors_wb = {}
    flavorkey = tuple(dict_flavors_xy.keys())
    for i in range(len(flavorkey)):
        eachX, eachY = dict_flavors_xy[flavorkey[i]]
        dict_flavors_wb[flavorkey[i]] = SLR(eachX,eachY)
    return dict_flavors_wb
