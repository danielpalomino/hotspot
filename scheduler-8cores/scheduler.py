import os
import sys
import subprocess


#n_l2s = number of l2s to ignore when calculating the temperature gradients
def sgt_calc(temp_traces,sgt_th,n_l2s):
    for i in range(0,len(temp_traces)):
        max_temp = max(temp_traces[i][:-n_l2s])
        min_temp = min(temp_traces[i][:-n_l2s])
        sgt = float(max_temp) - float(min_temp)
        if sgt >= sgt_th:
            return i
    return -10 

def numeric_compare(x, y):
    if float(x[1]) - float(y[1]) > 0:
        return 1
    else:
        return -1

def numeric_compare_reverse(x, y):
    if float(x[1]) - float(y[1]) > 0:
        return -1
    else:
        return 1

#pos where the traces need to be re-scheduled
def build_new_ptraces(power_traces, temp_traces ,pos, n_l2s):
    #make sure power traces and temp traces have the same size
    assert len(power_traces) == len(temp_traces)
    
    #create 2-tuple list with traces and positions for temperature
    tuple_temp_trace = []
    t_trace = temp_traces[pos][:-n_l2s]
    for i in range(0,len(t_trace)):
        tuple_temp_trace.append([])
        tuple_temp_trace[i].append(i)
        tuple_temp_trace[i].append(t_trace[i])
    tuple_temp_trace = sorted(tuple_temp_trace,cmp=numeric_compare)
#   print tuple_temp_trace

    #create 2-tuple list with traces and positions for power
    tuple_power_trace = []
    p_trace = power_traces[pos][:-n_l2s]
    for i in range(0,len(p_trace)):
        tuple_power_trace.append([])
        tuple_power_trace[i].append(i)
        tuple_power_trace[i].append(p_trace[i])
    tuple_power_trace = sorted(tuple_power_trace,cmp=numeric_compare_reverse)
#    print tuple_power_trace

    assert len(tuple_temp_trace) == len(tuple_power_trace)

    for i in range(pos,len(power_traces)):
        p_trace = []
        #build p_trace
        for j in range(0,len(power_traces[i])):
            p_trace.append(power_traces[i][j])
        for j in range(0,len(tuple_temp_trace)):
            position_temp = tuple_temp_trace[j][0]
            position_power = tuple_power_trace[j][0]
            power_traces[i][position_power] = p_trace[position_temp]

    return power_traces

hotspot = '/home/daniel/vipg-simulator/hotspot/hotspot'
pl_grid = '/home/daniel/vipg-simulator/hotspot/grid_thermal_map.pl'
ptrace = sys.argv[1]
hotspot_config = sys.argv[2]
flp = sys.argv[3]
steady = sys.argv[1][:-6]+'steady'
grid_file = sys.argv[1][:-6]+'grid.steady'
ttrace = sys.argv[1][:-6]+'ttrace'

sgt_th = 4.0
counter = 0
pos = 1
last_pos = 1
n_l2s = 2

while(pos > 0):
    #1. RUN HOTSPOT(with current power traces)
    subprocess.call(['echo',hotspot,'-c',hotspot_config,'-f',flp,'-p',ptrace,'-steady_file',steady,'-model_type','grid','-grid_steady_file',grid_file,'-o',ttrace])
    subprocess.call([hotspot,'-c',hotspot_config,'-f',flp,'-p',ptrace,'-steady_file',steady,'-model_type','grid','-grid_steady_file',grid_file,'-o',ttrace])
    #2. READ POWER TRACES
    power_file = open(ptrace,'r')
    ##READ HEADER
    header = power_file.readline()
    power_components = header.split('\t')

    power_traces = []
    buff = power_file.readlines()
    for i in range(0,len(buff)):#power_file.readlines():
        power_traces.append([])
        traces = buff[i].split('\t')
        for trace in traces[:-1]:
            power_traces[i].append(trace)
#        print power_traces[i]
    
#    print power_traces

    #3. READ TEMPERATURE TRACES
    ttrace_file = open(ttrace,'r')
    temp_components = ttrace_file.readline().split('\t')
    temp_traces = []
    buff = ttrace_file.readlines()
    for i in range(0,len(buff)):
        temp_traces.append([])
        traces = buff[i].split('\t')
        for trace in traces:
            temp_traces[i].append(trace.split('\n')[0])

 #   print temp_traces
    #4. GET FIRST SPATIAL GRADIENT TEMPERATURE HIGHER THAN SGT_TH
    pos = sgt_calc(temp_traces,sgt_th,n_l2s)
    if(pos == last_pos):
        pos = pos + 1
    print pos
    last_pos = pos
    
    #5. IF TEMPERATURE GRADIENT EXCEEDS THRESHOLD
    if pos > 0:
        #6.     BUILD POWER TRACES BASED ON SCHEDULER TECHNIQUE
        new_power_traces = build_new_ptraces(power_traces,temp_traces,pos,n_l2s)
        #UPDATE FILES NAMES TO RE RUN HOTSPOT
        ptrace = sys.argv[1][:-7]+'_'+str(counter)+'.ptrace'
        steady = sys.argv[1][:-7]+'_'+str(counter)+'.steady'
        grid_file = sys.argv[1][:-7]+'_'+str(counter)+'.grid.steady'
        ttrace = sys.argv[1][:-7]+'_'+str(counter)+'.ttrace'
        #WRITE NEW POWER TRACES TO NEW PTRACE FILE
        new_ptrace_file = open(ptrace,'w')
        #write header to new ptrace file
        new_ptrace_file.write(header)
#        for component in power_components:
    #        new_ptrace_file.write(component + '\t')
#        new_ptrace_file.write('\n')
        #write new power traces
        for traces in new_power_traces:
            for trace in traces:
                new_ptrace_file.write(trace + '\t')
            new_ptrace_file.write('\n')

    #7.     REPEATE STEP 2
    counter = counter + 1
    
    new_ptrace_file.close()
    power_file.close()
    ttrace_file.close()

os.system('perl ' + pl_grid + ' ' + flp + ' ' + grid_file + ' 64' + ' 64' + ' 324' + ' 356' + ' > out.svg')
#subprocess.call(['perl',pl_grid,flp,grid_file,'64','64','320','350','out.svg'])
subprocess.call(['convert','-density','288','out.svg','out.png'])
