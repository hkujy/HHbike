"""
    you should use on set exp id file instead of using two copies in GA and HH
"""

def set_Ex_ID(Ex_ID,_alg=""):
    # initialize the output first
    case_ID = -1
    demand_ID = -1
    Budget = -1
    fy = -1
    sita = -1
    UE_converge = 10000000
    isOutPutDetail = True
    Max_gen = -1
    pop_size = -1
    cross_p = -1
    mutation_p = -1
 
    if Ex_ID == 0:
        case_ID = 0
        demand_ID = 1
        Budget = 10000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True

        if _alg is "HH":
            Max_gen = 300
        elif _alg is "GA":
            Max_gen = 30
            pop_size = 10
            cross_p = 0.9
            mutation_p = 0.3
        else:
            print("Warning: exp id = 0, set _alg")
 

    if Ex_ID == 1:
        case_ID = 1
        demand_ID = 0
        Budget = 10000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True

        if _alg is "HH":
            Max_gen = 100
        elif _alg is "GA":
            Max_gen = 10
            pop_size = 10
            cross_p = 0.9
            mutation_p = 0.3
        else:
            print("Warning")
 
    if Ex_ID == 2:
        case_ID = 1
        demand_ID = 1
        Budget = 10000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True

        if _alg is "HH":
            Max_gen = 200
        elif _alg is "GA":
            Max_gen = 20
            pop_size = 10      
            cross_p = 0.9
            mutation_p = 0.3
        else:
            print("Warning")
        
   
    if Ex_ID == 3:
        case_ID = 1
        demand_ID = 2
        Budget = 10000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True
        
        if _alg is "HH":
            Max_gen = 400
        elif _alg is "GA":
            Max_gen = 40
            pop_size = 10 
            cross_p = 0.9
            mutation_p = 0.3
        else:
            print("Warning")
 
    if Ex_ID == 4:
        case_ID = 2
        demand_ID = 0
        Budget = 100000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True

        if _alg is "HH":
            Max_gen = 1000
        elif _alg is "GA":
            Max_gen = 50
            pop_size = 20 
            cross_p = 0.9
            mutation_p = 0.3
        else: 
            print("warning")

    if Ex_ID == 5:
        case_ID = 2
        demand_ID = 1
        Budget = 100000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True

        if _alg is "HH":
            Max_gen = 1500
        elif _alg is "GA":
            Max_gen = 75
            pop_size = 20 
            cross_p = 0.9
            mutation_p = 0.3
        else:
            print("Warning")

    if Ex_ID == 6:
        case_ID = 2
        demand_ID = 2
        Budget = 100000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True
        
        if _alg is "HH":
            Max_gen = 2000
        elif _alg is "GA":
            Max_gen = 100
            pop_size = 20 
            cross_p = 0.9
            mutation_p = 0.3
        else:
            print("Warning")

 

    if Ex_ID == 7:
        case_ID = 0
        demand_ID = 0
        Budget = 10000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True

        if _alg is "HH":        
            Max_gen = 100
        elif _alg is "GA":
            Max_gen = 10
            pop_size = 10 
            cross_p = 0.9
            mutation_p = 0.3
        else:
            print("Warning")
 

    if Ex_ID == 8:
        case_ID = 0
        demand_ID = 1
        Budget = 10000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True

        if _alg is "HH":
            Max_gen = 120
        elif _alg is "GA":
            Max_gen = 12
            pop_size = 10 
            cross_p = 0.9
            mutation_p = 0.3
        else:
            print("Warning")
  
    if Ex_ID == 9:
        case_ID = 0
        demand_ID = 2
        Budget = 10000000000

        fy = 2.5
        sita = 1
        UE_converge = 0.001
        isOutPutDetail = True

        if _alg is "HH":
            Max_gen = 150
        elif _alg is "GA":
            Max_gen = 15
            pop_size = 10 
            cross_p = 0.9
            mutation_p = 0.3
 

    # UE_converge = 0.001
    if _alg is "HH":
        return case_ID, demand_ID, Budget, fy, sita, UE_converge, isOutPutDetail, Max_gen
    elif _alg is "GA":
        return case_ID,demand_ID,Budget,fy,sita,UE_converge,isOutPutDetail,Max_gen, cross_p,mutation_p, pop_size
    else:
        print("Warning")
        
   

