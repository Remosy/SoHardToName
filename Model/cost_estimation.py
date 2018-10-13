# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 13:22:34 2018

@author: qyk13
"""

import pandas as pd
import numpy as np
import math

rimpull = pd.read_excel('Truck_Spec.xlsx','Rimpull').convert_objects(convert_numeric=True).fillna(0).values
seg_hist = pd.read_csv('road/roadSegment.csv')

acc = 1.5

def getMaxV(force):
    i = -1
    while ((force < rimpull[i + 1, 1]) & (i != 60)): 
        i += 1
    if i == -1 : return 0
    lowf = rimpull[i + 1, 1]
    highf = rimpull[i, 1]
    lows = rimpull[i + 1, 0]
    highs = rimpull[i, 0]
    return (lows + (highs - lows) * (force - lowf) / (highf - lowf))/3.6

def estimate(load,startV,totalLength,slopeLength,slopeHeight):
    if (slopeHeight/slopeLength <= 0.01) :
        maxV = getMaxV(load * 120)
        accDistance = abs(startV - maxV) / acc * (startV + maxV) / 2
        if accDistance < totalLength:
            cost = (accDistance/ ((startV + maxV) / 2) + 
                    (totalLength - accDistance) / maxV)
            return (cost,maxV)
        else:
            cost = (-startV+math.sqrt(startV**2+3*totalLength))/acc
            endV = cost*acc + startV
            return (cost,endV)
    elif (totalLength - slopeLength <= 10):
        maxV = getMaxV(load * math.sin(slopeHeight/slopeLength) * 1000)
        accDistance = abs(startV - maxV) / acc * (startV + maxV) / 2
        if accDistance < totalLength:
            cost = (accDistance/ ((startV + maxV) / 2) + 
                    (totalLength - accDistance) / maxV)
            return (cost,maxV)
        else:
            cost = (-startV+math.sqrt(startV**2+3*totalLength))/acc
            endV = cost*acc + startV
            return (cost,endV)
    else:
        (cost1,endV) = estimate(load,startV,(totalLength - slopeLength) / 2,0)
        (cost2,endV) = estimate(load,endV,slopeLength,slopeHeight)
        (cost3,endV) = estimate(load,endV,(totalLength - slopeLength) / 2,0)
        return (cost1 + cost2 + cost3, endV)
    
def query(path,load):
    cost = 0.0
    startV = 0.0
    total = 0.0
    for i in range(path.shape[0]-1):
        
        tup = seg_hist[(seg_hist['x1']==path[i,1])&(seg_hist['y1']==path[i,0])&
                       (seg_hist['z1']==path[i,2])&(seg_hist['x2']==path[i+1,1])&
                       (seg_hist['y2']==path[i+1,0])&(seg_hist['z2']==path[i+1,2])]  
        if tup.empty:
            cost = path[i,3]
            startV = getMaxV(load * 120)
        else :(cost,startV) = estimate(load,startV,tup['EfhLength'].values[0],
                 tup['SlopeLength'].values[0],tup['RiseHeight'])
        total += cost + path[i+1,4]
    return total/60