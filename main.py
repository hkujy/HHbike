from random import random
import new as new
import GA_new as ga
import csv
import sys
import new as hh
import numpy as np


def run_test(run_ex_ID, Run_time,_alg=""):
    a = []
    for c in run_ex_ID:
        Ex_ID = c
        print(_alg+":Ex_ID = "+str(Ex_ID))
    #    # 1. 创建文件对象
    #    f = open('"{0}{1}".format("Ex ",Ex_ID).csv','w',newline='')
    #    writer = csv.writer(f)
    #    worksheet = workbook.add_worksheet("{0}{1}".format("Ex ",Ex_ID))   #work.add_worksheet('employee')
        for run_time in range(Run_time):
            # the number in the random seed brace can be set arbitrable 
            np.random.seed(Ex_ID+run_time+1359)
            print("{0}:run_time = {1}".format(_alg,run_time))
            if _alg is "GA":
                result = ga.run_ga(Ex_ID)
                a.append(result)
            elif _alg is "HH":
                result = hh.run_upper(Ex_ID)
                a.append(result)
            else:
                print("Warning")
    
    f = open(_alg+'_solution.csv', 'w', newline='')
    writer = csv.writer(f)

    if _alg is "GA":
        writer.writerow(["Ex_ID", "Best_cost", "Constr_cost", "Travel_time","Best_lane", "Best_station", "Best_iter", "CPU_time", "FW_time"])
        # for i in range(len(a)):
            # writer.writerow(a[i])
    elif _alg is "HH": 
        writer.writerow(["Ex_ID", "Best_cost", "Constr_cost", "Travel_time", "Best_lane", "Best_station", "Best_iter", "CPU_time", "TM", "SM", "LO", "L1", "L2", "L3", "L4", "FW_time"])

    for i in range(len(a)):
        writer.writerow(a[i])

    f.close()



if __name__ == "__main__":

    # hh.hh_main(run_ex_ID=[7, 8, 9])
    # ga.GA_main(run_ex_ID=[4])
    run_test(run_ex_ID=[8],Run_time=10,_alg="HH")
    run_test(run_ex_ID=[8],Run_time=10,_alg="GA")
