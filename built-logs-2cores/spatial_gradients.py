import sys

SIZE = 64
#read grid file (64x64)
grid_file = open(sys.argv[1],'r')

#initialize matrix of grid
grid = []
for i in range(0,SIZE):
    grid.append([])

#read grid from file
for i in range(0,SIZE):
    for j in range(0,SIZE):
        #get line
        line = grid_file.readline()
        #get tokens "line_number temp_stat"
        tokens = line.split('\t')
        #get token "temp_stat"
        grid[i].append(tokens[1][:-1])
    #read empty line
    grid_file.readline()

print grid
#calculate spatial gradients (HOW?)
