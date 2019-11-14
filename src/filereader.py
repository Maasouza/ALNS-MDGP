
def readInstance(file):
    #Talvez substituir por um dict de (i,j) : diversidade
    a = []
    groupBounds = []
    n = None
    g = None
    groupSizeType = None

    with open(file) as f:
        try:

            params = f.readline().split()
            n = int(params[0])
            g =  int(params[1]) 
            groupSizeType = params[2]
           
            for i in range(3, len(params), 2):
                
                lowerBound = int(params[i])
                upperBound = int(params[i+1])
                
                if(groupSizeType=='ss' and lowerBound != upperBound):
                    raise Exception("Group type is Same Size but different bounds was recieved", groupSizeType, lowerBound, upperBound)
                

                if(lowerBound > upperBound):
                    raise Exception("Lower Bound greater than Upper Bound", lowerBound, upperBound)
                
                groupBounds.append([lowerBound, upperBound])
            
            if(g != len(groupBounds)):
                raise Exception("Number of groups and number of bounds don't match", g, len(groupBounds))                

            a = [[0]*n for i in range(n)]

            for line in f:
                i, j, k = line.split()
                a[int(i)][int(j)] = float(k)
                a[int(j)][int(i)] = float(k)

        except Exception as e:
            print(repr(e))

    return  a, n, g, groupSizeType, groupBounds