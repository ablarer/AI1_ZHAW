#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:38:21 2017

@author: tugg
update: vissejul, bachmdo2, stdm (Nov 27, 2018)
"""
import pandas as pa
from pyDatalog import pyDatalog

# ---------------------------------------------------------------------------
# Social graph analysis:
# work through this code from top to bottom (in the way you would use a R or Jupyter notebook as well...) and write datalog clauses
# and python code in order to solve the respective tasks. Overall, there are 7 tasks.
# ---------------------------------------------------------------------------
calls = pa.read_csv('calls.csv', sep='\t', encoding='utf-8')
texts = pa.read_csv('texts.csv', sep='\t', encoding='utf-8')

suspect = 'Quandt Katarina'
company_Board = ['Soltau Kristine', 'Eder Eva', 'Michael Jill']

# Given in template
# pyDatalog.create_terms('knows','has_link','many_more_needed')

# Expanded for task
# Constants / Objects ( X ... P2)
# Predicates / Relations (knows ... can_reach),
# Function / Functions (all_path ... all_path_time)
# X, Y, Z: Caller, callee, indirect connection
# C, C2: Company board members, C2 is chosen to contribute in such a way to calculate the terms where C is contained.
# D, D2: Dates
# P, P2: Paths, , P2 is chosen to contribute in such a way to calculate the terms where P is contained.
pyDatalog.create_terms('X','Y','Z','C','C2','D','D2','P','P2','knows','has_link','contacted','can_reach','all_path','path_cost_short','all_path_time')

# Resets the default datalog database
pyDatalog.clear()

# First, treat calls as simple social links (denoted as knows), that have no date
# Expanded from the template given value 50 to 150
# We have 150 calls.
for i in range(0,150):
    +knows(calls.iloc[i,1], calls.iloc[i,2])


# Task 1: Knowing someone is a bi-directional relationship -> define the predicate accordingly

# See https://sites.google.com/site/pydatalog/Online-datalog-tutorial
# Calls / links are bidirectional (<=)
# A certain person X knows a certain person Y as a certain person Y knows a certain person X

knows(X,Y) <= knows(Y,X)

# Task 2: Define the predicate has_link in a way that it is true if a connection exists (path of people knowing the next link)
# Hints:
#   check if your predicate works: at least 1 of the following asserts should be true (2 if you read in all 150 communication records)
#   (be aware of the unusual behaviour that if an assert evaluates as true, an exception is thrown)

# See also
# https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py
# https://sites.google.com/site/pydatalog/home
has_link(X,Y) <= knows(X,Y)
has_link(X,Y) <= has_link(X,Z) & knows(Z,Y) & (X!=Y)

# Read in with 150 communications
# Throws no assertion error, it valuates as false
# Quandt Katarian does not know company board member Soltau Kristine
# assert (has_link('Quandt Katarina', company_Board[0]) == ())

# Throws assertion error, it valuates as true
# Quandt Katarian knows company board member number 2
# assert (has_link('Quandt Katarina', company_Board[1]) == ())

# Throws assertion error, it valuates as false
# Quandt Katarian does not know company board member number 3
# assert (has_link('Quandt Katarina', company_Board[2]) == ())

# --> Quandt Katarian knows Eder Eva and Michael Jill

# Task 3: You already know that a connection exists; now find the concrete paths between the board members and the suspect
# Hints:
#   if a knows b, there is a path between a and b
#   (X._not_in(P2)) is used to check whether x is not in path P2
#   (P==P2+[Z]) declares P as a new path containing P2 and Z

# See also
# https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py
# https://sites.google.com/site/pydatalog/home

all_path(X,Y,P) <= all_path(X,Z,P2) & knows(Z,Y) & (X!=Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P==P2+[Z])

all_path(X,Y,P) <= knows(X,Y) & (P==[])

"""
# Print might work but takes an extremely long time to calculate because of all the possible paths
# Iterate of list company_Board
for i in range(3):
    print(f'Has contacted: {company_Board[i]}.')
    print(all_path(company_Board[i], Y, P))
    print()
"""

# Task 4: There are too many paths. We are only interested in short paths.
# Find all the paths between the suspect and the company board that contain five people or less

# The idea of above suggestion might be, that the possibility of tipping off someone is more likely
# if the path is shorter.
# Same as above but plus "C", "C2" (company board members) plus "& (C==C2+1) & (C<5)" for the restriction
path_cost_short(X,Y,P,C) <= (path_cost_short(X,Z,P2,C2)) & knows(Z,Y) & (X!=Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P==P2+[Z]) & (C==C2+1) & (C<5)

# Same as above but plus "C" (company board member) plus "& (C==0)" for the restriction
path_cost_short(X,Y,P,C) <= knows(X,Y) & (P==[]) & (C==0)

"""
# Print might work but takes an extremely long time to calculate because of all the possible paths
# Iterate of list company_Board
for i in range(3):
    print(f'Has contacted: {company_Board[i]}.')
    print(path_cost_short(company_Board[i], Y, P, C))
    print()
"""

# ---------------------------------------------------------------------------
# Call-Data analysis:
# Now we use the text and the calls data together with their corresponding dates
# ---------------------------------------------------------------------------
date_board_decision = '12.2.2017'
date_shares_bought = '23.2.2017'
pyDatalog.create_terms('called,texted')
# Resets the default datalog database
pyDatalog.clear()

# # Expanded from the template given value 50 to 150
# Helps to figure out what the printed results further below may mean. With onyl 50 calls, the print out information
# where not so obvious.
# See also explanations further below.
for i in range(0,150): # calls
    +called(calls.iloc[i,1], calls.iloc[i,2],calls.iloc[i,3])

for i in range(0,150): # texts
    +texted(texts.iloc[i,1], texts.iloc[i,2],texts.iloc[i,3])

# calls are bi-directional
# If X called Y than Y called X and Z can reach X trough Y and Y through X
called(X,Y,Z) <= called(Y,X,Z)



# Task 5: Again we are interested in links, but this time a connection is only valid if the links are descending in date; 
#         find out who could have actually sent the information by adding this new restriction
# Hints:
#   You are allowed to naively compare the dates lexicographically using ">" and "<";
#   it works in this example (but is evil in general)

contacted(X,Y,Z) <= called(X,Y,Z)
contacted(X,Y,Z) <= texted(X,Y,Z)

# Iterate of list company_Board
for i in range(3):
    print(f'Has contacted: {company_Board[i]}.')
    print(contacted(company_Board[i], Y, Z))
    print()

 # --> No one contacted Soltau Kristine

can_reach(X,Y,D) <= can_reach(X,Z,D2) & contacted(Z,Y,D) & (X!=Y) & (D>=D2)
can_reach(X,Y,D) <= contacted(X,Y,D)

# Iterate of list company_Board
for i in range(3):
    print(f'Can reach: {company_Board[i]}.')
    print(can_reach(company_Board[i], Y, D))
    print()

 # --> No one reached Soltau Kristine

# Task 6: Find all the communication paths that lead to the suspect (with the restriction that the dates have to be ordered correctly)
# See also
# https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py
all_path_time(X,Y,P,D) <= all_path_time(X,Z,P2,D2) & contacted(Z,Y,D) & (X!=Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P==P2+[Z]) & (D>=D2)
all_path_time(X,Y,P,D) <= contacted(X,Y,D) & (P==[]) & (D>=date_board_decision)


# Final task: after seeing this information, who, if anybody, do you think gave a tip to the suspect?

# Iterate of list company_Board
print('--- Printout to deduct the results from. ---')
for i in range(3):
    print(f'Paths from: {company_Board[i]} to {suspect}.')
    print(f'Can reach {suspect} at date:')
    print(can_reach(company_Board[i], suspect, D))
    print(f'But only if there is a path as specified above leading from {company_Board[i]} to {suspect}:')
    print(all_path_time(company_Board[i],suspect,P, D))
    print()

# Result
# Going out from each the board members, there are only leading pathes to Quandt Katarina from Eder Eva
# at the dates: 16th, 21st, 23rd, two at 28th Feruary but not on the 24th February.
# The assertions above tell us this already further above but there, Michael Jill is additionally proposed.
# Thus, it might be rather possible that Eder Eva gave Quandt Katarina more or less directly a hint.

# General hint (only use on last resort!): 
#   if nothing else helped, have a look at https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py
