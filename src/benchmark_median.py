"""
Creates some plots showing the improvement of using heaps in calculating the median of streaming values.
The medians of a set of streaming random integers (between 0 and 1000) is calculated with two methods
1) add value to a list and calculate the median with numpy.median; repeat
2) add value to a class that uses two heaps to more intelligently calculate the median; repeat

Three plots are created
1) Median as a function of number of random integers added
2) Cumulative run time as function of number of random integers added
3) Time to calculate the median as a function of list size (basically the np.diff of plot 2)

"""
import numpy as np
import time
import matplotlib.pyplot as plt
from helpers import MedianStreaming

### Create the dataset of random numbers ###
number_values = 10000
random_integers_list = np.random.randint(0, 1000, number_values)

### create the data structures for storing the streaming values and run times  ###
running_medians = {}
run_times = {}

for algo_name in ['no_heaps', 'with_heaps']:
    running_medians[algo_name] = np.zeros(number_values)
    run_times[algo_name] = np.zeros(number_values)


#### Calculate the median values  ###
print('Calculating median values')
# no heaps
algo_name = 'no_heaps'
current_list_of_values = []
t_start = time.time()
for i in xrange(number_values):
    # add a value to the list
    current_list_of_values.append(random_integers_list[i])
    running_medians[algo_name][i] = np.median(current_list_of_values)
    run_times[algo_name][i] = time.time()
run_times[algo_name] = run_times[algo_name] - run_times[algo_name][0]
print('Time Elapsed: %3.3f' %(time.time() - t_start))


# with class that uses heaps
algo_name = 'with_heaps'
median_streaming = MedianStreaming()
t_start = time.time()

median_old = 0
for i in xrange(number_values):
    running_medians[algo_name][i] = median_streaming.ingest(random_integers_list[i])
    run_times[algo_name][i] = time.time()
print('Time Elapsed: %3.3f' %(time.time() - t_start))

run_times[algo_name] = run_times[algo_name] - run_times[algo_name][0]

# are the running median values equal?
algo_name = 'no_heaps'
print('Are the running median values equal?: {}'.format(np.all(running_medians['no_heaps'] == running_medians['with_heaps'])))

##### Make plots and save to file #####

print('Creating and saving plots')

# 1) Median as a function of number of random integers added
plt.figure(figsize = [8,6])
plt.grid()
for algo_index, algo_name in enumerate(running_medians.keys()):
    plt.plot(running_medians[algo_name], label = algo_name, alpha = 0.4, linewidth = 2, linestyle = ['-', '--'][algo_index])
plt.ylim((0, 1000))
plt.xlabel('Number of Values')
plt.ylabel('Median Value')
plt.legend()
plt.savefig('Median_Values.png')
plt.close()

# 2) Cumulative run time as function of number of random integers added
plt.figure(figsize = [8,6])
plt.grid()
for algo_index, algo_name in enumerate(running_medians.keys()):
    plt.plot(run_times[algo_name], label = algo_name, alpha = 0.4, linewidth = 2)
plt.xlabel('Number of Values')
plt.ylabel('Total Time Elapsed (sec)')
plt.legend()
plt.savefig('Total_Time_Calculate_Median.png')
plt.close()


# 3) Time to calculate the median as a function of list size (basically the np.diff of plot 2)
plt.figure(figsize = [8,6])
plt.grid()
for algo_index, algo_name in enumerate(running_medians.keys()):
    plt.plot(np.diff(run_times[algo_name]), label = algo_name, alpha = 0.4, linewidth = 2)
plt.ylim((0, 0.002))
plt.xlabel('Number of Values')
plt.ylabel('Time to Calculate Median (sec)')
plt.legend()
plt.savefig('Time_Calculate_Median.png')
plt.close()

