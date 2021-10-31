from copy import deepcopy
from assignment.graph import *
from assignment.line import *
from assignment.shortest_path import ShortestPath as SPP
#import assignment.globalpara as gl
import math
def find_y_flow(_net_a,_net_b,od_info,od_flow,od_flow_a,od_flow_b,_label_station,per_b,sita,fy):
    va_y = {}
    vb_y = {}
    timecost_b = deepcopy(od_flow)
    assign_flow_a=deepcopy(od_flow)
    assign_flow_b=deepcopy(od_flow)
    for l in _net_a.edge_id_set:
        va_y[l] = 0
    for l in _net_b.edge_id_set:
        vb_y[l] = 0    
#    
    for i in range(len(od_info)):
        o = od_info[i][0]
        d = od_info[i][1]
        cost_a, path_a = SPP.dijkstra(_net_a, o, d)
        cost_b, path_b = SPP.dijkstra(_net_b, o, d)
        timecost_b[o][d] = cost_b
        lpath_a = [_net_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
        lpath_b = [_net_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
        assign_flow_a[o][d] = 0
        assign_flow_b[o][d] = 0
        if od_flow[o][d]==0:
            assign_flow_a[o][d] = 0
            assign_flow_b[o][d] = 0
        elif per_b[o][d]==0:
            assign_flow_a[o][d] = od_flow[o][d]
            assign_flow_b[o][d] = 0
        else: 
            assign_flow_b[o][d] = od_flow[o][d]/(1+math.exp(sita*(cost_b-cost_a+fy)))
            assign_flow_a[o][d] = od_flow[o][d]-assign_flow_b[o][d]
    
        
        
        
#    for o in _origins:
#        for d in _dests:
#            cost_a, path_a = SPP.dijkstra(_net_a, o, d)
#            cost_b, path_b = SPP.dijkstra(_net_b, o, d)
#            timecost_b[o][d] = cost_b
#            lpath_a = [_net_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
#            lpath_b = [_net_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
#            assign_flow_a[o][d] = 0
#            assign_flow_b[o][d] = 0
#            if od_flow[o][d]==0:
#                assign_flow_a[o][d] = 0
#                assign_flow_b[o][d] = 0
#            elif per_b[o][d]==0:
#                assign_flow_a[o][d] = od_flow[o][d]
#                assign_flow_b[o][d] = 0
#            else: 
#                assign_flow_b[o][d] = od_flow[o][d]/(1+math.exp(gl.sita*(cost_b-cost_a+gl.fy)))
#                assign_flow_a[o][d] = od_flow[o][d]-assign_flow_b[o][d]
           
 # Update auxiliary variable (y)  ( potential_volume_auto, potential_volume_bike)
        for l in lpath_a:
            va_y[l] += assign_flow_a[o][d]
        for l in lpath_b:
            vb_y[l] += assign_flow_b[o][d]
        continue
    return va_y,vb_y, assign_flow_b,per_b,timecost_b


def update_net_cost(_net_a,_net_b,_va,_vb,_label,No_edge):
    _net_a.update_cost1(_va,_vb,_label,No_edge)
    _net_b.update_cost2(_va,_vb,_label,No_edge)


def initialization(_net_a,_net_b,od_info,od_flow,_label_lane,_label_station,demand):
    
    va = {}
    vb = {}
    for l in _net_a.edge_id_set:
        va[l] = 0
    for l in _net_b.edge_id_set:
        vb[l] = 0
    od_flow_a = deepcopy(od_flow)
    od_flow_b = deepcopy(od_flow)
    per_a = deepcopy(od_flow)
    per_b = deepcopy(od_flow)
    No_edge = len(_label_lane)
    _net_a.init_cost1(_label_lane,No_edge)
    _net_b.init_cost2(_label_lane,No_edge)
# 
    for i in range(len(od_info)):
        o = od_info[i][0]
        d = od_info[i][1]
        cost_a, path_a = SPP.dijkstra(_net_a, o, d)
        cost_b, path_b = SPP.dijkstra(_net_b, o, d)
        lpath_a = [_net_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
        lpath_b = [_net_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
        # intial condition set the demand for each mode to be equal
        per_a[o][d]=1
        per_b[o][d]=0
        
        a = []
        for e in range(len(demand)):
            if _label_station[e] != 0:
                a.append(e)
        for f in a:
            if o in ["N{:0>3}".format(demand[f])]:
                for g in a:
                    if d in ["N{:0>3}".format(demand[g])]:
                        per_a[o][d]=1/2
                        per_b[o][d]=1/2
                        break
                break   
    

#        for i in _label_station:
#            if o in ["N{:0>3}".format(i)]:
#                for j in _label_station:
#                    if d in ["N{:0>3}".format(j)]:  
#                        per_a[o][d]=1/2
#                        per_b[o][d]=1/2
#                        break
#                break


        od_flow_a[o][d]=per_a[o][d]*od_flow[o][d]
        od_flow_b[o][d]=per_b[o][d]*od_flow[o][d]
        for l in lpath_a:
            va[l] += od_flow_a[o][d]
        for l in lpath_b:
            vb[l] += od_flow_b[o][d]
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    for o in _origins:
#        for d in _dests:
#            cost_a, path_a = SPP.dijkstra(_net_a, o, d)
#            cost_b, path_b = SPP.dijkstra(_net_b, o, d)
#            lpath_a = [_net_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
#            lpath_b = [_net_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
#            # intial condition set the demand for each mode to be equal
#            per_a[o][d]=1
#            per_b[o][d]=0
#            for i in _label_station:
#                if o in ["N{:0>3}".format(i)]:
#                    for j in _label_station:
#                        if d in ["N{:0>3}".format(j)]:  
#                            per_a[o][d]=1/2
#                            per_b[o][d]=1/2
#                            break
#                    break
#            od_flow_a[o][d]=per_a[o][d]*od_flow[o][d]
#            od_flow_b[o][d]=per_b[o][d]*od_flow[o][d]
#            for l in lpath_a:
#                va[l] += od_flow_a[o][d]
#            for l in lpath_b:
#                vb[l] += od_flow_b[o][d]
    return va,vb,od_flow_a,od_flow_b,per_b

     
#def FW_main(network_a, network_b, od_flow, origins, destinations,_label_lane,_label_station,time_station):
def FW_main(network_a, network_b,od_info,od_flow,_label_lane,_label_station,UE_converge,sita,fy,demand):

    (va_x,vb_x,od_flow_a,od_flow_b,per_b) = initialization(network_a,network_b,od_info,od_flow,_label_lane,_label_station,demand)
#    IterCounter = 0
    converge = 1
    time_cost=0
    while converge>=UE_converge:
        No_edge = len(_label_lane)
        update_net_cost(network_a,network_b,va_x,vb_x,_label_lane,No_edge)
        (va_y,vb_y,v_b,per_b,timecost_b) = find_y_flow(network_a,network_b,od_info,od_flow,od_flow_a,od_flow_b,_label_station,per_b,sita,fy)
        step = cal_step(network_a,network_b, va_x,vb_x,va_y,vb_y,od_info,od_flow,od_flow_b,v_b,timecost_b,_label_lane,per_b,sita,fy)
        va_old =deepcopy(va_x)
        vb_old =deepcopy(vb_x)
        for link in network_a.edge_id_set:
            va_x[link] += step * (va_y[link] - va_x[link])
        for link in network_b.edge_id_set:
            vb_x[link] += step * (vb_y[link] - vb_x[link]) 
        for i in range(len(od_info)):
            o = od_info[i][0]
            d = od_info[i][1]
            if od_flow[o][d]==0:
                od_flow_b[o][d]=0
            elif per_b[o][d]!=0:
                od_flow_b[o][d] += step*(v_b[o][d]-od_flow_b[o][d])
            else:
                od_flow_b[o][d]=0
            od_flow_a[o][d]=od_flow[o][d]-od_flow_b[o][d]
        converge = cal_limit(va_x,va_old, vb_x, vb_old)
#        IterCounter+=1
#    print("iter={0},gap={1}".format(IterCounter,converge))
 

#        for o in origins:
#            for d in destinations:
#                if od_flow[o][d]==-1:
#                    od_flow_b[o][d]=-1
#                elif per_b[o][d]!=-1:
#                    od_flow_b[o][d] += step*(v_b[o][d]-od_flow_b[o][d])
#                else:
#                    od_flow_b[o][d]=-1
#                od_flow_a[o][d]=od_flow[o][d]-od_flow_b[o][d]
       
        
    #    0731
#    vol_b_o = dict()
    
#    

#    cur_origin=od_info[0][0]
#    h=0
#    for i in range(len(od_info)):
#        o = od_info[i][0]
#        if o in cur_origin:    
#            d=od_info[i][1]
#            if per_b[o][d]!=0:
#                h+=od_flow_b[o][d]
#        else:
#            vol_b_o[cur_origin]=h
#            cur_origin=o
#            h=0

#    
    
    
    
#    for o in origins:
#        h = 0
#        for d in destinations:
#            if per_b[o][d]!=0:
#                h+=od_flow_b[o][d]
#        vol_b_o[o]=h
        
#    vol_b_d = dict()


#

#    cur_dest=od_info[0][1]
#    p=0
#    for i in range(len(od_info)):
#        d = od_info[i][1]
#        if d in cur_dest:    
#            o=od_info[i][0]
#            if per_b[o][d]!=0:
#                p+=od_flow_b[o][d]
#        else:
#            vol_b_d[cur_dest]=p
#            cur_dest=d
#            p=0    

#    
    
    
    
#    for d in destinations:
#        p = 0
#        for o in origins:
#            if per_b[o][d]!=0:
#                p+=od_flow_b[o][d]
#        vol_b_d[d]=p
#'''    
#    walk_time=0    
#    for i in range(len(od_info)):
#        o = od_info[i][0]
#        d = od_info[i][1]
#        if od_flow_b[o][d]!=0:
#            for j in range(len(demand)):
#                if o in ["N{:0>3}".format(demand[j])]:
#                    walk_time+=od_flow_b[o][d]*time_station[o][_label_station[j]]
#            for j in range(len(demand)):
#                if d in ["N{:0>3}".format(demand[j])]:
#                    walk_time+=od_flow_b[o][d]*time_station[d][_label_station[j]]                    
#'''
          
 
    
    
#    for o in origins:
#        for j in range(len(_label_station)):
#            if o in ["N{:0>3}".format(_label_station[j])]:
#                walk_time+=vol_b_o[o]*time_station[o][j]
#    for d in destinations:
#        for j in range(len(_label_station)):
#            if d in ["N{:0>3}".format(_label_station[j])]:
#                walk_time+=vol_b_d[d]*time_station[d][j]
#    print('walk_time',walk_time)
#    
    
    time_cost=cal_timecost(network_a,network_b,va_x,vb_x,_label_lane)
    time_cost*=20000
    return va_x,vb_x,time_cost,od_flow_b
def cal_timecost(_network_a,_network_b,_va_x,_vb_x,_lab_lane):
    _time_cost=0
    a=0
    for lid in _va_x.keys():
        for j in range(1,len(_lab_lane)+1):
            if lid in ["E{:0>3}".format(j)]:
                a = _network_a.edgeset[lid].cal_weight1(_va_x[lid],_vb_x[lid],_lab_lane[j-1]) * _va_x[lid]
                _time_cost+=a
    for lid in _vb_x.keys():
        for j in range(1,len(_lab_lane)+1):
            if lid in ["E{:0>3}".format(j)]:
                a = _network_b.edgeset[lid].cal_weight2(_va_x[lid],_vb_x[lid],_lab_lane[j-1]) * _vb_x[lid]
                _time_cost+=a

#    
    return _time_cost 
            
   