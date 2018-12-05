#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 04:05:56 2018

@author: gdcutting
"""

# model_run.py
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from graphviz import Digraph
#from SOCEconModel import *  # omit this in jupyter notebooks

model = SOCEconModel(1000,3,.4,.2,do_rewire=False,fix_demand=True)
incomes = []
demand = []
num_steps = 200
for i in range(num_steps):
    #model.period_income = 0
    model.step()
    
    incomes.append(model.period_income)
    demand.append(model.period_demand)
        
income_long_avg = np.convolve(incomes, np.ones((int(num_steps/40),))/int(num_steps/40), mode='valid')
income_short_avg = np.convolve(incomes, np.ones((int(num_steps/200),))/int(num_steps/200), mode='valid')
demand_coverage = sum(incomes)/sum(demand)

#print(incomes)
print('Total income:', model.total_income)
print('Demand coverage', demand_coverage)

#main income / demand plot
fig = plt.figure(1,figsize=(6,3))

if num_steps <= 5000:
    income_line, = plt.plot(incomes, label='Line 2')#,color='blue')
    demand_line, = plt.plot(demand, label='Line 1')#,color='red')
    income_avg_line, = plt.plot(income_long_avg, label='Line 1')#,color='yellow')
    plt.legend([income_line, demand_line,income_avg_line], ['Income', 'Demand', 'Average Income'],loc='best')
else:
    income_short_line, = plt.plot(income_short_avg, label='Line 2')#,color='blue')
    demand_line, = plt.plot(demand, label='Line 1')#,color='red')
    income_long_line, = plt.plot(income_long_avg, label='Line 1')#,color='yellow')
    plt.legend([income_short_line, demand_line,income_long_line], ['Income (short avg.)', 'Demand', 'Income (long avg.)'],loc='best')
    
plt.xlabel('Simulation time')
plt.ylabel('Units of product')
plt.ylim(bottom=0)
income_var = np.var(incomes)
income_sd = np.sqrt(income_var)
print(income_sd)
#textstr = 'Income:\n' + '\u03C3' + ' = ' + str(income_var)
#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5,)
#plt.text(0, 0,textstr, fontsize=12,verticalalignment='top', bbox=props)
#plt.rcParams["figure.figsize"] = [5,10]
plt.show()


cascade_list = list(model.cascades.values())

#plot cascade sizes and frequency in loglog
cascade_h = np.histogram(cascade_list, bins=50)
cascade_h_lim = [c for c in list(cascade_h[0]) if c >= 8]
l1 = plt.loglog(cascade_h_lim)
plt.xlabel('Log(cascade size)')
plt.ylabel('Log(cascade frequency)')
plt.show()

#for future network visualization
"""
agent_net_graph = nx.Graph()
for a in model.schedule.agents:
    for s in a.suppliers:
        agent_net_graph.add_edge(a.unique_id,s.unique_id)
       
plt.subplot(121)
nx.draw(agent_net_graph) # default spring_layout
plt.subplot(122)
nx.draw(agent_net_graph, pos=nx.random_layout(agent_net_graph), nodecolor='r', edge_color='b')
"""

"""
dot = Digraph(comment='The Round Table')
for a in model.schedule.agents:
    dot.node(str(a.unique_id), 'Agent'+str(a.unique_id))
for a in model.schedule.agents:
    for s in a.suppliers:
        dot.edge(str(a.unique_id), str(s.unique_id), constraint='false')
    
print(dot.source)
dot.render('agent_net.gv', view=True)
"""

"""
for agent in model.schedule.agents:
    #print(agent.suppliers)
    if len(agent.suppliers):
        print(agent.producer_level, agent.suppliers[0].producer_level)
"""