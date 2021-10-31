# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 17:33:58 2020

@author: Cheng Rong
"""
import numpy as np
import xlrd
import import_data 
data=import_data.import_data()
import assignment
from assignment.assign import *
from assignment.line import *
from assignment.graph import *
import random
import copy
import time
import csv



def enumeration ():    
    book = xlrd.open_workbook("enumeration.xlsx")  
    table1 = book.sheet_by_name("lane")
    table2 = book.sheet_by_name("station")
    row_Num1 = table1.nrows
    col_Num1 = table1.ncols
    row_Num2 = table2.nrows
    col_Num2 = table2.ncols
    lane = np.array(np.zeros((row_Num1,col_Num1)),dtype=np.int)
    station = np.array(np.zeros((row_Num2,col_Num2)),dtype=np.int)
    
    for i in range(row_Num1):
        for j in range(col_Num1):
            lane[i,j] = int(table1.cell(i,j).value)
    for i in range(row_Num2):
        for j in range(col_Num2):
            station[i,j] = int(table2.cell(i,j).value)
#    print(lane,station)
    return lane,station

def cal_new_cost(_label_station, _label_lane, _cost_station, _cost_lane, _lane, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand):
    fixed_cost = 0
    _new_cost = 0
    once_FW_time = 0
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
        star_FW = time.time()
#        print("lane=",_label_lane,"station=",_label_station)
        vol_a, vol_b, time_cost, od_flow_bike = assignment.assign.FW_main(
            nt_a, nt_b, od_info, od_flow, _label_lane, _label_station, UE_converge, sita, fy, demand)
#        print("od_flow_bike=",od_flow_bike)
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
    return _new_cost, fixed_cost, once_FW_time, od_flow_bike


def set_Ex_ID(Ex_ID):  


    if Ex_ID == 7:
        case_ID=0
        demand_ID=0
        Budget=10000000000
        
        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1    
        
    if Ex_ID == 8:
        case_ID=0
        demand_ID=1
        Budget=10000000000
        
        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1 
        
        
    if Ex_ID == 9:
        case_ID=0
        demand_ID=2
        Budget=10000000000
        
        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1
        
        
    if Ex_ID == 10:              #Five node -  High demand  - 0.1
        case_ID=0
        demand_ID=2
        Budget=10000000000
        
        fy = 2.5
        sita = 0.1
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1
        
    if Ex_ID == 11:                # Five node - High demand   - 10
        case_ID=0
        demand_ID=2
        Budget=10000000000
        
        fy = 2.5
        sita = 10
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1

        
    if Ex_ID == 12:                # Five node - Med demand   - 0.1
        case_ID=0
        demand_ID=1
        Budget=10000000000
        
        fy = 2.5
        sita = 0.1
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1    
    
    if Ex_ID == 13:                # Five node - Med demand   - 10
        case_ID=0
        demand_ID=1
        Budget=10000000000
        
        fy = 2.5
        sita = 10
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1    
    
    
    
    if Ex_ID == 14:                # Five node - Low demand   - 0.1
        case_ID=0
        demand_ID=0
        Budget=10000000000
        
        fy = 2.5
        sita = 0.1
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1    
    
    if Ex_ID == 15:                # Five node - Low demand   - 10
        case_ID=0
        demand_ID=0
        Budget=10000000000
        
        fy = 2.5
        sita = 10
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1    
        
        
    if Ex_ID == 16:                # Five node - Low demand   - 5
        case_ID=0
        demand_ID=0
        Budget=10000000000
        
        fy = 2.5
        sita = 5
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1  
        
    if Ex_ID == 17:                # Five node - Med demand   - 5
        case_ID=0
        demand_ID=1
        Budget=10000000000
        
        fy = 2.5
        sita = 5
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1   
        
    if Ex_ID == 18:                # Five node - High demand   - 5
        case_ID=0
        demand_ID=2
        Budget=10000000000
        
        fy = 2.5
        sita = 5
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1   
    
    
    
    
    if Ex_ID == 19:                # Five node - Low demand   - 5
        case_ID=0
        demand_ID=0
        Budget=10000000000
        
        fy = 2.5
        sita = 0.5
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1  
        
    if Ex_ID == 20:                # Five node - Med demand   - 5
        case_ID=0
        demand_ID=1
        Budget=10000000000
        
        fy = 2.5
        sita = 0.5
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1   
        
    if Ex_ID == 21:                # Five node - High demand   - 5
        case_ID=0
        demand_ID=2
        Budget=10000000000
        
        fy = 2.5
        sita = 0.5
        UE_converge = 0.001
        isOutPutDetail = True    
        
        Max_gen = 1   
    
    
    
    
    if Ex_ID == 70:
        case_ID = 0
        demand_ID = 0
        Budget = 1000000

        fy = 2.5
#        sita = 1
        UE_converge = 0.001
#        isOutPutDetail = True

#        if _alg is "HH":        
#            Max_gen = 100
#            Pop_size = 10
#        elif _alg is "GA":
#            Max_gen = 10
#            pop_size = 10 
#            cross_p = 0.9
#            mutation_p = 0.3
#        else:
#            print("Warning")
 

    if Ex_ID == 80:
        case_ID = 0
        demand_ID = 1
        Budget = 1000000

        fy = 2.5
#        sita = 1
        UE_converge = 0.001
#        isOutPutDetail = True

#        if _alg is "HH":
#            Max_gen = 120
#            Pop_size = 10
#        elif _alg is "GA":
#            Max_gen = 12
#            pop_size = 10 
#            cross_p = 0.9
#            mutation_p = 0.3
#        else:
#            print("Warning")
  
    if Ex_ID == 90:
        case_ID = 0
        demand_ID = 2
        Budget = 1000000

        fy = 2.5
#        sita = 1
        UE_converge = 0.001
#        isOutPutDetail = True

#        if _alg is "HH":
#            Max_gen = 150
#            Pop_size = 10
#        elif _alg is "GA":
#            Max_gen = 15
#            pop_size = 10 
#            cross_p = 0.9
#            mutation_p = 0.3
        
    return case_ID,demand_ID,Budget,fy,UE_converge


#
#def run_enumeration(Ex_ID):
#    case_ID,demand_ID,Budget,fy,sita,UE_converge,isOutPutDetail,Max_gen = set_Ex_ID(Ex_ID)
#    
#    
#    #.....................input       od_demand,    network
##    data=import_data.import_data()
#    od_info,od_flow=data.read_od(case_ID,demand_ID)   #od_info list, od_demand  dict
#
#    station,lane,cost_lane,cost_station,time_station,demand = data.set_sta_lane(case_ID)
#    nt_a,nt_b=data.set_network(case_ID) 
#    label_lane, label_station = enumeration()
#    best_cost,fixcost,FW_time = cal_new_cost(label_station,label_lane,cost_station,cost_lane,lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)
#    result = ["{0}{1}".format("Ex ",Ex_ID),best_cost,fixcost,(best_cost-fixcost)/20000,label_lane[i],label_station[j],FW_time]
#    
#    return result


  
a=[]
d = []
enum_time = []
run_ex_ID = [70,80,90]

for c in run_ex_ID:
    Ex_ID = c
    print("Ex_ID",Ex_ID)

    case_ID,demand_ID,Budget,fy,UE_converge = set_Ex_ID(Ex_ID)
    od_info,od_flow=data.read_od(case_ID,demand_ID)   #od_info list, od_demand  dict
    lane,cost_lane,cost_station,demand = data.set_sta_lane(case_ID)
    nt_a,nt_b,net_bike=data.set_network(case_ID) 
    lane_set,station_set=enumeration()

    label_lane=np.array(np.zeros((6)),dtype=np.int)
    label_station = np.array(np.zeros((3)),dtype=np.int)
    start_time = time.time()
    
    sita = 0
    for k in range(1,51):
        sita =  0.1 * k
        b = []
        for i in range(len(lane_set)):
            for j in range(len(station_set)):
                for m in range(6):
                    label_lane[m] = lane_set[i,m]
                for n in range(3):
                    label_station[n] = station_set [j,n]
                best_cost,fixcost,FW_time, od_bike = cal_new_cost(label_station,label_lane,cost_station,cost_lane,lane,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)          
                result = []
                result = ["{0}{1}".format("Ex ",Ex_ID),"{0}{1}".format("sita ",sita),best_cost,fixcost,(best_cost-fixcost)/20000,label_lane,label_station,FW_time,od_bike] 
                result1 = copy.deepcopy(result)
                a.append(result1)
                b.append(result1)
                
        b.sort(key=lambda x:x[2])         
#        print(b)
        c1 = []
        c1 = b[0]
        print(c1)
        c = copy.deepcopy(c1)
        d.append(c)
    end_time = time.time()
    enum_time.append(end_time-start_time)
f = open('enum_solution.csv','w',newline='')
writer = csv.writer(f)
writer.writerow(["Ex_ID","sita","Best_cost","Constr_cost","Travel_time","Best_lane","Best_station","FW_time","Bike_flow"])
for i in range(len(a)):
    writer.writerow(a[i])
writer.writerow([enum_time])
f.close()

f1 = open('sita_sum.csv','w',newline='')
writer1 = csv.writer(f1)
writer1.writerow(["Ex_ID","sita","Best_cost","Constr_cost","Travel_time","Best_lane","Best_station","FW_time","Bike_flow"])
for j in range(len(d)):
    writer1.writerow(d[j])
f1.close()

