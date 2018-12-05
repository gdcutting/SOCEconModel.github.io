#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 02:16:46 2018

@author: gdcutting
"""

# server.py
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from .model import ACSEconModel

chart = ChartModule([{"Label": "Income","Color": "Black"},
                     {"Label": "Demand","Color": "Red"}],
                    data_collector_name='data_collector')

"""
model_params = {'num_agents': UserSettableParameter('slider', 'Number of agents', 10, 10, 100, 1,
                                       description='Choose how many agents to include in the model'),
                'p_consumers': UserSettableParameter('slider', 'Number of agents', 0, .5, 1, .1,
                                       description='What proportion of agents are consumers'),
                                                    
                 "width": 10, 
                 "height": 10}
"""

server = ModularServer(SOCEconModel,
                       [chart],
                       "SOC Econ Model",
                       {"num_agents": UserSettableParameter('slider', 'Number of agents', 100, 10, 50000, 10,
                                       description='Choose how many agents to include in the model'), 
                        "production_levels": UserSettableParameter('slider', 'Number of production levels', 3, 2, 10, 1,
                                       description='Choose how many levels of production to include in the model'),
                        "p_consumers": UserSettableParameter('slider', 'Proportion of consumers', .5, .1, .9, .1,
                                       description='What proportion of agents are consumers'),
                        "p_orders": UserSettableParameter('slider', 'P(order)', .05, .001, .2, .001,
                                       description='Probability that each consumer places an order in each period'),
                        "do_rewire": False})

#model_params
