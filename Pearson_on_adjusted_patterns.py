# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 23:50:09 2020

@author: ludov
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

url = 'C:/Users/ludov/Documents/00_ANALYSIS/03_FORMATED_DATA/ELECTROPHY/WT'

mouseList=['{}/{}'.format(url,x) for x in os.listdir(url)]

#First identify the extreme limits of the maps:
#We take the shortest map on each side as reference for futur slicing
MIN, MAX = [],[]

for path in mouseList:
    
    pattern=np.genfromtxt('{}/{}_Amp_max_OK.csv'.format(path,path.split('/')[-1]),
                          delimiter=',')
    
    
    positions=np.genfromtxt('{}/{}_Positions_cp_centered_OK.csv'.format(path,path.split('/')[-1]),
                            delimiter=',')
    
    MIN.append(positions[0])
    MAX.append(positions[-1])
    
minBorder = max(MIN)
maxBorder = min(MAX)

print ('patterns will be sliced between {} and {} %'.format(round(minBorder,2),round(maxBorder,2)))
    
#Now the serious business
MANIPS=[]

plt.figure()

for path,idx in zip(mouseList,range(len(mouseList))):
    
    pattern=np.genfromtxt('{}/{}_Amp_max_OK.csv'.format(path,path.split('/')[-1]),
                          delimiter=',')
    
    positions=np.genfromtxt('{}/{}_Positions_cp_centered_OK.csv'.format(path,path.split('/')[-1]),
                            delimiter=',')
   
    MANIPS.append(path.split('/')[-1])
    
    leftBorder = np.asarray(np.where(positions>=minBorder))
    rightBorder = np.asarray(np.where(positions<=maxBorder))
    
    slicedPattern=pattern[leftBorder[0][0]:rightBorder[0][-1]]
    slicedPositions=positions[leftBorder[0][0]:rightBorder[0][-1]]
    
    plt.plot(slicedPositions,slicedPattern)
    
    print (len(slicedPattern))

    
    
