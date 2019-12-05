from gurobipy import *
import time
from instance import *
import sys
import os

instancia = ""

def resolve(instance, file):
    
    try:

        model = Model("mdgp")
        model.setAttr("ModelSense", GRB.MAXIMIZE)
        X = []

        #criando variaveis para cada set
        for i in range(instance.number_items):
            x = []
            for g in range(instance.number_groups):
                x.append(model.addVar(0, 1, 0, GRB.BINARY, "x_"+str(i)+'_'+str(g)))
            X.append(x)
        #criando restricao: cada item sa pertence a no maximo um set
        Y = []
        for i in range(instance.number_items):
            y = []
            for j in range(instance.number_items):
                yl = []
                if j <= i:
                    y.append(yl)
                    continue
                for g in range(instance.number_groups):
                    yl.append(model.addVar(0,1,instance.adj_matrix[i][j]*(i<j),GRB.BINARY, 'y_'+str(i)+'_'+str(j)+'_'+str(g)))
                y.append(yl) 
            Y.append(y)    



        for i in range(instance.number_items):
            constraint = 0
            for g in range(instance.number_groups):
                constraint += X[i][g]
            model.addConstr(constraint, GRB.EQUAL, 1, "c_item_"+str(i))
        for g in range(instance.number_groups):
            constraint = 0
            for i in range(instance.number_items):
                constraint += X[i][g]
            model.addConstr(constraint, GRB.LESS_EQUAL, instance.group_bounds[g][1], 'c_group_upper_'+str(g))
            model.addConstr(constraint, GRB.GREATER_EQUAL, instance.group_bounds[g][0], 'c_group_lower_'+str(g))

        for i in range(instance.number_items):
            for j in range(instance.number_items):
                if j<=i:
                    continue
                for g in range(instance.number_groups):
                    model.addConstr(X[i][g] + X[j][g] - 1 <= Y[i][j][g])
                    model.addConstr(Y[i][j][g] <= X[i][g])
                    model.addConstr(Y[i][j][g] <= X[j][g])
        
        # for j in range(instance.number_items):
        #     for g in range(instance.number_groups):
        #         constraint = 0
        #         for i in range(instance.number_items):
        #             constraint += Y[i][j][g]
        #         model.addConstr(constraint, GRB.GREATER_EQUAL, (instance.group_bounds[g][0]-1)*X[j][g])
        #         model.addConstr(constraint, GRB.LESS_EQUAL, (instance.group_bounds[g][1]-1)*X[j][g])
                 

        # print("Optimizing...")
        # model.setParam("OutputFlag",  0)
        model.setParam("TuneOutput", 0)

        # rodar para pegar o valor da relaxacao da raiz

        model.optimize()

        # model.optimize()
        arq = open("../output.dat",'a')
        arq.write(file+"\nsolucao otima - :" + str(model.objVal)+"\n")
        arq.close()
        print(file+"\nsolucao otima - :" + str(model.objVal)+"\n")
        # for i in X:
        #     for var in i:
        #         print(var.varName, var.x)

    except GurobiError as e:
        print(e)


##Main
## python3 gurobi_model.py >&1 | tee output.dat

if __name__ == '__main__':
    # if(len(sys.argv) != 2):
    #     print("Insira uma instancia!\nExemplo: python bnb.py instancia.dat")
    #     exit(0)
    # instancia = sys.argv[1]
    # instance = Instance(instancia)
    # resolve(instance)
    path = '../data/mdgplib/'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if any(i in file for i in ['10','12','30','60','120']):#, '240', '480', '960']):
                files.append(os.path.join(r, file))

    files.sort()
    for file in files:
        instance = Instance(file)
        print(file.split('/')[-1])
        resolve(instance, file)    
