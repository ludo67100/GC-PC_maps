# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:48:42 2019

@author: ludov
"""

import numpy as np 
from matplotlib import pyplot as plt

from scipy import trapz 

animal_list = ['AI','AII','AIII','BI','BII','BIII','BIV',
               'CI','CII','CIII','CIV','DI','DII','DIII',
               'DIV'] #List your animals here

is_sham = [True, False, False, False, False, False, False,
           True, True, True, True, False, False, False,
           False, True] #True if animal is sham, False if animal if cuffed

baseline =['BL_Day_6','BL_Day_8']
conditions =['Cuff_Day_2','Cuff_Day_4','Cuff_Day_9','Cuff_Day_14','Cuff_Day_15','Cuff_Day_21','Cuff_Day_28','Cuff_Day_33']

path = 'C:/Users/ludov/Documents/Catwalk/Individual Analysis'


def compute_baseline(path,animal,trials):
    
    BASELINE_INDEX = []
    
    for trial in trials:
        
        data = '{}/{}/{}_TRACES.csv'.format(path,trial,animal)
        
        trace = np.genfromtxt(data,delimiter='').reshape((16,3,-1))
        
        CHARGES = []
        for i in range(trace.shape[0]):
            
            sinus = trace[i,2,:]
            clean_trace = sinus[np.logical_not(np.isnan(sinus))]
            
            #Discard empty trials 
            if len(clean_trace) == 0:
                continue
            
            else:
                charge = trapz(clean_trace,dx=0.0001)
                
                CHARGES.append(charge)
                
        BASELINE_INDEX.append(np.nanmean(CHARGES))
        
    return [np.nanmean(BASELINE_INDEX), np.nanstd(BASELINE_INDEX), 
            np.nanstd(BASELINE_INDEX)/np.sqrt(len(BASELINE_INDEX))]




def compute_timecourse(path,animal,trials):
    
    TIMECOURSE = []
    
    for trial in trials:
        
        data = '{}/{}/{}_TRACES.csv'.format(path,trial,animal)
        
        trace = np.genfromtxt(data,delimiter='').reshape((16,3,-1))
        
        CHARGES = []
        for i in range(trace.shape[0]):
            
            sinus = trace[i,2,:]
            clean_trace = sinus[np.logical_not(np.isnan(sinus))]
            
            #Discard empty trials 
            if len(clean_trace) == 0:
                continue
            
            else:
                charge = trapz(clean_trace,dx=0.0001)
                
                CHARGES.append(charge)
                
        TIMECOURSE.append(np.nanmean(CHARGES))
        
    return TIMECOURSE


test_baseline = compute_baseline(path,'AII',baseline)[0]

test_timecourse = compute_timecourse(path,'AII',conditions)

final = np.hstack((test_baseline, test_timecourse))

norm_final = final/test_baseline


plt.plot(norm_final)

