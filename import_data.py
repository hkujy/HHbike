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




import xlrd
import numpy as np
from assignment.assign import *
from assignment.line import *
from assignment.graph import *
class import_data():

    def read_od(self, case_ID, demand_ID):
        if case_ID == 0:
            xlsx_name = "small.xlsx"
        if case_ID == 1:
            xlsx_name = "ND.xlsx"
        if case_ID == 2:
            xlsx_name = "SF.xlsx"

        if demand_ID == 0:
            xls_sheet = "low_demand"
        if demand_ID == 1:
            xls_sheet = "med_demand"
        if demand_ID == 2:
            xls_sheet = "high_demand"
        book = xlrd.open_workbook(xlsx_name)
        table = book.sheet_by_name(xls_sheet)
        row_Num = table.nrows
        col_Num = table.ncols
        od_info = []
        for i in range(row_Num):
            a = table.row_values(i)
            od_info.append(a)
        for i in range(len(od_info)):
            od_info[i][2] = int(od_info[i][2])

        od_demand = {}
        key1 = {}
        a = {}
        for i in range(row_Num):
            key1[i] = table.cell(i, 0).value
        cur_origin = table.cell(0, 0).value
        for i in range(row_Num):
            key1[i] = table.cell(i, 0).value
            if key1[i] == cur_origin:
                key2 = table.cell(i, 1).value
                a[key2] = int(table.cell(i, 2).value)
                od_demand[key1[i]] = a
            else:
                a = {}
                key2 = {}
                cur_origin = table.cell(i, 0).value
                key2 = table.cell(i, 1).value
                a[key2] = int(table.cell(i, 2).value)
                od_demand[key1[i]] = a
        return od_info, od_demand

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
                for ln in lines:
                    eg_b = ln.split(',')
                    nt_b.add_edge(edge_b(eg_b))
        if case_ID == 1:
            with open('bike_ND.txt', 'r') as fo:
                lines = fo.readlines()
                for ln in lines:
                    eg_b = ln.split(',')
                    nt_b.add_edge(edge_b(eg_b))
        if case_ID == 2:
            with open('bike_SF.csv', 'r') as fo:
                lines = fo.readlines()
                for ln in lines:
                    eg_b = ln.split(',')
                    nt_b.add_edge(edge_b(eg_b))

        return nt_a, nt_b

    def set_sta_lane(self, case_ID):
        if case_ID == 0:
            xlsx_name = "Small.xlsx"
        if case_ID == 1:
            xlsx_name = "ND.xlsx"
        if case_ID == 2:
            xlsx_name = "SF.xlsx"
        book = xlrd.open_workbook(xlsx_name)
        tab_lane = book.sheet_by_name("lane_cost")
        tab_station = book.sheet_by_name("station_cost")
        tab_time_station = book.sheet_by_name("time_station")
        tab_demand_point = book.sheet_by_name("demand_point")
        row_Num1 = tab_lane.nrows
        col_Num1 = tab_lane.ncols
        row_Num2 = tab_station.nrows
        col_Num2 = tab_station.ncols
        row_Num3 = tab_time_station.nrows
        col_Num3 = tab_time_station.ncols
        lane = range(0, row_Num1)
        station = range(0, row_Num2)
        demand_point = np.array(tab_demand_point.col_values(0), dtype=np.int)
        cost_lane = tab_lane.col_values(0)
        cost_station = tab_station.col_values(0)

        od_sta_info = []
        for i in range(row_Num3):
            a = tab_time_station.row_values(i)
            od_sta_info.append(a)
        time_station = {}
        key1 = {}
        a = {}
        for i in range(row_Num3):
            key1[i] = tab_time_station.cell(i, 0).value
        cur_origin = tab_time_station.cell(0, 0).value
        for i in range(row_Num3):
            key1[i] = tab_time_station.cell(i, 0).value
            if key1[i] == cur_origin:
                key2 = int(tab_time_station.cell(i, 1).value)
                a[key2] = tab_time_station.cell(i, 2).value
                time_station[key1[i]] = a
            else:
                a = {}
                key2 = {}
                cur_origin = tab_time_station.cell(i, 0).value
                key2 = int(tab_time_station.cell(i, 1).value)
                a[key2] = tab_time_station.cell(i, 2).value
                time_station[key1[i]] = a

        return station, lane, cost_lane, cost_station, time_station, demand_point

    def read_network_auto(self, nt_a, _label_lane, No_edge):
        # initialize cost_auto
        nt_a.init_cost1(_label_lane, No_edge)
        return nt_a

    def read_network_bike(self, nt_b, _label_lane, No_edge):
        # initialize cost_bike
        nt_b.init_cost2(_label_lane, No_edge)
        return nt_b

    def set_prob(self):
        book = xlrd.open_workbook("LLH.xlsx")
        # 找到sheet页
        tab_TM = book.sheet_by_name("TM")
        tab_SM = book.sheet_by_name("SM")
        row_Num1 = tab_TM.nrows
        col_Num1 = tab_TM.ncols
        row_Num2 = tab_SM.nrows
        col_Num2 = tab_SM.ncols
        TM = {}
        key1 = {}
        key2 = {}
        val = np.array(np.zeros((row_Num1-1, col_Num1-1)), dtype=np.int)
#        a={}
        for i in range(row_Num1-1):
            key1[i] = tab_TM.cell(i+1, 0).value
        for j in range(col_Num1-1):
            key2[j] = tab_TM.cell(0, j+1).value
        for i in range(row_Num1-1):
            a = {}
            for j in range(col_Num1-1):
                val[i, j] = tab_TM.cell(i+1, j+1).value
            for k in range(len(key2)):
                a[key2[k]] = val[i, k]
            TM[key1[i]] = a

        SM = {}
        key1 = {}
        key2 = {}
        val = np.array(np.zeros((row_Num2-1, col_Num2-1)), dtype=np.int)
#        a={}
        for i in range(row_Num2-1):
            key1[i] = tab_SM.cell(i+1, 0).value
        for j in range(col_Num2-1):
            key2[j] = tab_SM.cell(0, j+1).value
        for i in range(row_Num2-1):
            a = {}
            for j in range(col_Num2-1):
                val[i, j] = tab_SM.cell(i+1, j+1).value
            for k in range(len(key2)):
                a[key2[k]] = val[i, k]
            SM[key1[i]] = a
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
# od_info,od_flow=r.read_od("ND.xlsx","od_demand")
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
