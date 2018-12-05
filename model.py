#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 04:01:48 2018

@author: gdcutting
"""

# model.py

import random
from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

#functions for data reporting with data collector
def get_period_income(self):
    return self.period_income

def get_period_demand(self):
    return self.period_demand

class SOCEconModel(Model):
    def __init__(self, num_agents, production_levels, p_consumers, p_orders, do_rewire, fix_demand):
        #random seeds for checkpointing model runs if necessary
        #random.seed(1234)
        #random.seed(4321)
        
        #model variables
        self.num_agents = num_agents
        self.num_products = 5
        self.p_consumers = p_consumers
        self.num_consumers = 0
        self.p_orders = p_orders
        self.do_rewire = do_rewire
        self.fix_demand = fix_demand
        self.products = []
        self.production_levels = production_levels
        self.num_suppliers = 2
        self.period_demand = 0
        self.period_income = 0
        self.total_income = 0
        self.cascades = {}
        #self.reactions = []
        
        self.schedule = RandomActivation(self)
        
        #data collector for visualization
        self.data_collector = DataCollector(model_reporters={"Income": get_period_income,
                                                             "Demand": get_period_demand})
        
    # Create agents
        for i in range(self.num_agents):
            a = EconAgent(i, self)
            self.schedule.add(a)
        
        #assign each producer to two suppliers
        for l in range(0, self.production_levels):
            print("Agents at level ", l)
            next_level_p = []
            for agent in self.schedule.agents:
                if agent.producer_level == l + 1:
                    next_level_p.append(agent)
            for agent in self.schedule.agents:
                if agent.producer_level == l:
                    for supp_num in range(1,self.num_suppliers+1):
                        agent.suppliers.append(random.choice(next_level_p))
        
        for agent in self.schedule.agents:
            #debugging output
            #if agent.producer_level < self.production_levels:
            #print('Agent ', agent.unique_id, 'has production level ', agent.producer_level, ' and suppliers: ', agent.suppliers[0].unique_id, agent.suppliers[1].unique_id)
            #print('Agent ', agent.unique_id, 'has production level ', agent.producer_level, ' and suppliers: ', agent.suppliers)
            do_something = False
            
        self.running = True
        self.data_collector.collect(self)

    def step(self):
        #step model forward
        self.period_income = 0
        self.period_demand = 0
        self.order_agents = []
        #calculate number of orders for specified demand p
        self.num_orders = int(self.p_orders * self.num_consumers)
        self.consumers = [a.unique_id for a in self.schedule.agents if a.producer_level == 0]
        while len(self.order_agents) < self.num_orders:
            this_agent = random.choice(self.consumers)
            if not this_agent in self.order_agents:
                self.order_agents.append(this_agent)
        if self.fix_demand == False:
            for ra in range(int(.1*len(self.order_agents))):
                self.order_agents.append(random.choice(self.consumers))
            
        #print(self.order_agents, len(self.order_agents))
        #add agent (population growth)
        #turned off for now
        if random.random() < 0:
            a = EconAgent(self.num_agents, self)
            self.schedule.add(a)
            self.num_agents += 1
        self.schedule.step()
        self.data_collector.collect(self)

class EconAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #initialize agent variables (some not currently used)
        self.wealth = 0
        self.income = 0
        self.MPC = random.random()
        self.is_producer = False
        self.demand = {}
        self.inventory = random.randint(0,1)
        self.input_inventory = [0,0]
        self.supply = {}
        self.producer_level = 0
        self.suppliers = []
        self.output_orders = []
        self.input_orders = []
        
        #order history for rewiring
        self.order_history = [[],[]]
        for ns in range(model.num_suppliers):
            self.order_history[ns] = []
        
        self.cascade_id = -1
        
        if random.random() > self.model.p_consumers:
            self.is_producer = True
            #self.wealth = random.gauss(1000000,100000)
            self.producer_level = random.randint(1,self.model.production_levels)
        else:
            self.is_producer = False
            self.producer_level = 0
            self.wealth = random.gauss(50000,50000)
            self.demand[random.randint(1, self.model.num_products)] = random.randint(0,10)
            self.model.num_consumers += 1
            #assign consumer to two producers that she will purchase from
    
    def show_demand(self):
        print('Demand schedule for agent ', self.unique_id, self.demand)

    def order(self, buyer, quantity, cascade_id, input_id):
        #buyer, seller = self, get_agent_by_id(seller)
        self.output_orders.append((buyer,quantity, input_id))
        self.cascade_id = cascade_id
        self.model.cascades[cascade_id] += 1
        
    def fill_order(self, supplier, qty, input_id):
        if self.producer_level == 0:
            self.model.period_income += 1
            self.model.total_income += 1
        else:    
            
            for k in range(len(self.suppliers)):
                if self.suppliers[k].unique_id == supplier.unique_id:
                    #print('Found myself')
                    self.input_inventory[k] += qty
            #self.input_inventory[input_id] += qty
                                      
    def get_agent_by_id(self, agent_id):
        for a in self.model.scheduler.agents:
            if a.unique_id == agent_id: 
                return a
    
    def rewire(self,supplier_index):
        #choose a random new supplier
        new_suppliers = []
        for agent in self.model.schedule.agents:
            if agent.producer_level == self.producer_level + 1:
                new_suppliers.append(agent)
        
        self.suppliers[supplier_index] = random.choice(new_suppliers)
            
        #clear order history after rewiring
        self.order_history[supplier_index] = []
            
    def step(self):
        #consumption/production cycle
        #receive orders and produce
        
        #production function
        #initiate consumer orders randomly
        if self.producer_level == 0:
            supplier = random.choice(self.suppliers)
            this_supplier = self.suppliers.index(supplier)
            #for s in self.suppliers: 
            if self.unique_id in self.model.order_agents:
                if supplier.inventory == 0:
                    self.model.cascades[len(self.model.cascades)+1] = 0
                    supplier.order(self,1,len(self.model.cascades),self.suppliers.index(supplier))
                    self.order_history[this_supplier].append(0)
                else:
                    self.model.period_income += 1
                    self.model.total_income += 1
                    supplier.inventory -= 1
                    self.order_history[this_supplier].append(1)
                    
                #keep track of demand
                self.model.period_demand += 1
        #for producers
        elif self.producer_level < self.model.production_levels:
            #receive inventory and produce
            if self.input_inventory[0] > 0 and self.input_inventory[1] > 0:
                self.inventory += 2
                self.input_inventory[0] -= 1
                self.input_inventory[1] -= 1
                                    
            #fill orders
            if len(self.output_orders) > 0:
                order_agent, order_qty, input_id = self.output_orders[0]
                if self.inventory > 0:
                    order_agent.fill_order(self, order_qty, input_id)
                    self.inventory -= 1
                    self.output_orders.pop(0)
                    #self.order_history.append(1)
                else:
                    for s in self.suppliers:
                        s.order(self,1, self.cascade_id,self.suppliers.index(s))
                        
                        #eventually move this order history part, it's in the wrong place
                        this_supplier = self.suppliers.index(s)
                        self.order_history[this_supplier].append(0)
        else:
            #bottom-level agents produce raw materials
            for order_agent, order_qty, input_id in self.output_orders:
                order_agent.fill_order(self,1, input_id)
                self.output_orders.pop(0)
        
        #network rewiring - pick a new supplier if orders haven't been arriving
        for s in self.suppliers:
            this_supplier = self.suppliers.index(s)
            if len(self.order_history[this_supplier]) > 4 \
                  and (sum(self.order_history[this_supplier]) < .6 * len(self.order_history[this_supplier])) \
                      and self.producer_level == 0 \
                      and self.model.do_rewire:
                          self.rewire(this_supplier)

            