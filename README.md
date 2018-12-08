# Self-Organized Criticality Economic Model
An Agent-Based Model, using mesa for Python, which implements a self-organized criticality (SOC) mechanism

## Summary
This model implements a mechanism from the literature on Self-Organized Criticality (SOC), an idea which is frequently cited in the literature on complex systems. It implements a version of a Producer-Distributor-Consumer model which gives interesting and unpredictable behavior for aggregate income even when demand variation is low or zero. Also includes a mechanism which rewires the connections in the agent network based on connection profitability (ability to deliver orders on demand). It is intended as proof of concept, and a starting point for a more robust model which includes other, possibly critical, economic mechanisms, and a more fully developed machine learning component for agent behavior.

## How to Run

There are three ways to run the model: in a jupyter notebook for demo purposes, in interactive visualization mode, and from a run file (for collecting data, plotting, and more sytematic simulation study).

Launch an interactive server by Running ``run.py``:

```
    $ python run.py
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run. 

## Files

### ``SOCEconModel/model.py``
The **SOCEconModel** class is the model container. It is instantiated with the following parameters: num_agents is the total number of agents; p_orders specifies the total portion of consumer agents who will place an order in each period; p_consumers specifies ratio of consumers to producers in the network; production_levels is the network depth; do_rewire enables or disables network rewiring; and fix_demand specified whether demand is fixed or variable from period to period.

This defines the model. There is one agent class, **EconAgent**. Each EconAgent has two connections to other agents (its suppliers). Agents in the top level of the network are consumers, and other agents are producers. At each step of the model, there is demand for consumer products, which consumers attempt to purchase from suppliers in the next level down. If inventory is not available, it is ordered. When producers have inventory of all their inputs, they manufacture product to generate inventory to fill orders. Depending on the state of the network, it is possible for demand at the top of the network to initiate a cascade of orders down the network, potentially all the way to raw materials producers. The network is rewired dynamically based on a very simple order history tracking. 

### ``SOCEconModel/model_run.py``
This is where the model is run if visualization is not required. This code runs the model, tallies demand and income, and generates plots of the model behavior.

### ``SOCEconModel/server.py``

This file sets up the interactive visualization. The above listed parameters are implemented as sliders that the user can control. The visualization can be run continuously or the user can advance the model one step at a time. The plot shows the level of demand and the level of income in each period.

## Further Reading

See the SOCEconModelReport.pdf file for the project report about this model that I wrote for my class. It contains detailed discussion of the model development, experiments, ideas for future development, and references to relevant academic papers.

