# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 11:17:06 2018

@author: qyk13
"""

import pandas as pd
import numpy as np

data = pd.read_csv('Truck Cycle.csv')
data['Full slope length'] = data['Full slope length'].str.replace(',','')
data = data.iloc[:,6:9].values.astype(float)
data = data[~np.any(data == 0, axis = 1)]
points = np.zeros((data.shape[0],2))
points[:,0] = data[:,1]
points[:,1] = data[:,2] / data[:,0]
points[:,0] += 124

#%%
rs = pd.read_excel('road/Road Segment Data.xlsx').fillna(0).round(2)
