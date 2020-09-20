from random import randint, random
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
        print("************"+_alg+":Ex_ID = "+str(Ex_ID)+"*****************")
    #    # 1. 创建文件对象
    #    f = open('"{0}{1}".format("Ex ",Ex_ID).csv','w',newline='')
    #    writer = csv.writer(f)
    #    worksheet = workbook.add_worksheet("{0}{1}".format("Ex ",Ex_ID))   #work.add_worksheet('employee')
        for run_time in range(Run_time):
            """
            # 1. the number in the random seed brace can be set arbitrable 
            # 2. random and numpy random are different packages, the seed only applies to numpy
            # 3. therefore, you should not use random package to generate random number
            # 4. I have removed it 
            # 5. By setting the seed number, you should be able to reproduce the same results under the same seed number
            """
            np.random.seed(Ex_ID + run_time + 1359)
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
    return a



if __name__ == "__main__":

    # hh.hh_main(run_ex_ID=[7, 8, 9])
    # ga.GA_main(run_ex_ID=[4])
    res_ga = run_test(run_ex_ID=[5],Run_time=1,_alg="GA")
    res_hh = run_test(run_ex_ID=[5],Run_time=1,_alg="HH")
    # print(res_ga)
    # print(res_hh)
    # sys.exit()

    best_cost_hh = []
    best_cost_ga = []
    for i in res_hh:
        best_cost_hh.append(i[1])
    for i in res_ga:
        best_cost_ga.append(i[1])

    """
    you can write more information in the summary txt
    """
    with open("Summary.txt","w") as f:
        print("AveHH:{0:.2f},Best:{1:.2f}".format(np.mean(best_cost_hh),np.min(best_cost_hh)))
        print("AveGA:{0:.2f},Best:{1:.2f}".format(np.mean(best_cost_ga),np.min(best_cost_ga)))
        print("AveHH:{0:.2f},Best:{1:.2f}".format(np.mean(best_cost_hh),np.min(best_cost_hh)),file=f)
        print("AveGA:{0:.2f},Best:{1:.2f}".format(np.mean(best_cost_ga),np.min(best_cost_ga)),file=f)
