class Instance:
    number_itens = 0
    number_groups = 0
    adj_matrix = []
    group_bounds = []
    group_size_type = None

    def __init__(self, path):
        self.__read_instance(path)
    
    def __read_instance(self, path):
        with open(path) as f:
            try:
                params = f.readline().split()
                self.number_itens = int(params[0])
                self.number_groups = int(params[1]) 
                self.group_size_type = params[2]
            
                for i in range(3, len(params), 2):
                    
                    lower_bound = int(params[i])
                    upper_bound = int(params[i+1])
                    
                    if self.group_size_type == 'ss' and lower_bound != upper_bound:
                        raise Exception("Group type is Same Size but different bounds was recieved", self.group_size_type, lower_bound, upper_bound)
                    
                    if lower_bound > upper_bound:
                        raise Exception("Lower Bound greater than Upper Bound", lower_bound, upper_bound)
                    
                    self.group_bounds.append([lower_bound, upper_bound])
                
                if self.number_groups != len(self.group_bounds):
                    raise Exception("Number of groups and number of bounds don't match", self.number_groups, len(self.group_bounds))                

                self.adj_matrix = [[0]*self.number_itens for i in range(self.number_itens)]

                for line in f:
                    i, j, k = line.split()
                    self.adj_matrix[int(i)][int(j)] = float(k)
                    self.adj_matrix[int(j)][int(i)] = float(k)

            except Exception as e:
                print(repr(e))

if __name__ == "__main__":
    instance = Instance('../data/mdgplib/Geo/Geo_n010_ds_01.txt')
    print(instance.number_itens, instance.number_groups)