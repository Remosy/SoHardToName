# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import cost_estimation
from tabulate import tabulate
trucks_amount = 16
truck_weight = 124
truck_max_weight = 330
load_time = (33.8 * 5 + 30 + 30 + 75) / 60 * 4 / 3
paths = []
scenario = 'scenario1.xlsx'
df = pd.read_excel(scenario,'Excavator01').convert_objects(convert_numeric=True).fillna(0).round(2)
paths.append(df.iloc[2:,0:5].values.astype(float))
df = pd.read_excel(scenario,'Excavator02').convert_objects(convert_numeric=True).fillna(0).round(2)
paths.append(df.iloc[2:,0:5].values.astype(float))
df = pd.read_excel(scenario,'Excavator03').convert_objects(convert_numeric=True).fillna(0).round(2)
paths.append(df.iloc[2:,0:5].values.astype(float))

#%%
N = 100
G = 100
T = 20
sigma = 10    
fric_coef = 0.02
weight = [1,1,1]

hist_cost = np.zeros((N,3))
def fitness(n,paths,loads,assignments):
    productivity = 0.0
    for i in range(0,3):
        cycle_cost = max(cost_estimation.query(paths[i],loads[i],fric_coef) / assignments[i],load_time)
        if assignments[i] == 1 :
            cycle_cost += load_time
        hist_cost[n,i] = cycle_cost
        productivity += (loads[i]-124) * (60 / cycle_cost) * weight[i]
    return productivity

def rand_pop(N, mu, sigma):
    pops = np.zeros((N,6),dtype = int)
    pops[:,:3] = np.random.normal(mu, sigma, (N,3)).astype(int)
    assignments = np.zeros((N,3), dtype = int)
    for i in range(0,N):
        for j in range(0,trucks_amount):
            assignments[i,np.random.randint(0,3)] += 1
    pops[:,3:] = assignments
    return pops

def mutate(pop, sigma):
    mutated = pop.copy()
    mutated[:3] += np.random.normal(0, sigma, 3).astype(int)
    np.clip(mutated[:3],124,330,mutated[:3])
    i = np.random.randint(3,6)
    j = np.random.randint(3,6)
    if (mutated[i] != 0):
        mutated[i] -= 1
        mutated[j] += 1
    return mutated

population = rand_pop(N, 180, 40)

for i in range(0,G):
    print(i)
    fvalues = np.zeros(N)
    for j in range(0,N):
        fvalues[j] = fitness(j,paths,population[j,:3],population[j,3:])
    index = np.flip(fvalues.argsort())
    hist_cost = hist_cost[index]
    population = population[index,:]
    new_pops = np.zeros((N,6),dtype = int)
    new_pops[0] = population[0]
    for j in range(1,N):
        new_pops[j] = mutate(population[np.random.randint(0,T)],sigma)
    population = new_pops
    
print(tabulate([population[0]], headers=[ 'Trucks to E1','Trucks to E2', 'Trucks to E3', 'Payload at E1','Payload at E2', ' Payload at E3'], tablefmt='orgtbl'))

#%%
import matplotlib.pyplot as plt
max_gross = 710
truck_weight = 124
cycle_time = np.zeros(max_gross-truck_weight)
prod = np.zeros(max_gross-truck_weight)

payload = range(0,max_gross-truck_weight)

for i in range(0,max_gross-truck_weight):
    cycle_time[i] = cost_estimation.query(paths[2],i + 124,0.02)
    prod[i] = i * 60 / cycle_time[i]

plt.figure()
plt.plot(payload,cycle_time)
plt.savefig('pvc.png')
plt.figure()
plt.plot(payload,prod)
plt.savefig('pvp.png')

#%%
prod = np.zeros(100)
fric_coef = np.zeros(100)
for i in range(0,100):
    fric_coef[i] = (i + 1) / 1000
    prod[i] = 200 * 60 / cost_estimation.query(paths[0],324,fric_coef[i])
    

plt.figure()
plt.plot(fric_coef,prod)
plt.savefig('fvp.png')

#%%
fric_coef = np.zeros(100)
cost = np.zeros(100)
for i in range(0,100):
    fric_coef[i] = (i + 1) / 1000
    cost[i] = cost_estimation.estimate(324,fric_coef[i],10,200,200,30)[0]

plt.figure()
plt.plot(fric_coef,cost)
    