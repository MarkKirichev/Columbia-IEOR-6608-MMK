# Columbia-IEOR-6608-MMK
IEOR E6608 Integer Programming Final Course Project

This repository containts the files used to implement the Feasibility Pump, decribed in the following paper:
Fischetti, M., Glover, F. & Lodi, A. The feasibility pump. Math. Program. 104, 91–104 (2005). https://doi.org/10.1007/s10107-004-0570-3

The first implementation will be done in Python.
Future implementations will be done in C in order to help run the algorithm faster as it can require vast amounts of time due to the heuristic nature of the Pump. Thus, we'd like the calculations and algorithm to be performed faster in order for the Pump to pass through more possible feasible solutions in a shorter timespan. 

The first implementation deals with (0, 1)-LPs and future implementations would strive to encapsulate the solutions of a general MIP. Future steps include adding a regularization term that will restrict the projection step.
