# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 11:32:51 2020

@author: Cheng Rong
"""

'''
read excel and create dict like this:
    od_flow = {'N001': {'N002':4000,'N003':2500},
              'N004': {'N002':3500,'N003':2000}}
    od_flow['N001']['N002']=4000
'''


import numpy as np
from assignment.assign import *
from assignment.line import *
from assignment.graph import *
class import_data():

    def read_od(self, case_ID, demand_ID):    
        
        od_info = []
        if case_ID == 0 and demand_ID == 0:
            with open('Small_Low_demand.csv', 'r') as fo:
                lines = fo.readlines()
        
        if case_ID == 0 and demand_ID == 1:
            with open('Small_Med_demand.csv', 'r') as fo:
                lines = fo.readlines()
        
        if case_ID == 0 and demand_ID == 2:
            with open('Small_High_demand.csv', 'r') as fo:
                lines = fo.readlines()
        
        if case_ID == 1 and demand_ID == 0:
            with open('ND_Low_demand.csv', 'r') as fo:
                lines = fo.readlines()
                
        if case_ID == 1 and demand_ID == 1:
            with open('ND_Med_demand.csv', 'r') as fo:
                lines = fo.readlines()
                
        if case_ID == 1 and demand_ID == 2:
            with open('ND_High_demand.csv', 'r') as fo:
                lines = fo.readlines()
                
        if case_ID == 2 and demand_ID == 0:
            with open('SF_Low_demand.csv', 'r') as fo:
                lines = fo.readlines()
                
        if case_ID == 2 and demand_ID == 1:
            with open('SF_Med_demand.csv', 'r') as fo:
                lines = fo.readlines()
                
        if case_ID == 2 and demand_ID == 2:
            with open('SF_High_demand.csv', 'r') as fo:
                lines = fo.readlines()    
    
        for ln in lines:
            a = ln.split(',')
            od_info.append(a)
        for i in range(len(od_info)):
            od_info[i][2] = int(od_info[i][2])
        
#        print("od_info",type(od_info),od_info,od_info[0][1])
        od_demand = {}
        key1 = {}
        a = {}
#        for i in range(len(od_info)):
#            key1[i] = od_info[i][0]
        cur_origin = od_info[0][0]
        for i in range(len(od_info)):
            key1[i] = od_info[i][0]
            if key1[i] == cur_origin:
                key2 = od_info[i][1]
                a[key2] = int(od_info[i][2])
                od_demand[key1[i]] = a
            else:
                a = {}
                key2 = {}
                cur_origin = od_info[i][0]
                key2 = od_info[i][1]
                a[key2] = int(od_info[i][2])
                od_demand[key1[i]] = a           
#        print("od_demand",od_demand,type(od_demand),od_demand["N001"]["N003"])
        
#        print("od_info=",od_info,"od_demand=",od_demand)
        return od_info,od_demand
        


    def set_network(self, case_ID):
        nt_a = network_a('net_a')
        node_a = vertex_a("a_a")
        if case_ID == 0:
            with open('auto_small.csv', 'r') as fo:
                lines = fo.readlines()
                for ln in lines:
                    eg_a = ln.split(',')
                    nt_a.add_edge(edge_a(eg_a))
        if case_ID == 1:
            with open('auto_ND.csv', 'r') as fo:
                lines = fo.readlines()
                for ln in lines:
                    eg_a = ln.split(',')
                    nt_a.add_edge(edge_a(eg_a))
        if case_ID == 2:
            with open('auto_SF.csv', 'r') as fo:
                lines = fo.readlines()
                for ln in lines:
                    eg_a = ln.split(',')
                    nt_a.add_edge(edge_a(eg_a))

        nt_b = network_b('net_b')
        node_b = vertex_b("a_b")
        if case_ID == 0:
            with open('bike_small.csv', 'r') as fo:
                lines = fo.readlines()
#                for ln in lines:
#                    eg_b = ln.split(',')
#                    nt_b.add_edge(edge_b(eg_b))
        if case_ID == 1:
            with open('bike_ND.txt', 'r') as fo:
                lines = fo.readlines()
#                for ln in lines:
#                    eg_b = ln.split(',')
#                    nt_b.add_edge(edge_b(eg_b))
        if case_ID == 2:
            with open('bike_SF.csv', 'r') as fo:
                lines = fo.readlines()
#                for ln in lines:
#                    eg_b = ln.split(',')
#                    nt_b.add_edge(edge_b(eg_b))
#        print (type(nt_a))
        

        network_bike_info = []
        for ln in lines:
            eg_b = ln.split(',')
            nt_b.add_edge(edge_b(eg_b))
            network_bike_info.append(eg_b)
        key1 = {}
        network_bike = {}
        for i in range(len(network_bike_info)):
            a = {}
            key1[i] = network_bike_info[i][0]
            a['o'] = network_bike_info[i][1]
            a['d'] = network_bike_info[i][2]
            network_bike[key1[i]] = a
#        print("network_bike= ", network_bike)

        return nt_a, nt_b,network_bike

    def set_sta_lane(self, case_ID):
        
        list_cost_lane = []
        list_cost_station = []
#        list_time_station = []
        list_demand_point = []
        
        od_info = []
        if case_ID == 0:
            with open('Small_Lane_cost.csv', 'r') as fo1:
                lines1 = fo1.readlines()
            with open('Small_Station_cost.csv', 'r') as fo2:
                lines2 = fo2.readlines()
#            with open('Small_Time_station.csv', 'r') as fo3:
#                lines3 = fo3.readlines()
            with open('Small_Demand_point.csv', 'r') as fo4:
                lines4 = fo4.readlines()
                
        if case_ID == 1:
            with open('ND_Lane_cost.csv', 'r') as fo1:
                lines1 = fo1.readlines()
            with open('ND_Station_cost.csv', 'r') as fo2:
                lines2 = fo2.readlines()
#            with open('ND_Time_station.csv', 'r') as fo3:
#                lines3 = fo3.readlines()
            with open('ND_Demand_point.csv', 'r') as fo4:
                lines4 = fo4.readlines()
        
        if case_ID == 2:
            with open('SF_Lane_cost.csv', 'r') as fo1:
                lines1 = fo1.readlines()
            with open('SF_Station_cost.csv', 'r') as fo2:
                lines2 = fo2.readlines()
#            with open('SF_Time_station.csv', 'r') as fo3:
#                lines3 = fo3.readlines()
            with open('SF_Demand_point.csv', 'r') as fo4:
                lines4 = fo4.readlines()
        
        
        
        
        for ln in lines1:
            a = ln.split(',')
            list_cost_lane.append(a)
        
        for ln in lines2:
            a = ln.split(',')
            list_cost_station.append(a)
            
#        for ln in lines3:
#            a = ln.split(',')
#            list_time_station.append(a)
        
        for ln in lines4:
            a = ln.split(',')
            list_demand_point.append(a)  
        
        
        
        
        
        
        lane = range(0, len(list_cost_lane))
#        station = range(0, len(list_cost_station))
        demand_point = np.array(np.zeros((len(list_demand_point))),dtype=np.int)
        for i in range (len(list_demand_point)):
            demand_point[i] = int(list_demand_point[i][0])
        cost_lane = np.array(np.zeros((len(list_cost_lane))), dtype=np.int)
        for i in range(len(list_cost_lane)):
            cost_lane[i] = int(list_cost_lane[i][0])
        cost_station = np.array(np.zeros((len(list_cost_station))),dtype=np.int)
        for i in range(len(list_cost_station)):
            cost_station[i] = int(list_cost_station[i][0])
        
       

#        od_sta_info = []
#        for i in range(len(list_time_station)):
#            a = list_time_station[i]
#            od_sta_info.append(a)
#        time_station = {}
#        key1 = {}
#        a = {}
#        for i in range(len(list_time_station)):
#            key1[i] = list_time_station[i][0]
#        cur_origin = list_time_station[0][0]
#        for i in range(len(list_time_station)):
#            key1[i] = list_time_station[i][0]
#            if key1[i] == cur_origin:
#                key2 = int(list_time_station[i][1])
#                a[key2] = float(list_time_station[i][2])
#                time_station[key1[i]] = a
#            else:
#                a = {}
#                key2 = {}
#                cur_origin = list_time_station[i][0]
#                key2 = int(list_time_station[i][1])
#                a[key2] = float(list_time_station[i][2])
#                time_station[key1[i]] = a
                
#        print(station,lane,cost_lane,cost_station,time_station["N001"][1],"time_station",time_station,demand_point)

        return lane, cost_lane, cost_station, demand_point

    def read_network_auto(self, nt_a, _label_lane, No_edge):
        # initialize cost_auto
        nt_a.init_cost1(_label_lane, No_edge)
        return nt_a

    def read_network_bike(self, nt_b, _label_lane, No_edge):
        # initialize cost_bike
        nt_b.init_cost2(_label_lane, No_edge)
        return nt_b

    def set_prob(self):
#        book = xlrd.open_workbook("LLH.xlsx")
#        # 找到sheet页
#        tab_TM = book.sheet_by_name("TM")
#        tab_SM = book.sheet_by_name("SM")
#        row_Num1 = tab_TM.nrows
#        col_Num1 = tab_TM.ncols
#        row_Num2 = tab_SM.nrows
#        col_Num2 = tab_SM.ncols
        LLH_TM = []
        LLH_SM = []
        
        with open('LLH_TM.csv', 'r') as fo1:            
            lines1 = fo1.readlines()
        for ln in lines1:
            ln = ln.strip('\n')
            a = ln.split(',') 
            LLH_TM.append(a)
    
        with open('LLH_SM.csv', 'r') as fo2:
            lines2 = fo2.readlines()
        for ln in lines2:
            ln = ln.strip('\n')
            a = ln.split(',') 

            LLH_SM.append(a)

#        print(type(LLH_TM),LLH_TM,LLH_SM)  

        
        TM = {}
        key1 = {}
        key2 = {}
        val = np.array(np.zeros((len(LLH_TM)-1, len(LLH_TM)-1)), dtype=np.int)
#        a={}
        for i in range(len(LLH_TM)-1):
            key1[i] = LLH_TM[i+1][0]
        for j in range(len(LLH_TM)-1):
            key2[j] = LLH_TM[0][j+1]
        for i in range(len(LLH_TM)-1):
            a = {}
            for j in range(len(LLH_TM)-1):
                val[i,j] = LLH_TM[i+1][j+1]
            for k in range(len(key2)):
                a[key2[k]] = val[i, k]
            TM[key1[i]] = a

        SM = {}
        key1 = {}
        key2 = {}
        val = np.array(np.zeros((len(LLH_SM)-1, 2)), dtype=np.int)
#        a={}
        for i in range(len(LLH_SM)-1):
            key1[i] = LLH_SM[i+1][0]
        for j in range(2):
            key2[j] = LLH_SM[0][j+1]
        for i in range(len(LLH_SM)-1):
            a = {}
            for j in range(2):
                val[i, j] = int(LLH_SM[i+1][j+1])
            for k in range(len(key2)):
                a[key2[k]] = val[i, k]
            SM[key1[i]] = a
#        print(TM,SM)
        return TM, SM


#    def read_od(self,xlsx_name,xls_sheet):
#        book = xlrd.open_workbook(xlsx_name)
#        table = book.sheet_by_name(xls_sheet)
#        row_Num = table.nrows
#        col_Num = table.ncols
#        od_info =[]
#        for i in range(row_Num):
#            a=table.row_values(i)
#            od_info.append(a)
#        od_demand ={}
# key =table.row_values(0)# 这是第一行数据，作为字典的key值
#        key1={}
#        a={}
#        for i in range(row_Num):
#            key1[i]=table.cell(i,0).value
#        cur_origin=table.cell(0,0).value
#        for i in range(row_Num):
#            key1[i]=table.cell(i,0).value
#            if key1[i]==cur_origin:
#                key2=table.cell(i,1).value
#                a[key2]=table.cell(i,2).value
#                od_demand[key1[i]]=a
#            else:
#                a={}
#                key2={}
#                cur_origin=table.cell(i,0).value
#                key2=table.cell(i,1).value
#                a[key2]=table.cell(i,2).value
#                od_demand[key1[i]]=a
#        return od_info,od_demand


#
#    def read_demand(self,xlsx_name,xls_sheet):
#        #打开excel表，填写路径
#        book = xlrd.open_workbook(xlsx_name)
#        #找到sheet页
#        table = book.sheet_by_name(xls_sheet)
#        #获取总行数总列数
#        row_Num = table.nrows
#        col_Num = table.ncols
#
#        s ={}
# key =table.row_values(0)# 这是第一行数据，作为字典的key值
#        key1={}
#        key2={}
#        val=np.array(np.zeros((row_Num-1,col_Num-1)))
#        a={}
#        for i in range(row_Num-1):
#            key1[i]=table.cell(i+1,0).value
#        for j in range(col_Num-1):
#            key2[j]=table.cell(0,j+1).value
#        if row_Num <= 1:
#            print("没数据")
#        else:
#            for i in range(row_Num-1):
#                 for j in range (col_Num-1):
#                     val[i,j]=table.cell(i+1,j+1).value
#                 for k in range(len(key2)):
#                     a[key2[k]]=val[i,k]
#                     s[key1[i]]=a
#        return s
#r = import_data()
##station, lane, cost_lane, cost_station, time_station, demand_point = r.set_sta_lane(2)

#od_info=r.read_od(0,0)
#tm,sm = r.set_prob()
# for i in range(len(od_info)):
#    o = od_info[i][0]
#    d = od_info[i][1]
#    print(od_flow[o][d])
# print(s[0][1])
# print(s)
# print(s[1.0][6.0])
# print(s.cell(0,0).value)

# for k,v in s.items():
#    print(k, '=', v)

# '''
# read excel and create dict like this:
#    a={('N001', 'N005'): 100.0, ('N001', 'N006'): 10.0, ('N001', 'N007'): 1.0,
#       ('N002', 'N005'): 200.0, ('N002', 'N006'): 20.0, ('N002', 'N007'): 2.0,
#       ('N003', 'N005'): 300.0, ('N003', 'N006'): 30.0, ('N003', 'N007'): 3.0,
#       ('N004', 'N005'): 400.0, ('N004', 'N006'): 40.0, ('N004', 'N007'): 4.0}
#    s['N001','N005']=100
# '''
#
#import xlrd
#import numpy as np
# class Read_Ex():
#    def read_excel(self):
#        #打开excel表，填写路径
#        book = xlrd.open_workbook("demand.xlsx")
#        #找到sheet页
#        table = book.sheet_by_name("Sheet1")
#        #获取总行数总列数
#        row_Num = table.nrows
#        col_Num = table.ncols
#
#        s ={}
# key =table.row_values(0)# 这是第一行数据，作为字典的key值
#        key1={}
#        key2={}
#        val=np.array(np.zeros((row_Num-1,col_Num-1)))
#        a={}
#        for i in range(row_Num-1):
#            key1[i]=table.cell(i+1,0).value
#        for j in range(col_Num-1):
#            key2[j]=table.cell(0,j+1).value
#        if row_Num <= 1:
#            print("没数据")
#        else:
#            for i in range(len(key1)):
#                for j in range(len(key2)):
#                    s[key1[i],key2[j]]=table.cell(i+1,j+1).value
#        return s
#r = Read_Ex()
# s=r.read_excel()
# print(s['N001','N005'])

#a = r.set_network(1)