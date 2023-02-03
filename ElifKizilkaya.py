import sys
import random
import time
import threading
import resource
import copy
sys.setrecursionlimit(1000000)
resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])





def listmaker(input_type, n):
    listi = []
    
    if input_type == 1:
        multiplier = 10
    elif input_type == 2:
        multiplier = 0.75
    elif input_type == 3:
        multiplier = 0.25

    if input_type == 4: # all elements are 1
        for x in range(n):
            listi.append(1)
    else: # input type is 1,2 or 3
        for x in range(n):
            listi.append(random.randint(1,int(multiplier*n))) #elements are between 1 to 0.25*n, 0.75*n or 10*n
    return listi

def interchange(input_list, right, left):
	temp = input_list[right]
	input_list[right] = input_list[left]
	input_list[left] = temp



def rearrange_13(input_list, low, high): #list[low:high], for quicksort 1 and 3
    right = low
    left = high #size-1
    x = input_list[low] #pivot
    position = 0
    
    while True :
        while x > input_list[right]:
            right = right + 1
        
        while x < input_list[left]:
            left = left - 1
            
        if right >= left:
            position = left
            return position
            
        interchange(input_list,right,left)
        
        right = right + 1
        left = left - 1
        



def rearrange_2(input_list, low, high): #list[low:high], for quicksort 2
	right = low
	left = high #size-1
	index = random.randint(low, high)
	x = input_list[index] #pivot
	position = 0
	while True :
		while x > input_list[right]:
		 	right = right + 1
		while x < input_list[left]:
		 	left = left - 1
		
		if right >= left:
			position = left
			return position
		interchange(input_list,right,left)
		
		right = right + 1
		left = left - 1


def rearrange_4(input_list, low, high): #list[low:high], for quicksort 4
	right = low
	left = high #size-1
	index = median_of_3(input_list, low, high)
	x = input_list[index] #pivot
	position = 0
	while True :
		while x > input_list[right]:
		 	right = right + 1
		while x < input_list[left]:
		 	left = left - 1
		
		if right >= left:
			position = left
			return position
		interchange(input_list,right,left)
		
		right = right + 1
		left = left - 1

def shuffle(list):
	for i in range(0,len(list)-2):
		index = random.randint(i, len(list)-1)
		interchange(list, i, index)


def median_of_3(input_list, low, high):
	rightmost = input_list[high]
	leftmost = input_list[low]
	mid_index = (low + high)//2
	middle = input_list[mid_index]
	if rightmost >= leftmost and rightmost <= middle: #l r m , l m r
		input_list[high], input_list[mid_index] = input_list[mid_index], input_list[high]
		return high
	elif rightmost >= middle and rightmost <= leftmost: #m r l, l m r
		temp = input_list[low]
		input_list[low] = input_list[mid_index]
		input_list[mid_index] = input_list[high]
		input_list[high] =  temp
		return high
	elif leftmost >= rightmost and leftmost <= middle: # r l m, l m r
		temp = input_list[low]
		temp2 = input_list[mid_index]
		input_list[low] = input_list[high]
		input_list[mid_index] = temp
		input_list[high] =  temp2
		return low
	elif leftmost >= middle and leftmost <= rightmost:# m l r, l m r
		temp = input_list[low]
		input_list[low] = input_list[mid_index]
		input_list[mid_index] = temp
		return low
	elif middle >= leftmost and middle <= rightmost:# l m r, l m r
		return mid_index
	elif middle >= rightmost and middle <= leftmost:# r m l, l m r
		input_list[low], input_list[high] = input_list[high], input_list[low]
		return mid_index


def quicksort(input_list,low,high, quicksort_version):

    if high > low:
        if quicksort_version in [1, 3]:
            position = rearrange_13(input_list,low, high)
        elif quicksort_version == 2:
            position = rearrange_2(input_list,low, high)
        else:
            position = rearrange_4(input_list,low, high)
            
        quicksort(input_list, low, position, quicksort_version)
        quicksort(input_list, position+1, high, quicksort_version)

	

def call_function(input_type, quicksort_version, listt):

    total_exec_time = 0
    for i in range(5):
        if quicksort_version == 3:
            shuffle(listt[i])
        start = time.time()
        quicksort(listt[i], 0, len(listt[i])-1, quicksort_version)
        end = time.time()
        exec_time = end - start
        total_exec_time += exec_time
    avrg_exec_time = total_exec_time / 5

    
    listt[5].sort() # 2 is for worst case

    if quicksort_version == 3:
        shuffle(listt[5])
    start = time.time()
    quicksort(listt[5], 0, len(listt[5])-1, quicksort_version)

    end = time.time()
    worst_exec_time = end - start
    return avrg_exec_time, worst_exec_time






ns = [100, 1000, 10000]
quicksort_versions = [1, 2, 3, 4]
input_types = [1, 2, 3, 4]
case_type = [1, 2]




for n in ns:
    for input_type in input_types:
        l = [listmaker(input_type, n) for i in range(6)] 
        f = open(f"list_size{n}_type{input_type}", "w+")
        for ll in l:
        	f.write(str(ll))
        	f.write("\n")
        f.close()
        for quicksort_version in quicksort_versions:	
            exec_times = call_function(input_type, quicksort_version,copy.deepcopy(l))
            print("Input type: ", input_type, " Quicksort Version: ", quicksort_version, " n: ", n, " Average time:", exec_times[0], " Worst time: ", exec_times[1] )
     

