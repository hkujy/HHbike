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
    print(lane,station)
    return lane,station

def cal_new_cost(_label_station,_label_lane,_cost_station,_cost_lane,_lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand):
    fixed_cost=0
    _new_cost=0
    once_FW_time = 0
    for i in range(len(demand)):
        if _label_station[i]!=0:
            fixed_cost+=_cost_station[_label_station[i]-1]
    for i in _lane:
        if _label_lane[i]!=0:
            fixed_cost+=_cost_lane[i]
    if fixed_cost>Budget:
#        print("over budget")
        _new_cost=Budget+fixed_cost 
    else:    
   # time_cost
        time_cost=0
        No_edge = len(_cost_lane)
        nt_a = data.read_network_auto(nt_a,_label_lane,No_edge)  
        nt_b = data.read_network_bike(nt_b,_label_lane,No_edge)
        star_FW=time.time()
#        print("lane=",_label_lane,"station=",_label_station)
        vol_a,vol_b,time_cost = assignment.assign.FW_main(nt_a,nt_b,od_info,od_flow,_label_lane,_label_station,time_station,UE_converge,sita,fy,demand)
        end_FW=time.time()
        once_FW_time = end_FW-star_FW
#        print("fw time=", end_FW-star_FW)
#        if isOutPutDetail:
#        print("*****motor vehicles*****")
#        for link in vol_a.keys():
#            print("{0},{1}".format(link,vol_a[link]))
#        print("*****bikes*****")
#        for link in vol_b.keys():
#            print("{0},{1}".format(link,vol_b[link]))

        _new_cost=time_cost+fixed_cost
    return _new_cost,fixed_cost,once_FW_time


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

        
    if Ex_ID == 12:                # Five node - Med demand   - 10
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
    
        
    
        
    return case_ID,demand_ID,Budget,fy,sita,UE_converge,isOutPutDetail,Max_gen


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
run_ex_ID = [12,13]
for c in run_ex_ID:
    Ex_ID = c
    print("Ex_ID",Ex_ID)
    case_ID,demand_ID,Budget,fy,sita,UE_converge,isOutPutDetail,Max_gen = set_Ex_ID(Ex_ID)
    od_info,od_flow=data.read_od(case_ID,demand_ID)   #od_info list, od_demand  dict
    station,lane,cost_lane,cost_station,time_station,demand = data.set_sta_lane(case_ID)
    nt_a,nt_b=data.set_network(case_ID) 
    lane_set,station_set=enumeration()

    label_lane=np.array(np.zeros((6)),dtype=np.int)
    label_station = np.array(np.zeros((3)),dtype=np.int)
#    result=[]
    for i in range(len(lane_set)):
        for j in range(len(station_set)):
#            print(i,j)
            for m in range(6):
                label_lane[m] = lane_set[i,m]
            for n in range(3):
                label_station[n] = station_set [j,n]
#            c_label_lane = copy.deepcopy(label_lane)
#            c_label_station = copy.deepcopy(label_station)
            best_cost,fixcost,FW_time = cal_new_cost(label_station,label_lane,cost_station,cost_lane,lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)          
            result = []
            result = ["{0}{1}".format("Ex ",Ex_ID),best_cost,fixcost,(best_cost-fixcost)/20000,label_lane,label_station,FW_time] 
            result1 = copy.deepcopy(result)
#           result = ["{0}{1}".format("Ex ",Ex_ID),best_cost,fixcost,(best_cost-fixcost)/20000,lane_set[i],station_set[j],FW_time] 
            a.append(result1)
        
f = open('solution.csv','w',newline='')
writer = csv.writer(f)
writer.writerow(["Ex_ID","Best_cost","Constr_cost","Travel_time","Best_lane","Best_station","FW_time"])
for i in range(len(a)):
    writer.writerow(a[i])
f.close()