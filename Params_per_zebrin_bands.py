# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:54:36 2019

Inputs : excel file from PREPARE_PCA.py 

@author: ludov
"""

datapath = 'D:/PCA/NEW/Charge_PATTERNS.xlsx'

output_path = 'D:/PCA/NEW/Charge_PARAMS_PER_BANDS.xlsx'

GROUPS = ['WT','ENR','CUFF_1_MONTH','SHAM_1_MONTH','CUFF_15_DAYS','SHAM_15_DAYS']

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
import pandas as pd 

data_file = pd.ExcelFile(datapath)

list_sheets = data_file.sheet_names

#------------------------------------------------------------------------------

def clusterize(bands,pattern,positions,method='median'):
    '''
    Clusterize synaptic charge according to method in each zebrin band from a given cell
    Inputs:
        bands (array) : the zebrin bands values (.values from excel file)
        pattern (array) : the 1D pattern (charge or amp)
        positions (array) : the 1D position array 
        method (str) : mean or median
        
    Output :
        cluster (array) : array with computed median for each zebrin band as 
        ['P2mCL','P2mCM','P2pC','P1mCL','P1mCM','P1p','P1mIM','P1mIL','P2pI','P2mIM','P2mIL']        
    '''
    import numpy as np
    
    assert len(bands) == 8, 'Zebrin array does not match'
    assert len(pattern) == len (positions), 'Not same number of values in pattern and positions'
     
    P2mCL = float(bands[0])
    P2pC = float(bands[1])
    P1mCL = float(bands[2])
    P1p = float(bands[3])
    
    P1mIL = 100.
    P1mIM = 33.        
    P2pI = float(bands[6])

    P2mIL = float(bands[7])
    P2mIM = P2mIL-((P2mIL-P2pI)/2.)
    
    P2mCM = P2mCL-((P2mCL-P2pC)/2.)
    P1mCM = P1mCL-((P1mCL-P1p)/2.)
    
    
    zebrin_start = np.array([P2mCL,P2mCM,P2pC,P1mCL,P1mCM,P1p,0,P1mIM,P1mIL,P2pI,P2mIM])
    zebrin_stop = np.array([P2mCM,P2pC,P1mCL,P1mCM,P1p,0,P1mIM,P1mIL,P2pI,P2mIM,P2mIL])
    
    cluster = []
    
    for start, stop in zip(zebrin_start,zebrin_stop):
        
        temp = []
        
        for site,pos in zip(pattern, positions) : 
            if start <= pos < stop:
                temp.append(site)
                
        if not temp :
            cluster.append(0.)
        else:
            if method == 'median':
                cluster.append(np.nanmedian(temp))
            
            elif method == 'mean':
                cluster.append(np.nanmean(temp))
            
    return np.asarray(cluster)

#------------------------------------------------------------------------------        

with pd.ExcelWriter(output_path) as writer:
    
    ALL_MEDS, ALL_AVG, ALL_COND, ALL_MANIP = [],[],[],[]
    
    for group in GROUPS :
    
        print ('----------------------')
        print ('{} data group'.format(group))
        
        #All the patterns for a given group
        patterns = pd.read_excel(datapath,header=0,
                                 sheetname='{}_Charge_patterns'.format(group))
        
        #All the positions for a given group
        positions = pd.read_excel(datapath,header=0,
                                  sheetname='{}_Charge_positions'.format(group))
        
        #And the zebrin values
        zebrin_file=pd.read_excel('D:/01_ANALYSIS/Mesures_ZII_HighRes_WT_Cuff_Sham_Enr.xlsx',
                                  header=1,index_col=0,sheetname=group)
        
        #List of manips in each group
        manips = patterns.index
        
        MED,AVG = [],[]
        cols = ['P2mCL','P2mCM','P2pC','P1mCL','P1mCM','P1p',
                'P1mIM','P1mIL','P2pI','P2mIM','P2mIL']

        for cell in manips : 
            
            print ()
            #Individual patterns, position and bands
            print ('Loading {} charge pattern'.format(cell))
            charges = patterns.loc[cell].values
            
            position = positions.loc[cell].values

            bands = zebrin_file.loc[['{} norm_P1-'.format(cell)],
                                     'P2- contra':'P2- ipsi'].values.ravel()
            
            #Clusterize 
            MED.append(clusterize(bands,charges,position,method='median'))
            AVG.append(clusterize(bands,charges,position,method='mean'))
            
            ALL_MEDS.append(clusterize(bands,charges,position,method='median'))
            ALL_AVG.append(clusterize(bands,charges,position,method='mean'))
            ALL_MANIP.append(cell)
            ALL_COND.append(group)
            print ('DONE')
        
        #Save each condition to Excel File
        MED_df = pd.DataFrame(MED,index=manips,columns=cols)
        AVG_df = pd.DataFrame(AVG,index=manips,columns=cols)
        
        MED_df.to_excel(writer,sheet_name='{}_Median_Charge'.format(group))
        AVG_df.to_excel(writer,sheet_name='{}_Average_Charge'.format(group))
        
    #Save everything in one sheet
    ALL_MED_df = pd.DataFrame(ALL_MEDS,index=ALL_MANIP,columns=cols)
    ALL_AVG_df = pd.DataFrame(ALL_AVG,index=ALL_MANIP,columns=cols)
    ALL_COND_df = pd.DataFrame(ALL_COND,index=ALL_MANIP)
    
    
    ALL_MED_df.to_excel(writer,sheet_name='ALL_MEDIAN_CHARGES')
    ALL_AVG_df.to_excel(writer,sheet_name='ALL_AVERAGE_CHARGES')
    ALL_COND_df.to_excel(writer,sheet_name='ALL_CONDITIONS')
    
            
        

                    
