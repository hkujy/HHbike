# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 15:38:01 2020

@author: Cheng Rong
"""
import math
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

data = import_data.import_data()

def population(Pop_size, lane, demand,cost_station, cost_lane, Budget, od_info,
               od_flow, nt_a, nt_b, UE_converge, sita, fy):
    Initial_Group = np.array(
        np.zeros((Pop_size, len(lane)+len(demand)+2)), dtype=np.int64)
    no_sol = 0
    while no_sol < Pop_size:
        Initial_Group[no_sol,0:len(lane)+len(demand)] = np.random.randint(0, 2, len(lane)+len(demand))
        a0,a1,a2,a3 = cal_new_cost(Initial_Group[no_sol,len(lane):len(lane)+len(demand)],
                Initial_Group[no_sol,0:len(lane)],cost_station, cost_lane, lane, 
                Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)   
        if a1 <= Budget:
            Initial_Group[no_sol,len(lane)+len(demand)], Initial_Group[no_sol,len(lane)+len(demand)+1]= a0,a1
            no_sol = no_sol + 1
            
            
    
#    for i in range(Pop_size):
#        Initial_Group[i, 0:len(lane)+len(demand)] = np.random.randint(0, 2, len(lane)+len(demand))
        # print(Initial_Group[i, 0:len(lane)])
#        Initial_Group[i,len(lane):len(lane)+len(station)]= np.random.randint(0,len(demand)+1,len(station))
#        Initial_Group[i,len(lane):len(lane)+len(station)]= np.array([1,0,0,2,0,3])
#        for j in range(0, len(demand)):
#            f = []
#            a = np.random.random()
#            if a > 0.5:
#                f = list(time_station["N{:0>3}".format(demand[j])].keys())
#                Initial_Group[i,len(lane)+j]=np.random.choice(f)
#            else:
#                Initial_Group[i,len(lane)+j]=0
#            f = list(time_station["N{:0>3}".format(demand[j])].keys())
#            Initial_Group[i, len(lane)+j] = np.random.choice(f)
    return Initial_Group


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



def father_pair(Pop_size):
    selected = [0]*Pop_size  # 是否被选择了
    couples = []  # 配对list
    for i in range(Pop_size//2):
        pair = []
        while len(pair) < 2:
            unit_index = np.random.randint(0, Pop_size)
            if not selected[unit_index]:
                pair.append(unit_index)
                selected[unit_index] = True
        couples.append(pair)
    couples = np.array(couples)
    return couples


def crossover(Group, couples, cross_p, lane, demand):  # cross_p为交叉概率
    new_population = np.array(
        np.zeros((np.size(Group, 0), np.size(Group, 1))), dtype=np.int64)
    for i in range(np.size(couples, 0)):
        unit_one = Group[couples[i, 0], :]
        unit_two = Group[couples[i, 1], :]
        p = np.random.random()
        if p <= cross_p:
            # 交叉使用从随机位置交叉尾部
            '''
            point1 = 2
            point2 = 7
            '''
            point1 = np.random.randint(0, len(lane)-1)  # 获得随机位置
            point2 = np.random.randint(len(lane), len(lane)+len(demand)-1)
            new_population[i, 0:point1+1] = unit_one[0:point1+1]
            new_population[i, point1 +
                           1:len(lane)] = unit_two[point1+1:len(lane)]
            new_population[i, len(lane):point2 +
                           1] = unit_one[len(lane):point2+1]
            new_population[i, point2+1:len(lane)+len(demand)
                           ] = unit_two[point2+1:len(lane)+len(demand)]
            new_population[i+np.size(couples, 0),
                           0:point1+1] = unit_two[0:point1+1]
            new_population[i+np.size(couples, 0), point1 +
                           1:len(lane)] = unit_one[point1+1:len(lane)]
            new_population[i+np.size(couples, 0), len(lane):point2+1] = unit_two[len(lane):point2+1]
            new_population[i+np.size(couples, 0), point2+1:len(lane) +
                           len(demand)] = unit_one[point2+1:len(lane)+len(demand)]
        else:
            new_population[i, :] = unit_one
            new_population[i+np.size(couples, 0), :] = unit_two
    return new_population


def mutation(Group, mut_p, lane, cost_station, cost_lane, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand):
    new_population = Group
    a = math.ceil(np.size(Group, 0)*mut_p)
    for i in range(0, a):     
        point_lane = []
        while(len(point_lane) < 2):
            a = np.random.randint(0, len(lane))
            if a not in point_lane:
                point_lane.append(a)
        if point_lane[0] < point_lane[1]:
            point1 = point_lane[0]
            point2 = point_lane[1]
        else:
            point1 = point_lane[1]
            point2 = point_lane[0]
        point_station = []
        while(len(point_station) < 2):
            b = np.random.randint(len(lane), len(lane)+len(demand))
            if b not in point_station:
                point_station.append(b)
        if point_station[0] < point_station[1]:
            point3 = point_station[0]
            point4 = point_station[1]
        else:
            point3 = point_station[1]
            point4 = point_station[0]
#        if Group[i,point1] == 0:
#            new_population[i,point1] = 1
#        else:
#            new_population[i,point1] = 0
#        if Group[i,point2] == 0:
#            new_population[i,point2] = 1
#        else:
#            new_population[i,point2] = 0

        if Group[i, point1] == 0:
           new_population[i, point1] = 1
        else:
           new_population[i, point1] = 0 

        if Group[i, point2] == 0:
           new_population[i, point2] = 1
        else:
           new_population[i, point2] = 0 
         
        if Group[i, point3] == 0:
           new_population[i, point3] = 1
        else:
           new_population[i, point3] = 0 

        if Group[i, point4] == 0:
           new_population[i, point4] = 1
        else:
           new_population[i, point4] = 0 


#...........................
#        for j in range(point1, point2+1):
#            if Group[i, j] == 0:
#                new_population[i, j] = 1
#            else:
#                new_population[i, j] = 0
#        for j in range(point3, point4+1):
#            if Group[i, j] == 0:
#                new_population[i, j] = 1
#            else:
#                new_population[i, j] = 0

#...............................................zhege






#            d = np.random.choice(
#                list(time_station["N{:0>3}".format(demand[j-len(lane)])].keys()))
#            if d == Group[i, j]:
#                d = 0
#            new_population[i, j] = d
#

#        p = random.random()
#        if p<= mut_p:

#            point_lane = []
#            while(len(point_lane)<2):
#                a = np.random.randint(0,len(lane))
#                if a not in point_lane:
#                    point_lane.append(a)
#            if point_lane[0]<point_lane[1]:
#                point1 = point_lane[0]
#                point2 = point_lane[1]
#            else:
#                point1 = point_lane[1]
#                point2 = point_lane[0]
#            point_station = []
#            while(len(point_station)<2):
#                b = np.random.randint(len(lane),len(lane)+len(station))
#                if b not in point_station:
#                    point_station.append(b)
#            if point_station [0]<point_station [1]:
#                point3 = point_station [0]
#                point4 = point_station [1]
#            else:
#                point3 = point_station [1]
#                point4 = point_station [0]
#
#            '''
#            point1 = 1
#            point2 = 4
#            point3 = 6
#            point4 = 9
#            '''
#            if Group[i,point1] == 0:
#                new_population[i,point1] = 1
#            else:
#                new_population[i,point1] = 0
#            if Group[i,point2] == 0:
#                new_population[i,point2] = 1
#            else:
#                new_population[i,point2] = 0
#            for j in range(point3,point4+1):
#                d = random.choice(option[j-len(lane)])
#                start1 = time.time()
#                while d == Group[i,j]:
#                    d = random.choice(option[j-len(lane)])
#                new_population[i,j] = d
#                end1 = time.time()
#                print("while  ",end1-start1)
#            lane_mut = Group[i,point1:point2+1]
#            lane_mut = lane_mut.tolist()
#            lane_mut.reverse()
#            lane_mut = np.array(lane_mut)
#            new_population[i,point1:point2+1]=lane_mut
#            station_mut = Group[i,point3:point4+1]
#            station_mut = station_mut.tolist()
#            station_mut.reverse()
#            station_mut = np.array(station_mut)
#            new_population[i,point3:point4+1]=station_mut
    n_FW_time = 0
    for i in range(np.size(Group, 0)):
        new_population[i, np.size(new_population, 1)-2], new_population[i, np.size(new_population, 1)-1], once_FW,odbike_flow = cal_new_cost(new_population[i, len(lane):len(lane)+len(
            demand)], new_population[i, 0:len(lane)], cost_station, cost_lane, lane, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)
        n_FW_time = n_FW_time+once_FW
    new_population = new_population[np.argsort(
        new_population[:, np.size(new_population, 1)-2])]
#    new_population = new_population[new_population[:,np.size(new_population,1)-2].argsort()]
    return new_population, n_FW_time,odbike_flow


def next_pop(Father_Group, Child_Group, lane, cost_station, cost_lane):
    tem_population = np.array(np.zeros((np.size(
        Father_Group, 0)+np.size(Child_Group, 0), np.size(Father_Group, 1))), dtype=np.int64)
    new_population = np.array(
        np.zeros((np.size(Father_Group, 0), np.size(Father_Group, 1))), dtype=np.int64)

    for i in range(np.size(Father_Group, 0)):
        tem_population[i, :] = Father_Group[i, :]
    for i in range(np.size(Child_Group, 0)):
        tem_population[i+np.size(Father_Group, 0), :] = Child_Group[i, :]
    tem_population = tem_population[np.argsort(
        tem_population[:, np.size(tem_population, 1)-2])]
#    tem_population = tem_population[tem_population[:,np.size(new_population,1)-2].argsort()]


#    new_population[0,:]=tem_population[0,:]
#    for i in range(1,np.size(Father_Group,0)):
#        b = np.random.randint(0,np.size(tem_population,0))
#        new_population[i,:] = tem_population[b,:]
#    new_population = new_population[np.argsort(new_population[:,np.size(new_population,1)-2])]


#    a = int(np.size(Father_Group,0)*0.6)
#    for i in range(0,a):
#        new_population[i,:]=tem_population[i,:]
#    for i in range(a,np.size(Father_Group,0)):
#        new_population[i,:]=tem_population[np.size(Father_Group,0)-i,:]

    for i in range(np.size(Father_Group, 0)):
        new_population[i, :] = tem_population[i, :]

    return new_population


# def f_cost(Pop_size, station, cost_station,cost_lane,lane,cross_p,mutation_p,G,option):
#    case_ID,demand_ID,Budget,fy,sita,UE_converge,isOutPutDetail,Max_gen = set_Ex_ID(Ex_ID)
#    od_info,od_flow=data.read_od(case_ID,demand_ID)   #od_info list, od_demand  dict
#    station,lane,cost_lane,cost_station,time_station,demand = data.set_sta_lane(case_ID)
#    nt_a,nt_b=data.set_network(case_ID)
#    pro_TM,pro_SM=data.set_prob()
#    cumulative_pro_TM,cumulative_pro_SM=data.set_prob()
#    TM,SM=data.set_prob()
#
#
#
#    result=[]
#
#
#
#
#
#
#
#
#
#
#
#
#
#    Initial_Group = population(Pop_size,lane,station, demand,time_station)
#    for i in range(Pop_size):
#        Initial_Group[i,np.size(Initial_Group,1)-2],Initial_Group[i,np.size(Initial_Group,1)-1]= cal_new_cost(station, Initial_Group[i,len(lane):len(lane)+len(station)],Initial_Group[i,0:len(lane)],cost_station,cost_lane,lane,time_station)
#    Initial_Group = Initial_Group[np.argsort(Initial_Group[:,np.size(Initial_Group,1)-1])]
#    parent = father_pair(Pop_size)
##    parent = np.array([[0,1],[2,3]])
#    after_cross = crossover(Initial_Group, parent, cross_p,lane,station)
#    after_mutation = mutation(after_cross, mutation_p,lane,station,option,cost_station,cost_lane)
#    children = next_pop(Initial_Group, after_mutation, lane, station, cost_station,cost_lane)
#    min_cost=np.array(np.zeros((G,1)),dtype=np.int64)
#    min_cost[0,0]=children[0,np.size(children,1)-1]
#    sol_cost=np.array(np.zeros((G,np.size(Initial_Group,1))),dtype=np.int64)
#    sol_cost[0,:]=children[0,:]
#    for i in range(1,G):
# print(i)
#        parent = father_pair(Pop_size)
#        after_cross = crossover(children, parent, cross_p,lane,station)
#        after_mutation = mutation(after_cross, mutation_p,lane,station,option, cost_station,cost_lane)
#        children = next_pop(children, after_mutation, lane, station, cost_station,cost_lane)
#        min_cost[i,0]= children[:,np.size(children,1)-1].min()
# print(min_cost[i,0])
#        sol_cost[i,:]=children[0,:]
#	#plt.plot(min_cost)
#    return min_cost,sol_cost


#    return Initial_Group,after_cross,after_mutation,children


# best_lane=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# best_lane=[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
# best_station=[1,2,3,4,0]
#fixcost,best_cost =cal_new_cost(station,best_station,best_lane,cost_station,cost_lane,lane,time_station)
# print("Test",best_cost,fixcost,best_lane,best_station)

#run_time =3
# sol_iter=np.array(np.zeros((G,run_time)),dtype=np.int64)
# for i in range(run_time):
#    print('run=',i)
#    start = time.time()
#
#    a,b = f_cost(Pop_size, station, cost_station,cost_lane,lane,0.9,0.3,G,option)
#    sol_iter[:,i]=a[:,0]
#    end = time.time()
#    print('run---',i,'---time=',end-start)


def run_ga(Ex_ID):
    case_ID, demand_ID, Budget, fy, sita, UE_converge, Max_gen, cross_p, mutation_p, Pop_size = sid.set_Ex_ID(
        Ex_ID, _alg="GA")

    # od_info list, od_demand  dict
    od_info, od_flow = data.read_od(case_ID, demand_ID)

    lane, cost_lane, cost_station, demand = data.set_sta_lane(
        case_ID)

    nt_a, nt_b, net_bike = data.set_network(case_ID)

    result = []
    cal_FW_time = 0

    start_time = time.time()
    Initial_Group = population(Pop_size, lane, demand,cost_station, cost_lane, 
                               Budget, od_info,od_flow, nt_a, nt_b, UE_converge, sita, fy)
#    for i in range(Pop_size):
#        print("GA ini sol = ",i)
#        Initial_Group[i, np.size(Initial_Group, 1)-2], Initial_Group[i, np.size(Initial_Group, 1)-1], once_FW_time,od_bike = cal_new_cost(Initial_Group[i, len(lane):len(lane)+len(
#            station)], Initial_Group[i, 0:len(lane)], cost_station, cost_lane, lane, time_station, Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)
#        cal_FW_time = cal_FW_time + once_FW_time
    Initial_Group = Initial_Group[np.argsort(
        Initial_Group[:, np.size(Initial_Group, 1)-2])]
    parent = father_pair(Pop_size)
#    parent = np.array([[0,1],[2,3]])
    after_cross = crossover(Initial_Group, parent, cross_p, lane, demand)
    after_mutation, n_FW_time, bike_flow = mutation(after_cross, mutation_p, lane, cost_station, cost_lane,
                                         Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)
    cal_FW_time = cal_FW_time + n_FW_time
    children = next_pop(Initial_Group, after_mutation, lane,
                        cost_station, cost_lane)
    # time stop
    min_cost=[]
    min_cost.append(children[0, np.size(children, 1)-2])
    sol_cost = []
    sol_cost.append(children[0, :])
    # min_cost = np.array(np.zeros((Max_gen, 1)), dtype=np.int64)
    # min_cost[0, 0] = children[0, np.size(children, 1)-2]
    # sol_cost = np.array(
    #     np.zeros((Max_gen, np.size(Initial_Group, 1))), dtype=np.int64)
    # sol_cost[0, :] = children[0, :]
    
    cur_time = 0
    i = 0
    while cur_time-start_time <=300:
        cur_time = time.time()
        i = i+1
    # for i in range(1, Max_gen):
        print("GA Generation = ",i)
        parent = father_pair(Pop_size)
        after_cross = crossover(children, parent, cross_p, lane, demand)
        after_mutation, n_FW_time,bike_flow = mutation(after_cross, mutation_p, lane, cost_station, cost_lane,
                                             Budget, od_info, od_flow, nt_a, nt_b, UE_converge, sita, fy, demand)
        cal_FW_time = cal_FW_time + n_FW_time
        children = next_pop(children, after_mutation, lane,
                            cost_station, cost_lane)
        # min_cost[i, 0] = children[:, np.size(children, 1)-2].min()
        
        #  time stop
        min_cost.append (children[:, np.size(children, 1)-2].min())
        
#        print(min_cost[i,0])
        # sol_cost[i, :] = children[0, :]
        
        #  time stop
        sol_cost.append( children[0, :])
        
        # plt.plot(min_cost)
    end_time = time.time()
    cal_time = end_time-start_time
    best_iter = np.argmin(min_cost)
    # best_cost = sol_cost[best_iter, np.size(sol_cost, 1)-2]
    # fixcost = sol_cost[best_iter, np.size(sol_cost, 1)-1]
    # best_lane = np.array(np.zeros((len(lane))))
    # best_station = np.array(np.zeros((len(demand))))
    # best_lane[0:len(lane)] = sol_cost[best_iter, 0:len(lane)]
    # best_station[0:len(demand)] = sol_cost[best_iter,
    #                                        len(lane):len(demand)+len(lane)]

#  time stop
    best_cost = sol_cost[best_iter][np.size(sol_cost, 1)-2]
    fixcost = sol_cost[best_iter][np.size(sol_cost, 1)-1]
    best_lane = np.array(np.zeros((len(lane))))
    best_station = np.array(np.zeros((len(demand))))
    best_lane[0:len(lane)] = sol_cost[best_iter][0:len(lane)]
    best_station[0:len(demand)] = sol_cost[best_iter][len(lane):len(demand)+len(lane)]



    result = ["{0}{1}".format("Ex ", Ex_ID), best_cost, fixcost, (best_cost-fixcost) /
              20000, best_lane, best_station, best_iter, cal_time, cal_FW_time,bike_flow,i]


#    print('best_iter=',best_iter)
#    print('time=',cal_time)
#    print("Best Combination",best_cost,fixcost,((best_cost-fixcost)/20000),best_lane,best_station)
#

#
#    test_lane=[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
#    test_station=[1,2,3,4]
#    test_cost,test_fixcost =cal_new_cost(test_station,test_lane,cost_station,cost_lane,lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)
#    print("Test11",test_cost,test_fixcost,((test_cost-test_fixcost)/20000),test_lane,test_station)


#    test_lane= np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
#    test_station= np.array([1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,  0, 21, 30, 23, 24])

#    test_lane = np.array(np.zeros((76)))
#    for i in range(76):
#        test_lane[i] = 1
#    test_station=np.array(np.zeros((24)))
#    test_station = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
#    test_cost,test_fixcost =cal_new_cost(test_station,test_lane,cost_station,cost_lane,lane,time_station,Budget,od_info,od_flow,nt_a,nt_b,UE_converge,sita,fy,demand)
#    print("Test11",test_cost,test_fixcost,((test_cost-test_fixcost)/20000),test_lane,test_station)

    return result

