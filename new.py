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
import random
import copy
import time
import csv
import set_exp_id as sid


Run_time = 1
data = import_data.import_data()


# Step 4: Calculate the cost
def cal_new_cost(_label_station, _label_lane, _cost_station, _cost_lane, _lane, time_station, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand):
    fixed_cost = 0
    _new_cost = 0
    once_FW_time = 0
    for i in range(len(demand)):
        if _label_station[i] != 0:
            fixed_cost += _cost_station[_label_station[i]-1]
    for i in _lane:
        if _label_lane[i] != 0:
            fixed_cost += _cost_lane[i]
    if fixed_cost > Budget:
        #        print("over budget")
        _new_cost = Budget+fixed_cost
    else:
       # time_cost
        time_cost = 0
        No_edge = len(_cost_lane)
        nt_a = data.read_network_auto(nt_a, _label_lane, No_edge)
        nt_b = data.read_network_bike(nt_b, _label_lane, No_edge)
        star_FW = time.time()
#        print("lane=",_label_lane,"station=",_label_station)
        vol_a, vol_b, time_cost = assignment.assign.FW_main(
            nt_a, nt_b, od_info, od_flow, _label_lane, _label_station, time_station, UE_converge, sita, fy, demand)
        end_FW = time.time()
        once_FW_time = end_FW-star_FW
#        print("fw time=", end_FW-star_FW)
#        if isOutPutDetail:
#        print("*****motor vehicles*****")
#        for link in vol_a.keys():
#            print("{0},{1}".format(link,vol_a[link]))
#        print("*****bikes*****")
#        for link in vol_b.keys():
#            print("{0},{1}".format(link,vol_b[link]))

        _new_cost = time_cost+fixed_cost
    return _new_cost, fixed_cost, once_FW_time


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
        e = random.choice(d)
        _label_lane[e] = 1
    return _label_lane

# LLH1:Select a link in the bicycle link set and move it out of the bicycle link set.


def cal_L1_remove_bike_link(_label_lane, _lane):
    d = []
    e = 0
    for i in _lane:
        if _label_lane[i] == 1:
            d.append(i)
    if len(d) != 0:
        e = random.choice(d)
        _label_lane[e] = 0
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


def cal_L2_add_bike_station(_label_station, _station, _time_station, _demand, _od_flow):
    d = []
    e = 0
    for j in range(len(_demand)):
        if _label_station[j] == 0:
            d.append(j)
    if len(d) != 0:
        e = random.choice(d)
        f = []
        f = list(_time_station["N{:0>3}".format(_demand[e])].keys())
        _label_station[e] = random.choice(f)

        for i in d:
            if ["N{:0>3}".format(_demand[e])] in list(_od_flow.keys()):
                if ["N{:0>3}".format(_demand[i])] in list(_od_flow["N{:0>3}".format(_demand[e])].keys()):
                    g = []
                    g = list(
                        _time_station["N{:0>3}".format(_demand[i])].keys())
                    _label_station[i] = random.choice(g)
            elif ["N{:0>3}".format(_demand[i])] in list(_od_flow.keys()):
                if ["N{:0>3}".format(_demand[e])] in list(_od_flow["N{:0>3}".format(_demand[i])].keys()):
                    h = []
                    h = list(
                        _time_station["N{:0>3}".format(_demand[i])].keys())
                    _label_station[i] = random.choice(h)

#    d=[]
#    for i in _demand:
# if _match_station[i][e]==1:
#        if e in _time_station["N{:0>3}".format(i)].keys():
#             d.append(i)
#    if len(d)!=0:
#        f=random.choice(d)
#        _label_station[e]=f
    return _label_station

# LLH3:


def cal_L3_remove_bike_station(_label_station, _station, _time_station, _demand):
    a = []
    b = 0
    for i in range(len(_demand)):
        if _label_station[i] != 0:
            a.append(i)
    if len(a) != 0:
        b = random.choice(a)
        _label_station[b] = 0
    return _label_station


# LLH4:

def cal_L4_replace_bike_station(_label_station, _station, _time_station, _demand):
    a = []
    b = 0
    c = 0
    for i in range(len(_demand)):
        if _label_station[i] != 0:
            a.append(i)
    if len(a) != 0:
        check_a = np.array(np.zeros((len(a))), dtype=int)
        has_opt = False
        while has_opt == False:
            d = []
            for j in range(len(check_a)):
                if check_a[j] == 0:
                    d.append(j)
            if len(d) != 0:
                b = random.choice(d)
                check_a[b] = 1
                if ["N{:0>3}".format(_demand[a[b]])] in list(_time_station.keys()):
                    if len(_time_station["N{:0>3}".format(_demand[a[b]])].keys()) != 1:
                        c = random.choice(
                            list(_time_station["N{:0>3}".format(_demand[a[b]])].keys()))
                        _label_station[b] = c
                        has_opt = True
            else:
                break

    return _label_station


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
    cur = random.randint(0, len(LLH)-1)
    SEQ.append(LLH[cur])

    # LLH(next) is chosen by a selection procedure based on the roulette wheel selection strategy
    """
    start of the roulette wheel
    """
    a = 0
    b = 0
    c = random.uniform(0, 1)
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
    c = random.uniform(0, 1)
    for j in CHOICE:
        a += SM[cur][j]
    for j in CHOICE:
        pro_SM[cur][j] = SM[cur][j]/a
    cumulative_pro_SM[cur][CHOICE[0]] = pro_SM[cur][CHOICE[0]]
    cumulative_pro_SM[cur][CHOICE[1]] = 1
    while cumulative_pro_SM[cur][CHOICE[0]] < c:
        a = 0
        b = 0
        c = random.uniform(0, 1)
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
        c = random.uniform(0, 1)
        for j in CHOICE:
            a += SM[cur][j]
        for j in CHOICE:
            pro_SM[cur][j] = SM[cur][j]/a
        cumulative_pro_SM[cur][CHOICE[0]] = pro_SM[cur][CHOICE[0]]
        cumulative_pro_SM[cur][CHOICE[1]] = 1
    return SEQ

 # step 3:apply SEQ


def cal_apply(_uSEQ, _ulabel_lane, _ulane, _ulabel_station, _ustation, _utime_station, _udemand, _uod_flow):
    for i in _uSEQ:
        if i in ["L0"]:
            _ulabel_lane = cal_L0_add_bike_link(
                _label_lane=_ulabel_lane, _lane=_ulane)
            continue
        if i in ["L1"]:
            _ulabel_lane = cal_L1_remove_bike_link(
                _label_lane=_ulabel_lane, _lane=_ulane)
            continue
        if i in ["L2"]:
            _ulabel_station = cal_L2_add_bike_station(
                _label_station=_ulabel_station, _station=_ustation, _time_station=_utime_station, _demand=_udemand, _od_flow=_uod_flow)
            continue
        if i in ["L3"]:
            _ulabel_station = cal_L3_remove_bike_station(
                _label_station=_ulabel_station, _station=_ustation, _time_station=_utime_station, _demand=_udemand)
            continue
        if i in ["L4"]:
            _ulabel_station = cal_L4_replace_bike_station(
                _label_station=_ulabel_station, _station=_ustation, _time_station=_utime_station, _demand=_udemand)
            '''
        if i in ["L5"]: 
            _ulabel_station=cal_L5_insert_bike_station(_label_station=_ulabel_station,_station=_ustation,_time_station=_utime_station,_demand=_udemand)
            continue
        if i in ["L6"]:
            _ulabel_station=cal_L6_swap_bike_station(_label_station=_ulabel_station,_station=_ustation,_time_station=_utime_station,_demand=_udemand)
            '''
    return _ulabel_lane, _ulabel_station


# for run in range(Run_time):
#    print("run",run)
def run_upper(Ex_ID):
    #    case_ID=0
    #    demand_ID=1
    #    Budget=10000000000
    #
    #    fy = 2.5
    #    sita = 1
    #    UE_converge = 0.001
    #    isOutPutDetail = True
    case_ID, demand_ID, Budget, fy, sita, UE_converge, isOutPutDetail, Max_gen = sid.set_Ex_ID(
        Ex_ID, _alg="HH")
    # .....................input       od_demand,    network
    #    data=import_data.import_data()
    # od_info list, od_demand  dict
    od_info, od_flow = data.read_od(case_ID, demand_ID)

    station, lane, cost_lane, cost_station, time_station, demand = data.set_sta_lane(
        case_ID)
    nt_a, nt_b = data.set_network(case_ID)
    # ....................Initialization
#    SEQ = []
    LLH = ['L0', 'L1', 'L2', 'L3', 'L4']

    pro_TM, pro_SM = data.set_prob()
    cumulative_pro_TM, cumulative_pro_SM = data.set_prob()
    TM, SM = data.set_prob()
#    pro_SM=copy.deepcopy(SM)
    CHOICE = ['STOP', 'CONTINUE']
#    cumulative_pro_SM=copy.deepcopy(SM)
    best_lane = np.array(np.zeros((len(lane))), dtype=np.int)
#    for i in range(len(lane)):
#        best_lane[i] = np.random.randint(0,2)
#        best_lane[i] = 1

    best_station = np.array(np.zeros((len(demand))), dtype=np.int)
    for i in range(len(demand)):
        best_station[i] = random.choice(
            list(time_station["N{:0>3}".format(demand[i])].keys()))
#        z = random.random()
#        if z> 0.5:
#            best_station[i] = random.choice(list(time_station["N{:0>3}".format(demand[i])].keys()))
#        else:
#            best_station[i] = 0
    cur_lane = copy.deepcopy(best_lane)
    cur_station = copy.deepcopy(best_station)
    label_lane = copy.deepcopy(best_lane)
    label_station = copy.deepcopy(best_station)
    best_cost = 1000000000000000
    cur_cost = 1000000000000000
    result = []

    No_0 = 0
    No_1 = 0
    No_2 = 0
    No_3 = 0
    No_4 = 0

    FW_time = 0

    # Step 5: test upper
    n = 0
    start_time = time.time()
    sol_cost = np.array(np.zeros((Max_gen+1, 1)))
    while n < Max_gen:
        #        print(n)
        n += 1
        SEQ = []
        SEQ = cal_HSS(LLH, SEQ, cumulative_pro_TM, TM, pro_TM,
                      CHOICE, SM, pro_SM, cumulative_pro_SM)
#        SEQ = ['L2','L2','L2','L2']
#        print("SEQ= ",SEQ)
        for y in range(len(SEQ)):
            if SEQ[y] == 'L0':
                No_0 += 1
            if SEQ[y] == 'L1':
                No_1 += 1
            if SEQ[y] == 'L2':
                No_2 += 1
            if SEQ[y] == 'L3':
                No_3 += 1
            if SEQ[y] == 'L4':
                No_4 += 1

        label_lane, label_station = cal_apply(_uSEQ=SEQ, _ulabel_lane=label_lane, _ulane=lane, _ulabel_station=label_station,
                                              _ustation=station, _utime_station=time_station, _udemand=demand, _uod_flow=od_flow)
#        print("station= ", label_station)
        # Acceptence method:Only Improve
        new_cost, newfixcost, o_FW_time = cal_new_cost(
            label_station, label_lane, cost_station, cost_lane, lane, time_station, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)
        FW_time = FW_time + o_FW_time
        sol_cost[n, 0] = copy.copy(new_cost)
        if new_cost < cur_cost:
            cur_cost = new_cost
            cur_lane = copy.deepcopy(label_lane)
            cur_station = copy.deepcopy(label_station)
          # Update TM and SM
            for i in range(len(SEQ)-1):
                TM[SEQ[i]][SEQ[i+1]] += 1
            for i in range(len(SEQ)-1):
                SM[SEQ[i]][CHOICE[0]] += 1
            SM[SEQ[len(SEQ)-1]][CHOICE[1]] += 1

      # Update best_cost,best_label_lane,best_label_station
            if cur_cost < best_cost:
                best_cost = cur_cost
                best_lane = copy.deepcopy(cur_lane)
                best_station = copy.deepcopy(cur_station)
                best_iter = n
        else:
            new_cost = cur_cost
            label_lane = copy.deepcopy(cur_lane)
            label_station = copy.deepcopy(cur_station)


#        if new_cost<cur_cost*1.1:
#            cur_lane=copy.deepcopy(label_lane)
#            cur_station=copy.deepcopy(label_station)
#            if new_cost < cur_cost:
#                cur_cost=new_cost
#              # Update TM and SM
#                for i in range(len(SEQ)-1):
#                    TM[SEQ[i]][SEQ[i+1]] += 1
#                for i in range(len(SEQ)-1):
#                    SM[SEQ[i]][CHOICE[0]]+=1
#                SM[SEQ[len(SEQ)-1]][CHOICE[1]]+=1
#
#      # Update best_cost,best_label_lane,best_label_station
#                if cur_cost<best_cost:
#                    best_cost=cur_cost
#                    best_lane=copy.deepcopy(cur_lane)
#                    best_station=copy.deepcopy(cur_station)
#                    best_iter=n
#        else:
#            new_cost=cur_cost
#            label_lane=copy.deepcopy(cur_lane)
#            label_station=copy.deepcopy(cur_station)

    end_time = time.time()
    cal_time = end_time-start_time
    best_cost, fixcost, on_FW_time = cal_new_cost(best_station, best_lane, cost_station, cost_lane,
                                                  lane, time_station, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)
    result = ["{0}{1}".format("Ex ", Ex_ID), best_cost, fixcost, (best_cost-fixcost)/20000,
              best_lane, best_station, best_iter, cal_time, TM, SM, No_0, No_1, No_2, No_3, No_4, FW_time]


#    print('best_iter=',best_iter)
#    print('time=',cal_time)
#    print("Best Combination",best_cost,fixcost,((best_cost-fixcost)/20000),best_lane,best_station)
#

#
#    test_lane=[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
#    test_station=[1,2,3,4]
#    test_cost,test_fixcost =cal_new_cost(station,test_station,test_lane,cost_station,cost_lane,lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)
#    print("Test11",test_cost,test_fixcost,((test_cost-test_fixcost)/20000),test_lane,test_station)

#    test_lane = np.array(np.zeros((76)))
#    for i in range(76):
#        test_lane[i] = 1
#    test_station=np.array(np.zeros((24)))
#    test_station = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
#    test_cost,test_fixcost =cal_new_cost(test_station,test_lane,cost_station,cost_lane,lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)
#    print("Test11",test_cost,test_fixcost,((test_cost-test_fixcost)/20000),test_lane,test_station)

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
