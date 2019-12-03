class Instance:


    def __init__(self, path):
        self.number_items = 0 #Inicializa o número de items
        self.number_groups = 0 #Inicializa o número de grupos
        self.adj_matrix = [] #Matriz de diversidade
        self.group_bounds = [] #Tamanho dos grupos
        self.group_size_type = None #Tipo de tamanhos de grupos
        self.__read_instance(path)
    
    def __read_instance(self, path):
        with open(path) as f:
            try: #Tente
                params = f.readline().split()
                self.number_items = int(params[0]) #Primeiro parâmetro do arquivo - número de items totais a serem divididos
                self.number_groups = int(params[1]) #Número de grupos a serem criados
                self.group_size_type = params[2] #Grupos de tamanho homogeneos (ss) ou tamanhos variados (ds) 
            
                for i in range(3, len(params), 2): #Ler a partir de 3 até final da primeira linha de 2 em 2
                    
                    lower_bound = int(params[i]) #lower_bound do grupo - (tamanho mínimo)
                    upper_bound = int(params[i+1]) #upper_bound do grupo - (tamanho máximo)
                    
                    if self.group_size_type == 'ss' and lower_bound != upper_bound: #Aponta incoerência - ss com grupos com limites distintos
                        raise Exception("Group type is Same Size but different bounds was recieved", self.group_size_type, lower_bound, upper_bound)
                    
                    if lower_bound > upper_bound: #Aponta incoerência - mínimo maior que máximo
                        raise Exception("Lower Bound greater than Upper Bound", lower_bound, upper_bound)
                    
                    self.group_bounds.append([lower_bound, upper_bound]) #Adiciona a uma tupla a lista [lower_bound e upper_bound] dos grupos
                
                if self.number_groups != len(self.group_bounds): #Aponta incoerência no número de grupos
                    raise Exception("Number of groups and number of bounds don't match", self.number_groups, len(self.group_bounds))                

                self.adj_matrix = [[0]*self.number_items for i in range(self.number_items)] #Inicializa a matriz em zeros?? Diagonal principal??

                for line in f: #Ler as linhas das instância - i,j e dij
                    i, j, k = line.split()
                    self.adj_matrix[int(i)][int(j)] = float(k) #Preenche a matriz de forma simétrica
                    self.adj_matrix[int(j)][int(i)] = float(k)

            except Exception as e: #Deu erro!! Imprima o erro/exceção
                print(repr(e))
