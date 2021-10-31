# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 12:22:34 2020

@author: Cheng Rong
"""

import import_data
import numpy as np
import assignment
from assignment.assign import *
from assignment.line import *
from assignment.graph import *
import copy
import time
import csv
import set_exp_id as sid
import math

data = import_data.import_data()

# Step 4: Calculate the cost
def cal_new_cost(_label_station, _label_lane, _cost_station, _cost_lane, _lane, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand):
    fixed_cost = 0
    _new_cost = 0
#    once_FW_time = 0
    od_flow_bike = copy.deepcopy(od_flow)
#    print ("lane = ",_label_lane, " station=", _label_station)
    for i in range(len(demand)):
        if _label_station[i] != 0:
            fixed_cost += _cost_station[i]
    for i in _lane:
        if _label_lane[i] != 0:
            fixed_cost += _cost_lane[i]
    if fixed_cost > Budget:
        _new_cost =1000000000000000+fixed_cost
    else:
       # time_cost
        time_cost = 0
        No_edge = len(_cost_lane)
        nt_a = data.read_network_auto(nt_a, _label_lane, No_edge)
        nt_b = data.read_network_bike(nt_b, _label_lane, No_edge)
#        star_FW = time.time()
#        print("lane=",_label_lane,"station=",_label_station)
        vol_a, vol_b, time_cost, od_flow_bike = assignment.assign.FW_main(
            nt_a, nt_b, od_info, od_flow, _label_lane, _label_station, UE_converge, sita, fy, demand)
#        print("od_flow_bike=",od_flow_bike)
#        end_FW = time.time()
#        once_FW_time = end_FW-star_FW
#        print("fw time=", end_FW-star_FW)
#        if isOutPutDetail:
#        print("*****motor vehicles*****")
#        for link in vol_a.keys():
#            print("{0},{1}".format(link,vol_a[link]))
#        print("*****bikes*****")
#        for link in vol_b.keys():
#            print("{0},{1}".format(link,vol_b[link]))

        _new_cost = time_cost+fixed_cost
    return _new_cost, fixed_cost,od_flow_bike


# Step 1: Low level heuristics
# LLH0:Select an unselected link and add it to the bicycle link set.
def cal_L0_add_bike_link(_label_lane, _lane):
 # d,e for temporary data storage,meaningless
    d = []
    e = 0
    for i in _lane:
        if _label_lane[i] == 0:
            d.append(i)
    if len(d) != 0:
        e = np.random.choice(d)
        _label_lane[e] = 1
#    print("lane=",_label_lane)
    return _label_lane

# LLH1:Select a link in the bicycle link set and move it out of the bicycle link set.


def cal_L1_remove_bike_link(_label_lane, _lane):
    d = []
    e = 0
    for i in _lane:
        if _label_lane[i] == 1:
            d.append(i)
    if len(d) != 0:
        e = np.random.choice(d)
        _label_lane[e] = 0
#    print("lane=",_label_lane)
    return _label_lane

# LLH2:
# roulette selection based on OD demand
# def cal_L2_add_bike_station(_label_station,_station,_time_station,_demand,_od_info):
#    a = True  #assume a selected node is not allacated to a bike station
#    while a == True:
#        b = random.uniform(0,1)
#        for i in range(len(_od_info)):
#            if _od_info[i][3]<b:
#                continue
#            else:
#                _od_ID = i
#                break
#        o = _od_info[_od_ID][0]
#        d = _od_info[_od_ID][1]
#        _is_add = 0
#        for k in range(len(_demand)):
#            if o in ["N{:0>3}".format(_demand[k])]:
#                if _label_station[k] == 0:
#                    _label_station[k] = random.choice(_time_station[o].keys())
#                    _is_add += 1
#            if d in ["N{:0>3}".format(_demand[k])]:
#                if _label_station[k] == 0:
#                    _label_station[k] = random.choice(_time_station[d].keys())
#                    _is_add += 1
#        if _is_add >0:
#            a = False
#    return _label_station


def cal_L2_add_bike_station(_label_station, _demand, _od_flow):
    d = []
    e = 0
    for j in range(len(_demand)):
        if _label_station[j] == 0:
            d.append(j)
    if len(d) != 0:
        e = np.random.choice(d)
        _label_station[e] = 1

#    print("station=",_label_station)
    return _label_station



def cal_L6_add_bike_staion_unserved_od(_label_station, _demand, _od_flow):
    d = []
    e = 0
    for j in range(len(_demand)):
        if _label_station[j] == 0:
            d.append(j)
    if len(d) != 0:
        e = np.random.choice(range(len(_demand)))
        if _label_station[e] == 0:
            _label_station[e] = 1        
        for i in d:
            if ["N{:0>3}".format(_demand[e])] in list(_od_flow.keys()):
                if ["N{:0>3}".format(_demand[i])] in list(_od_flow["N{:0>3}".format(_demand[e])].keys()):
#                    g = []
#                    g = list(
#                        _time_station["N{:0>3}".format(_demand[i])].keys())
                    _label_station[i] = 1
            elif ["N{:0>3}".format(_demand[i])] in list(_od_flow.keys()):
                if ["N{:0>3}".format(_demand[e])] in list(_od_flow["N{:0>3}".format(_demand[i])].keys()):
#                    h = []
#                    h = list(
#                        _time_station["N{:0>3}".format(_demand[i])].keys())
                    _label_station[i] = 1

#    d=[]
#    for i in _demand:
# if _match_station[i][e]==1:
#        if e in _time_station["N{:0>3}".format(i)].keys():
#             d.append(i)
#    if len(d)!=0:
#        f=random.choice(d)
#        _label_station[e]=f
#    print("station=",_label_station)
    return _label_station

# LLH3:

def cal_L3_remove_bike_station(_label_station,  _demand):
    a = []
    b = 0
    for i in range(len(_demand)):
        if _label_station[i] != 0:
            a.append(i)
    if len(a) != 0:
        b = np.random.choice(a)
        _label_station[b] = 0
#    print("station=",_label_station)
    return _label_station


# LLH4:

def cal_L4_exchange_two_bike_station_status(_label_station, _demand):
    a =  np.random.randint(0, len(_demand))
    b =  np.random.randint(0, len(_demand))
    while a-b == 0:
        b =  np.random.randint(0, len(_demand))
    m = _label_station[a]
    n = _label_station[b]    
    _label_station[a]=n
    _label_station[b]=m
# replace
#    a = []
#    b = 0
#    c = 0
#    for i in range(len(_demand)):
#        if _label_station[i] != 0:
#            a.append(i)
#    if len(a) != 0:
#        check_a = np.array(np.zeros((len(a))), dtype=int)
#        has_opt = False
#        while has_opt == False:
#            d = []
#            for j in range(len(check_a)):
#                if check_a[j] == 0:
#                    d.append(j)
#            if len(d) != 0:
#                b = np.random.choice(d)
#                check_a[b] = 1
###                if ["N{:0>3}".format(_demand[a[b]])] in list(_time_station.keys()):
##                    if len(_time_station["N{:0>3}".format(_demand[a[b]])].keys()) != 1:
##                        c = np.random.choice(
##                            list(_time_station["N{:0>3}".format(_demand[a[b]])].keys()))
#                        _label_station[b] = c
#                        has_opt = True
#            else:
#                break
#    print("ex_station",a,b)
#    print("station=",_label_station)
    return _label_station

def cal_L5_exchange_two_bike_lanes_status(_label_lane):
    a =  np.random.randint(0, len(_label_lane))
    b =  np.random.randint(0, len(_label_lane))
    while a-b == 0:
        b =  np.random.randint(0, len(_label_lane))
    m = _label_lane[a]
    n = _label_lane[b]
    _label_lane[a]= n
    _label_lane[b] = m
#    print("ex_lane",a,b)
#    print("lane=",_label_lane)
    return _label_lane




def cal_L7_add_neighbor_lane(_label_lane,_demand,_net_bike):
    z = []
    for i in range(len(_label_lane)):
        if _label_lane[i] != 0:
            z.append(i)
    if len(z) != 0:
        a0 = np.random.choice(z)
        a = a0 + 1        # lane_id
#        print("selected lane id = ", a)
        b = []
        lane_pointer = _net_bike["E{:0>3}".format(a)]['o']
        lane_pointee = _net_bike["E{:0>3}".format(a)]['d']
        for k in range(len(_net_bike)):
            if _net_bike["E{:0>3}".format(k+1)]['o'] in lane_pointer or _net_bike[
                    "E{:0>3}".format(k+1)]['o'] in lane_pointee or _net_bike[
                            "E{:0>3}".format(k+1)]['d'] in lane_pointer or _net_bike[
                                    "E{:0>3}".format(k+1)]['d'] in lane_pointee:
                b.append(k)

    
    
#    for i in range(len(_demand)):
#        for j in range(len(_demand)):
#            if ("N{:0>3}".format(_demand[i]),"N{:0>3}".format(_demand[j])) in _net_b.edgenode.keys():
#                if _net_b.edgenode[("N{:0>3}".format(_demand[i]),"N{:0>3}".format(_demand[j]))] in ["E{:0>3}".format(a)]:
#                    for k in range(len(_label_lane)):
#                        if k != a0:
#                            if _net_b.edgeset["E{:0>3}".format(k+1)].pointer == ["N{:0>3}".format(_demand[i])] or _net_b.edgeset["E{:0>3}".format(k+1)].pointee == ["N{:0>3}".format(_demand[i])] or _net_b.edgeset["E{:0>3}".format(k+1)].pointer == ["N{:0>3}".format(_demand[j])] or _net_b.edgeset["E{:0>3}".format(k+1)].pointee == ["N{:0>3}".format(_demand[j])]:
#                                b.append(k)
#            else:
#                continue                        
                
        if len(b) != 0:
#            print("neibor lane index = ", b)
            y = []
            for i in b:
                if _label_lane[i] == 0:
                    y.append(i)
#            print ("neighbor lane..0...index",y)
            if len(y) != 0 :
                c = np.random.choice(y)
                _label_lane[c] = 1
#            print ("selected neighbor lane index = ",c)
#    print("lane=",_label_lane)
    return _label_lane
                        
                
                
                






'''
def cal_L4_replace_bike_station(_label_station,_station,_time_station,_demand): 
 # d,g,e,f,h are used for temporary data storage,meaningless
    d=[]  
    g=[]
    e=0
    f=0
    h=0
    for i in _station:
        if _label_station[i]!=0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d) 
        f=_label_station[e]
        for i in _station:
#            if _match_station[f][i]==1 and _label_station[i]==0:
            if i in _time_station["N{:0>3}".format(f)].keys() and _label_station[i]==0:
                g.append
        if len(g)!=0:
            h=random.choice(g) 
            _label_station[h]=_label_station[e]
            _label_station[e]=0
    return _label_station
'''
'''
#LLH5:Select two random sets and a random node in each set. The node in the first set is inserted into the second set.
def cal_L5_insert_bike_station(_label_station,_station,_time_station,_demand): 
    d=[]  
    e=0
    f=0
    g=0
    for i in _station:
        if _label_station[i]!=0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d) 
        f=_label_station[e]
        d=[]
        for i in _station:
#            if _label_station[i]!=0 and _label_station[i]!=f and _match_station[f][i]==1:
            if _label_station[i]!=0 and _label_station[i]!=f and i in _time_station["N{:0>3}".format(f)].keys():
                d.append(i)   
        if len(d)!=0:
            g=random.choice(d) 
            _label_station[e]=_label_station[g]
    return _label_station

#LLH6:Select two random sets and a random node in each set and swap the nodes.
def cal_L6_swap_bike_station(_label_station,_station,_time_station,_demand): 
    d=[]  
    e=0
    f=0
    g=0
    for i in _station:
        if _label_station[i]!=0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d) 
        f=_label_station[e]
        d=[]
        for i in _station:
#            if _label_station[i]!=0 and _label_station[i]!=f and _match_station[f][i]==1 and _match_station[_label_station[i]][e]==1:
            if _label_station[i]!=0 and _label_station[i]!=f and i in _time_station["N{:0>3}".format(f)].keys() and i in _time_station["N{:0>3}".format(e)].keys()==1:

                d.append(i)   
        if len(d)!=0:
            g=random.choice(d) 
            _label_station[e]=_label_station[g]
            _label_station[g]=f
    return _label_station
'''

# Step2:Hueristics Sequence Selection


def cal_HSS(LLH, SEQ, cumulative_pro_TM, TM, pro_TM, CHOICE, SM, pro_SM, cumulative_pro_SM):
    """
    a random low level heuristic is selected and add to the sequence
    """
    cur = np.random.randint(0, len(LLH)-1)
    SEQ.append(LLH[cur])

    # LLH(next) is chosen by a selection procedure based on the roulette wheel selection strategy
    """
    start of the roulette wheel
    """
    
    a = 0
    b = 0
    c = np.random.uniform(0, 1)
    for i in LLH:
        for j in LLH:
            cumulative_pro_TM[i][j] = 0
    for j in LLH:
        a += TM[LLH[cur]][j]

    for j in LLH:
        pro_TM[LLH[cur]][j] = TM[LLH[cur]][j]/a
        cumulative_pro_TM[LLH[cur]][j] = b+pro_TM[LLH[cur]][j]
        b = cumulative_pro_TM[LLH[cur]][j]

    for j in LLH:
        if cumulative_pro_TM[LLH[cur]][j] < c:
            continue
        else:
            SEQ.append(j)
            cur = j
            break
    """
    end of the roulette wheel
    """
    # judge whether the sequence will terminate at this point
    a = 0
    c = np.random.uniform(0, 1)
    for j in CHOICE:
        a += SM[cur][j]
    for j in CHOICE:
        pro_SM[cur][j] = SM[cur][j]/a
    cumulative_pro_SM[cur][CHOICE[0]] = pro_SM[cur][CHOICE[0]]
    cumulative_pro_SM[cur][CHOICE[1]] = 1
    while cumulative_pro_SM[cur][CHOICE[0]] < c:
        a = 0
        b = 0
        c = np.random.uniform(0, 1)
        for i in LLH:
            for j in LLH:
                cumulative_pro_TM[i][j] = 0
        for j in LLH:
            a += TM[cur][j]
        for j in LLH:
            pro_TM[cur][j] = TM[cur][j]/a
            cumulative_pro_TM[cur][j] = b+pro_TM[cur][j]
            b = cumulative_pro_TM[cur][j]
        for j in LLH:
            if cumulative_pro_TM[cur][j] < c:
                continue
            else:
                SEQ.append(j)
                cur = j
                break
        a = 0
        c = np.random.uniform(0, 1)
        for j in CHOICE:
            a += SM[cur][j]
        for j in CHOICE:
            pro_SM[cur][j] = SM[cur][j]/a
        cumulative_pro_SM[cur][CHOICE[0]] = pro_SM[cur][CHOICE[0]]
        cumulative_pro_SM[cur][CHOICE[1]] = 1
    return SEQ

 # step 3:apply SEQ


def cal_apply(_uSEQ, _ulabel_lane, _ulane, _ulabel_station, _udemand, _uod_flow,_net_b,_net_bike):
    for i in _uSEQ:
        if i in ["L0"]:
            _ulabel_lane = cal_L0_add_bike_link(_ulabel_lane, _ulane)
            continue
        if i in ["L1"]:
            _ulabel_lane = cal_L1_remove_bike_link(_ulabel_lane, _ulane)
            continue
        if i in ["L2"]:
            _ulabel_station = cal_L2_add_bike_station(_ulabel_station, _udemand, _uod_flow)
            continue
        if i in ["L3"]:
            _ulabel_station = cal_L3_remove_bike_station(_ulabel_station, _udemand)
            continue
        if i in ["L4"]:
            _ulabel_station = cal_L4_exchange_two_bike_station_status(_ulabel_station, _udemand)
            continue
        if i in ["L5"]: 
            _ulabel_lane = cal_L5_exchange_two_bike_lanes_status(_ulabel_lane)
            continue
        if i in ["L6"]:
            _ulabel_station = cal_L6_add_bike_staion_unserved_od(_ulabel_station, _udemand, _uod_flow)
            continue
        if i in ["L7"]:
            _ulabel_lane = cal_L7_add_neighbor_lane(_ulabel_lane,_udemand,_net_bike)
            continue
    return _ulabel_lane, _ulabel_station



    


# for run in range(Run_time):
#    print("run",run)
def run_upper(Ex_ID):
    case_ID, demand_ID, Budget, fy, sita, UE_converge, Max_gen, Pop_size = sid.set_Ex_ID(
        Ex_ID, _alg="HH")
    # .....................input       od_demand,    network
    #    data=import_data.import_data()
    # od_info list, od_demand  dict
    od_info, od_flow = data.read_od(case_ID, demand_ID)

    lane, cost_lane, cost_station, demand = data.set_sta_lane(
        case_ID)
    nt_a, nt_b,net_bike = data.set_network(case_ID)

    # ....................Initialization

    LLH = ['L0','L1','L2','L3','L4','L5','L6','L7']

    pro_TM, pro_SM = data.set_prob()
    cumulative_pro_TM, cumulative_pro_SM = data.set_prob()
    TM, SM = data.set_prob()

    CHOICE = ['CONTINUE','STOP']
    
    
    
    
    
#    # set Initial Temperature
#    acc1 = 0
#    acc2=0
#    delt=0
#    alpha = 0.9999
##    init_lane = np.array(np.zeros((len(lane))), dtype=np.int)
##    init_station = np.array(np.zeros((len(demand))), dtype=np.int)
##    init_cost = 1000000000
#    for i in range(50):
#        t_lane = np.array(np.zeros((len(lane))), dtype=np.int)
#        t_station = np.array(np.zeros((len(demand))), dtype=np.int)
#        
#        t_lane[0:len(lane)]= np.random.randint(0, 2, len(lane))
#        t_station[0:len(demand)]= np.random.randint(0, 2, len(demand))
#        
#        a0,a1,a2 = cal_new_cost(t_station,t_lane,cost_station, cost_lane, lane, 
#                Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand) 
##        if a0<init_cost:
##            init_cost = a0
##            init_lane = copy.deepcopy(t_lane)
##            init_station = copy.deepcopy(t_station)
#        SEQ = []
#        SEQ = cal_HSS(LLH, SEQ, cumulative_pro_TM, TM, pro_TM,
#                      CHOICE, SM, pro_SM, cumulative_pro_SM)
#        for y in range(len(SEQ)):
#            if SEQ[y] == 'L0':
#                continue
#            if SEQ[y] == 'L1':
#                continue
#            if SEQ[y] == 'L2':
#                continue
#            if SEQ[y] == 'L3':
#                continue
#            if SEQ[y] == 'L4':
#                continue
#            if SEQ[y] == 'L5':
#                continue
#            if SEQ[y] == 'L6':
#                continue
#            if SEQ[y] == 'L7':
#                continue
#
#        tlabel_lane, tlabel_station = cal_apply(SEQ, t_lane, lane,t_station,
#                                              demand,od_flow,nt_b,net_bike)
#        new_c, a3, a4 = cal_new_cost(
#            tlabel_station, tlabel_lane, cost_station, cost_lane, lane, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)                
##        if new_c<init_cost:
##            init_cost = new_c
##            init_lane = tlabel_lane
##            init_station = tlabel_station
#        
#        
#        if new_c<a0:
#            acc1 = acc1+1
#        else:
#            acc2 = acc2+1
#            if new_c>a0:
#                delt = delt+1
#    delt = delt/50
#    T = int(delt/(math.log(acc2 / (acc2*alpha - acc1*(1-alpha)))))
#    print("Ini Temper  ",T)
#
    T = 3000
    alpha = 0.999
    batch = 10
#    val = 1
#    TM1 = {}
#    SM1 = {}
#    pro_TM1 = {}
#    pro_SM1 = {}
#    cumulative_pro_TM1={}
#    cumulative_pro_SM1={}
#    key1 = {}
#    key2 = {}
#    key2[CHOICE[0]] =int(val)
#    key2[CHOICE[1]] = int(val)
#    for i in LLH:
#
#        key1[i] = int(val)
#        TM1[i]=key1
#        pro_TM1[i]=key1
#        cumulative_pro_TM1[i]=key1   
#        
#        SM1[i]=key2
#        pro_SM1[i]=key2
#        cumulative_pro_SM1[i]=key2
#        SM1[i]=key2
#        pro_SM1[i]=key2
#        cumulative_pro_SM1[i]=key2
##    print(TM,SM,pro_TM,pro_SM,cumulative_pro_TM,cumulative_pro_SM)
#    TM = copy.deepcopy(TM1)
#    pro_TM = copy.deepcopy(pro_TM1)
#    cumulative_pro_TM = copy.deepcopy(cumulative_pro_TM1)
#    SM = copy.deepcopy(SM1)
#    pro_SM = copy.deepcopy(pro_SM1)
#    cumulative_pro_SM = copy.deepcopy(cumulative_pro_SM1)
    
    
    
    
    start_time = time.time()
    
# Initial Group..................................................
#    Initial_solution = np.array(np.zeros((Pop_size,len(lane)+len(demand)+1)),dtype=np.int64)
#    no_sol = 0
#    while no_sol < Pop_size:
#        Initial_solution[no_sol,len(lane):len(lane)+len(demand)] = np.random.randint(0, 2, len(demand))
#        a0,a1,a2,a3 = cal_new_cost(Initial_solution[no_sol,len(lane):len(lane)+len(demand)],
#                Initial_solution[no_sol,0:len(lane)],cost_station, cost_lane, lane, 
#                Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)   
#        if a1 <= Budget:
#            Initial_solution[no_sol,len(lane)+len(demand)] = a0
#            no_sol = no_sol + 1
#    Initial_solution = Initial_solution[np.argsort(
#        Initial_solution[:, np.size(Initial_solution, 1)-1])]
# 
#    best_lane = np.array(np.zeros((len(lane))), dtype=np.int)
##    for i in range(len(lane)):
##        best_lane[i] = Initial_solution[0,i]
#    best_station = np.array(np.zeros((len(demand))), dtype=np.int)
#    for i in range(len(demand)):
#        best_station[i] = Initial_solution[0,len(lane)+i]
#    print("Ini_station",best_station)
#    print("Ini_cost",Initial_solution[0,len(lane)+len(demand)])
#    
#
#    cur_lane = copy.deepcopy(best_lane)
#    cur_station = copy.deepcopy(best_station)
#    label_lane = copy.deepcopy(best_lane)
#    label_station = copy.deepcopy(best_station)
#    best_cost =  Initial_solution[0,len(lane)+len(demand)]
#    cur_cost = Initial_solution[0,len(lane)+len(demand)]
#.............................................................................
# fixed solution .......................................
    best_lane = np.array(np.zeros((len(lane))), dtype=np.int)
#
    best_station = np.array(np.zeros((len(demand))), dtype=np.int)
    
    
#    best_lane[0:len(lane)]= copy.deepcopy(init_lane)
#    best_station[0:len(demand)]= copy.deepcopy(init_station)
#    best_lane[0:len(lane)]= np.random.randint(0, 2, len(lane))
#    best_station[0:len(demand)]= np.random.randint(0, 2, len(demand))
    
    
    
    
#    SA前
    if Ex_ID in [3,6,9]:
        for i in range(len(demand)):
     #        best_station[i] = Initial_solution[0,len(lane)+i]
            best_station[i] = 1

    a0,a1,a2 = cal_new_cost(best_station,best_lane,cost_station, cost_lane, lane, 
                Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)   
    
    cur_lane = copy.deepcopy(best_lane)
    cur_station = copy.deepcopy(best_station)
    label_lane = copy.deepcopy(best_lane)
    label_station = copy.deepcopy(best_station)
    best_cost =  a0
    cur_cost = a0
    print("Ini_cost",best_cost,".....",cur_cost)
#...............................................................................

    result = []

    No_0 = 0
    No_1 = 0
    No_2 = 0
    No_3 = 0
    No_4 = 0
    No_5 = 0
    No_6 = 0
    No_7 = 0
    

#    FW_time = 0

    # Step 5: test upper
    n = 0

    # sol_cost = np.array(np.zeros((Max_gen+1, 1)))
 #  time stop
    sol_cost = []
    acc_time = []
    acc_time.append(0)
#  .............................................1.01+0.02
    Rate = 1.01
    Rate0 = 1.01
    rate_add = 0.02

#    Rate = 1.01
#    Rate0 = 1.01
#    rate_add = 0.001
#    Rate = 1.05
#    Rate0 = 1.05
#    rate_add = 0.01

#..................1+0.02          only+ta
#    Rate = 1
#    Rate0 = 1
#    rate_add = 0.02 

    reward = 1    
    
    best_iter = 0
#
    # if Ex_ID in [7,8,9]:
    #     batch = 10
    # else:
    #     batch = 100
    
    
    cur_time = 0
    total_generation = 0

    
    # while n < 1:  
    while cur_time-start_time<=300:
        cur_time = time.time()
        total_generation = total_generation +1
#        print("HH Generation = ",n)
        n += 1
        SEQ = []
        SEQ = cal_HSS(LLH, SEQ, cumulative_pro_TM, TM, pro_TM,
                      CHOICE, SM, pro_SM, cumulative_pro_SM)
        for y in range(len(SEQ)):
            if SEQ[y] == 'L0':
                No_0 += 1
                continue
            if SEQ[y] == 'L1':
                No_1 += 1
                continue
            if SEQ[y] == 'L2':
                No_2 += 1
                continue
            if SEQ[y] == 'L3':
                No_3 += 1
                continue
            if SEQ[y] == 'L4':
                No_4 += 1
                continue
            if SEQ[y] == 'L5':
                No_5 += 1
                continue
            if SEQ[y] == 'L6':
                No_6 += 1
                continue
            if SEQ[y] == 'L7':
                No_7 += 1
                continue

        label_lane, label_station = cal_apply(SEQ, label_lane, lane,label_station,
                                              demand,od_flow,nt_b,net_bike)
        new_cost, newfixcost, od_bike = cal_new_cost(
            label_station, label_lane, cost_station, cost_lane, lane, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)        
        
#        FW_time = FW_time + o_FW_time
        # sol_cost[n, 0] = copy.deepcopy(new_cost)
        sol_cost.append(new_cost)
# only improve   300s  tested     
#        if new_cost < cur_cost:
#            cur_cost = new_cost
#            cur_lane = copy.deepcopy(label_lane)
#            cur_station = copy.deepcopy(label_station)
#          # Update TM and SM
#          #  for i in range(len(SEQ)-1):
#          #     TM[SEQ[i]][SEQ[i+1]] += reward
#          #  for i in range(len(SEQ)-1):
#          #      SM[SEQ[i]][CHOICE[0]] += reward
#          #  SM[SEQ[len(SEQ)-1]][CHOICE[1]] += reward
#
#            # Update best_cost,best_label_lane,best_label_station
#            if cur_cost < best_cost:
#                best_cost = cur_cost
#                print("up_cost=",best_cost)
#                best_lane = copy.deepcopy(cur_lane)
#                best_station = copy.deepcopy(cur_station)
#                best_iter = n
#                print("best_iter",best_iter)
#                acc_time.append(best_iter)
##              Update TM and SM
#                for i in range(len(SEQ)-1):
#                    TM[SEQ[i]][SEQ[i+1]] += reward
#                for i in range(len(SEQ)-1):
#                    SM[SEQ[i]][CHOICE[0]] += reward
#                SM[SEQ[len(SEQ)-1]][CHOICE[1]] += reward
#
#        else:
#            new_cost = cur_cost
#            label_lane = copy.deepcopy(cur_lane)
#            label_station = copy.deepcopy(cur_station)


# 300s TA 1.01
        if new_cost<cur_cost*Rate:
            cur_lane=copy.deepcopy(label_lane)
            cur_station=copy.deepcopy(label_station)
            
            if new_cost < cur_cost:
                cur_cost=new_cost
      # Update best_cost,best_label_lane,best_label_station
                if cur_cost<best_cost:
                    best_cost=cur_cost
                    print("up_cost=",best_cost)
                    best_lane=copy.deepcopy(cur_lane)
                    best_station=copy.deepcopy(cur_station)
                    best_iter=n
                    print("best_iter",best_iter)
                    acc_time.append(best_iter)
                    Rate = 1.01

                    for i in range(len(SEQ)-1):
                        TM[SEQ[i]][SEQ[i+1]] +=  reward
                    for i in range(len(SEQ)-1):
                        SM[SEQ[i]][CHOICE[0]]+= reward
                    SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= reward
        else:
            new_cost=cur_cost
            label_lane=copy.deepcopy(cur_lane)
            label_station=copy.deepcopy(cur_station)

                
# 300s OI + 50 gen 0.02
#        ！！！！修改rate=1, rate0
#        if new_cost<cur_cost*Rate:
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#            
#            if new_cost < cur_cost:
#                cur_cost=new_cost
#      # Update best_cost,best_label_lane,best_label_station
#                if cur_cost<best_cost:
#                    best_cost=cur_cost
#                    print("up_cost=",best_cost)
#                    best_lane=copy.deepcopy(cur_lane)
#                    best_station=copy.deepcopy(cur_station)
#                    best_iter=n
#                    print("best_iter",best_iter)
#                    acc_time.append(best_iter)
#                    Rate = 1.01
#
#                    for i in range(len(SEQ)-1):
#                        TM[SEQ[i]][SEQ[i+1]] +=  reward
#                    for i in range(len(SEQ)-1):
#                        SM[SEQ[i]][CHOICE[0]]+= reward
#                    SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= reward
#        else:
#            new_cost=cur_cost
#            label_lane=copy.deepcopy(cur_lane)
#            label_station=copy.deepcopy(cur_station)
#            if n-acc_time[len(acc_time)-1] >= 50:
#                Rate = Rate0+rate_add


# 300s TA + 50 gen 0.02
#        ！！！！修改rate = 1.01
#        if new_cost<cur_cost*Rate:
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#            
#            if new_cost < cur_cost:
#                cur_cost=new_cost
#      # Update best_cost,best_label_lane,best_label_station
#                if cur_cost<best_cost:
#                    best_cost=cur_cost
#                    print("up_cost=",best_cost)
#                    best_lane=copy.deepcopy(cur_lane)
#                    best_station=copy.deepcopy(cur_station)
#                    best_iter=n
#                    print("best_iter",best_iter)
#                    acc_time.append(best_iter)
#                    Rate = 1.01
#
#                    for i in range(len(SEQ)-1):
#                        TM[SEQ[i]][SEQ[i+1]] +=  reward
#                    for i in range(len(SEQ)-1):
#                        SM[SEQ[i]][CHOICE[0]]+= reward
#                    SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= reward
#        else:
#            new_cost=cur_cost
#            label_lane=copy.deepcopy(cur_lane)
#            label_station=copy.deepcopy(cur_station)
#            if n-acc_time[len(acc_time)-1] >= 50:
#                Rate = Rate0+rate_add


## 300s SA
##   检查 T, Alpha    
#        if new_cost<cur_cost:
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#            cur_cost=new_cost
#      # Update best_cost,best_label_lane,best_label_station
#            if cur_cost<best_cost:
#                best_cost=cur_cost
#                print("up_cost=",best_cost)
#                best_lane=copy.deepcopy(cur_lane)
#                best_station=copy.deepcopy(cur_station)
#                best_iter=n
#                print("best_iter",best_iter)
#                acc_time.append(best_iter)
#
#                for i in range(len(SEQ)-1):
#                    TM[SEQ[i]][SEQ[i+1]] +=  1
#                for i in range(len(SEQ)-1):
#                    SM[SEQ[i]][CHOICE[0]]+= 1
#                SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 1
##            else:
##                for i in range(len(SEQ)-1):
##                    TM[SEQ[i]][SEQ[i+1]] +=  5
##                for i in range(len(SEQ)-1):
##                    SM[SEQ[i]][CHOICE[0]]+= 5
##                SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 5
#            
#        elif np.random.uniform(0, 1) < np.exp(-(new_cost-cur_cost)/T):
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#            cur_cost=new_cost
##            for i in range(len(SEQ)-1):
##                TM[SEQ[i]][SEQ[i+1]] +=  1
##            for i in range(len(SEQ)-1):
##                SM[SEQ[i]][CHOICE[0]]+= 1
##            SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 1
#            
#        else:
#            new_cost=cur_cost
#            label_lane=copy.deepcopy(cur_lane)
#            label_station=copy.deepcopy(cur_station)
#        
#        
#        if (n%batch == 0):
#            T = alpha * T


## 300s OI + SA
#        if new_cost < cur_cost:
#            cur_cost = new_cost
#            cur_lane = copy.deepcopy(label_lane)
#            cur_station = copy.deepcopy(label_station)
#
#            # Update best_cost,best_label_lane,best_label_station
#            if cur_cost < best_cost:
#                best_cost = cur_cost
#                print("up_cost=",best_cost)
#                best_lane = copy.deepcopy(cur_lane)
#                best_station = copy.deepcopy(cur_station)
#                best_iter = n
#                print("best_iter",best_iter)
#                acc_time.append(best_iter)
##              Update TM and SM
#                for i in range(len(SEQ)-1):
#                    TM[SEQ[i]][SEQ[i+1]] += reward
#                for i in range(len(SEQ)-1):
#                    SM[SEQ[i]][CHOICE[0]] += reward
#                SM[SEQ[len(SEQ)-1]][CHOICE[1]] += reward
##                TT = T
#
#        else:
#            if n-acc_time[len(acc_time)-1] >= 50:
#                if np.random.uniform(0, 1) < np.exp(-(new_cost-cur_cost)/T):
#                    cur_lane=copy.deepcopy(label_lane)
#                    cur_station=copy.deepcopy(label_station)
#                    cur_cost=new_cost
#                    
#                else:
#                    new_cost=cur_cost
#                    label_lane=copy.deepcopy(cur_lane)
#                    label_station=copy.deepcopy(cur_station)
#                
#                
#                if ((n-acc_time[len(acc_time)-1])%batch == 0):
#                    T = alpha * T               
#            
#            else:
#                 new_cost=cur_cost
#                 label_lane=copy.deepcopy(cur_lane)
#                 label_station=copy.deepcopy(cur_station)

































# ##     ..................   OI + SA .................
#         if n >0.5*Max_gen:
#             if new_cost<cur_cost:
#                 cur_lane=copy.deepcopy(label_lane)
#                 cur_station=copy.deepcopy(label_station)
#                 cur_cost=new_cost
#           # Update best_cost,best_label_lane,best_label_station
#                 if cur_cost<best_cost:
#                     best_cost=cur_cost
#                     print("up_cost=",best_cost)
#                     best_lane=copy.deepcopy(cur_lane)
#                     best_station=copy.deepcopy(cur_station)
#                     best_iter=n
#                     print("best_iter",best_iter)
#                     acc_time.append(best_iter)
        
#                     for i in range(len(SEQ)-1):
#                         TM[SEQ[i]][SEQ[i+1]] +=  1
#                     for i in range(len(SEQ)-1):
#                         SM[SEQ[i]][CHOICE[0]]+= 1
#                     SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 1
#             else:
#                 new_cost=cur_cost
#                 label_lane=copy.deepcopy(cur_lane)
#                 label_station=copy.deepcopy(cur_station)                
#         else:
#             if new_cost<cur_cost:
#                 cur_lane=copy.deepcopy(label_lane)
#                 cur_station=copy.deepcopy(label_station)
#                 cur_cost=new_cost
#           # Update best_cost,best_label_lane,best_label_station
#                 if cur_cost<best_cost:
#                     best_cost=cur_cost
#                     print("up_cost=",best_cost)
#                     best_lane=copy.deepcopy(cur_lane)
#                     best_station=copy.deepcopy(cur_station)
#                     best_iter=n
#                     print("best_iter",best_iter)
#                     acc_time.append(best_iter)
    
#                     for i in range(len(SEQ)-1):
#                         TM[SEQ[i]][SEQ[i+1]] +=  1
#                     for i in range(len(SEQ)-1):
#                         SM[SEQ[i]][CHOICE[0]]+= 1
#                     SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 1
#     #            else:
#     #                for i in range(len(SEQ)-1):
#     #                    TM[SEQ[i]][SEQ[i+1]] +=  5
#     #                for i in range(len(SEQ)-1):
#     #                    SM[SEQ[i]][CHOICE[0]]+= 5
#     #                SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 5
                
#             elif np.random.uniform(0, 1) < np.exp(-(new_cost-cur_cost)/T):
#                 cur_lane=copy.deepcopy(label_lane)
#                 cur_station=copy.deepcopy(label_station)
#                 cur_cost=new_cost
#     #            for i in range(len(SEQ)-1):
#     #                TM[SEQ[i]][SEQ[i+1]] +=  1
#     #            for i in range(len(SEQ)-1):
#     #                SM[SEQ[i]][CHOICE[0]]+= 1
#     #            SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 1
                
#             else:
#                 new_cost=cur_cost
#                 label_lane=copy.deepcopy(cur_lane)
#                 label_station=copy.deepcopy(cur_station)
            
            
#         if (n%batch == 0):
#             T = alpha * T
               









## .......................................SA..............................
#        if new_cost<cur_cost:
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#            cur_cost=new_cost
#      # Update best_cost,best_label_lane,best_label_station
#            if cur_cost<best_cost:
#                best_cost=cur_cost
#                print("up_cost=",best_cost)
#                best_lane=copy.deepcopy(cur_lane)
#                best_station=copy.deepcopy(cur_station)
#                best_iter=n
#                print("best_iter",best_iter)
#                acc_time.append(best_iter)
#
#                for i in range(len(SEQ)-1):
#                    TM[SEQ[i]][SEQ[i+1]] +=  1
#                for i in range(len(SEQ)-1):
#                    SM[SEQ[i]][CHOICE[0]]+= 1
#                SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 1
##            else:
##                for i in range(len(SEQ)-1):
##                    TM[SEQ[i]][SEQ[i+1]] +=  5
##                for i in range(len(SEQ)-1):
##                    SM[SEQ[i]][CHOICE[0]]+= 5
##                SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 5
#            
#        elif np.random.uniform(0, 1) < np.exp(-(new_cost-cur_cost)/T):
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#            cur_cost=new_cost
##            for i in range(len(SEQ)-1):
##                TM[SEQ[i]][SEQ[i+1]] +=  1
##            for i in range(len(SEQ)-1):
##                SM[SEQ[i]][CHOICE[0]]+= 1
##            SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= 1
#            
#        else:
#            new_cost=cur_cost
#            label_lane=copy.deepcopy(cur_lane)
#            label_station=copy.deepcopy(cur_station)
#        
#        
#        if (n%batch == 0):
#            T = alpha * T
#
##......................................

#  1.01+0.02.........................................................................
#        if new_cost<cur_cost*Rate:
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#            
#            if new_cost < cur_cost:
#                cur_cost=new_cost
#      # Update best_cost,best_label_lane,best_label_station
#                if cur_cost<best_cost:
#                    best_cost=cur_cost
#                    print("up_cost=",best_cost)
#                    best_lane=copy.deepcopy(cur_lane)
#                    best_station=copy.deepcopy(cur_station)
#                    best_iter=n
#                    print("best_iter",best_iter)
#                    acc_time.append(best_iter)
#                    Rate = 1.01
#
#                    for i in range(len(SEQ)-1):
#                        TM[SEQ[i]][SEQ[i+1]] +=  reward
#                    for i in range(len(SEQ)-1):
#                        SM[SEQ[i]][CHOICE[0]]+= reward
#                    SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= reward
#        else:
#            new_cost=cur_cost
#            label_lane=copy.deepcopy(cur_lane)
#            label_station=copy.deepcopy(cur_station)
#            if n > Max_gen*0.5:
##                rate_add = 0.05
#                if n-acc_time[len(acc_time)-1] >= Max_gen * 0.1 and n-acc_time[len(acc_time)-1] < Max_gen * 0.2:
#                    Rate = Rate0+rate_add
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.2 and n-acc_time[len(acc_time)-1] < Max_gen * 0.3:
#                    Rate = Rate0+rate_add * 2
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.3 and n-acc_time[len(acc_time)-1] < Max_gen * 0.4:
#                    Rate = Rate0+rate_add * 3
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.4 and n-acc_time[len(acc_time)-1] < Max_gen * 0.5:
#                    Rate = Rate0+rate_add * 4
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.5 and n-acc_time[len(acc_time)-1] < Max_gen * 0.6:
#                    Rate = Rate0+rate_add *5
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.6 and n-acc_time[len(acc_time)-1] < Max_gen * 0.7:
#                    Rate = Rate0+rate_add * 6
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.7 and n-acc_time[len(acc_time)-1] < Max_gen * 0.8:
#                    Rate = Rate0+rate_add * 7
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.8 and n-acc_time[len(acc_time)-1] < Max_gen * 0.9:
#                    Rate = Rate0+rate_add * 8
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.9 and n-acc_time[len(acc_time)-1] < Max_gen * 1:
#                    Rate = Rate0+rate_add * 9
#                    continue
                
 
                
                
                
#。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。
#            if n-acc_time[len(acc_time)-1] >= Max_gen * 0.1 and n-acc_time[len(acc_time)-1] < Max_gen * 0.2:
#                Rate = Rate0-rate_add
#                continue
#            elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.2 and n-acc_time[len(acc_time)-1] < Max_gen * 0.3:
#                Rate = Rate0-rate_add * 2
#                continue
#            elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.3 and n-acc_time[len(acc_time)-1] < Max_gen * 0.4:
#                Rate = Rate0-rate_add * 3
#                continue
#            elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.4 and n-acc_time[len(acc_time)-1] < Max_gen * 0.5:
#                Rate = Rate0-rate_add * 4
#                continue
#            elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.5:
#                Rate = 1
#                continue
#            elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.6 and n-acc_time[len(acc_time)-1] < Max_gen * 0.7:
#                Rate = Rate0-rate_add * 6
#                continue
#            elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.7 and n-acc_time[len(acc_time)-1] < Max_gen * 0.8:
#                Rate = Rate0-rate_add * 7
#                continue
#            elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.8 and n-acc_time[len(acc_time)-1] < Max_gen * 0.9:
#                Rate = Rate0-rate_add * 8
#                continue
#            elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.9 and n-acc_time[len(acc_time)-1] < Max_gen * 1:
#                Rate = Rate0-rate_add * 9
#                continue












#........only improvone+1.01,.02.......................................................................                              
#        if new_cost<cur_cost*Rate:
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#
#
#            if new_cost < cur_cost:
#                cur_cost=new_cost
#      # Update best_cost,best_label_lane,best_label_station
#                if cur_cost<best_cost:
#                    best_cost=cur_cost
#                    print("up_cost=",best_cost)
#                    best_lane=copy.deepcopy(cur_lane)
#                    best_station=copy.deepcopy(cur_station)
#                    best_iter=n
#                    print("best_iter",best_iter)
#                    acc_time.append(best_iter)
#                    Rate = 1      
#                    for i in range(len(SEQ)-1):
#                        TM[SEQ[i]][SEQ[i+1]] +=  reward
#                    for i in range(len(SEQ)-1):
#                        SM[SEQ[i]][CHOICE[0]]+= reward
#                    SM[SEQ[len(SEQ)-1]][CHOICE[1]]+= reward
#                                
#                    
#                    
#        else:
#            new_cost=cur_cost
#            label_lane=copy.deepcopy(cur_lane)
#            label_station=copy.deepcopy(cur_station)
#            if n > Max_gen*0.5:
#                if n-acc_time[len(acc_time)-1] >= Max_gen * 0.1 and n-acc_time[len(acc_time)-1] < Max_gen * 0.2:
#                    Rate = Rate0+rate_add * 1
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.2 and n-acc_time[len(acc_time)-1] < Max_gen * 0.3:
#                    Rate = Rate0+rate_add * 2
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.3 and n-acc_time[len(acc_time)-1] < Max_gen * 0.4:
#                    Rate = Rate0+rate_add * 3
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.4 and n-acc_time[len(acc_time)-1] < Max_gen * 0.5:
#                    Rate = Rate0+rate_add * 4
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.5 and n-acc_time[len(acc_time)-1] < Max_gen * 0.6:
#                    Rate = Rate0+rate_add *5
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.6 and n-acc_time[len(acc_time)-1] < Max_gen * 0.7:
#                    Rate = Rate0+rate_add * 6
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.7 and n-acc_time[len(acc_time)-1] < Max_gen * 0.8:
#                    Rate = Rate0+rate_add * 7
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.8 and n-acc_time[len(acc_time)-1] < Max_gen * 0.9:
#                    Rate = Rate0+rate_add * 8
#                    continue
#                elif n-acc_time[len(acc_time)-1] >= Max_gen * 0.9 and n-acc_time[len(acc_time)-1] < Max_gen * 1:
#                    Rate = Rate0-rate_add * 9
#                    continue
##              
#..............................................................................               
                
                
                
                
                
                
                
                
                
                
    end_time = time.time()
    cal_time = end_time-start_time
    best_cost, fixcost, bike_flow = cal_new_cost(best_station, best_lane, cost_station, cost_lane,
                                                  lane, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)
    result = ["{0}{1}".format("Ex ", Ex_ID), best_cost, fixcost, (best_cost-fixcost)/20000,
              best_lane, best_station, best_iter, cal_time, TM, SM, No_0, No_1, No_2, No_3, No_4, No_5, No_6,No_7,bike_flow,acc_time,total_generation]
    print("best_cost= ",best_cost,".....cal_time= ", cal_time)

#    print('best_iter=',best_iter)
#    print('time=',cal_time)
#    print("Best Combination",best_cost,fixcost,((best_cost-fixcost)/20000),best_lane,best_station)
#

#
#    test_lane=[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
#    test_station=[1,2,3,4]
#    test_cost,test_fixcost =cal_new_cost(station,test_station,test_lane,cost_station,cost_lane,lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)
#    print("Test11",test_cost,test_fixcost,((test_cost-test_fixcost)/20000),test_lane,test_station)

#    test_lane = np.array(np.zeros((76)),dtype = np.int)
#    test_station = np.array(np.zeros((24)),dtype = np.int)
#    for i in range(76):
#        if i in [37,41,43]:
#            test_lane[i] = 1
#    for i in range(24):
#        if i in [0,12]:
#            test_station[i] = 1
#    test_cost,test_fixcost,test_fwtime,test_bike_flow =cal_new_cost(test_station,test_lane,cost_station,cost_lane,lane,Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)
#    print("Test11",test_cost,test_fixcost,((test_cost-test_fixcost)/20000),test_lane,test_station)
            
#    test_station=np.array(np.zeros((24)))
#    test_station = [0,2,0,4,0,6,7,26,9,10,11,12,13,14,15,16,28,18,29,20,21,22,0,31]
#   2.28,9
     
#    for i in range(76):
#        if i in [3,15,18,21,23,32,38,46,49,58,60,68,71,72,74]:
#            test_lane[i] = 1
#    test_station=np.array(np.zeros((24)))
#    test_station = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,29,18,19,20,30,22,0,31]
#    

    return result


# 从列表中写入csv文件 -->从data中读取列表(一)
# csvFile2 = open('csvFile2.csv','w',newline='',encoding='utf-8')
# writer = csv.writer(csvFile2)
# m = len(data)
# for i in range(m):
#     writer.writerow(data[i])
# csvFile2.close()


# 5. 关闭文件

# workbook.save('solution.xlsx')
#        a.append(result)
# 参数对应 行, 列, 值
#worksheet.write(1,0, label = 'this is test')

# 保存
# workbook.save('Excel_test.xls')
# worksheet.write('A1', 'Hello world') # 向A1写入
#
# worksheet.write(1,1,'guoshun')#向第二行第二例写入guoshun
# best_lane=[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
# best_station=[1,2,3,4]
#best_cost,fixcost =cal_new_cost(station,best_station,best_lane,cost_station,cost_lane,lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)
# print("Test11",best_cost,fixcost,((best_cost-fixcost)/20000),best_lane,best_station)
