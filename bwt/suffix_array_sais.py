"""
Code for computing the suffix array of a string using Nong et al.'s 2008 
induced sorting algorithm
"""

def induced_sort(data,type_list,index_list,initial_positions):
    """
    Runs one round of the induced sorting algorithm to compute the 
    suffix array
    """
    
    final_list = [-1 for i in range(len(data))]
    max_char = max(data)
    fillings = {i:[] for i in range(max_char+1)}
    for i in range(len(initial_positions)):
        v = data[initial_positions[i]]
        fillings[v].append(initial_positions[i])
    
    for i in range(max_char+1):
        if i == max_char:
            end = len(data)-1
        else:
            end = index_list[i+1]-1
        ins = fillings[i]
        final_list[end-len(ins)+1:end+1] = ins 
        
    forward_copy_list = index_list.copy()

    for i in range(len(data)):
        if final_list[i] != -1 and final_list[i] != 0 and type_list[final_list[i]-1] == 1:
            to_add = final_list[i]-1
            char_at_to_add = data[to_add]
            position = forward_copy_list[char_at_to_add]
            final_list[position] = to_add
            forward_copy_list[char_at_to_add] += 1
    for i in range(len(data)):
        if final_list[i] == -1:
            continue
        elif type_list[final_list[i]] == 0:
            final_list[i] = -1
            
    backward_copy_list = index_list.copy()[1:]+[len(data)]
    backward_copy_list = [backward_copy_list[i]-1 for i in range(max_char+1)]
    
    for i in range(len(data)-1,-1,-1):
        if final_list[i] != -1 and final_list[i] != 0 and type_list[final_list[i]-1] == 0:
            to_add = final_list[i]-1
            char_at_to_add = data[to_add]
            position = backward_copy_list[char_at_to_add]
            final_list[position] = to_add
            backward_copy_list[char_at_to_add] -= 1
    final_list[0] = len(data)-1
    
    return final_list

def sais_numeric(data):
    """
    Computes the suffix array on a numerical list of data where the characters
    are integers denoting their relative order
    """
    
    max_char = max(data)
    type_list = [-1]*len(data)
    char_count_list = [0]*(max_char+1)
    index_list = [0]*(max_char+1)

    for i in range(len(data)-1,-1,-1):
        char_count_list[data[i]] += 1
        
        if i == len(data)-1:
            type_list[i] = 0
        else:
            if data[i] == data[i+1]:
                type_list[i] = type_list[i+1]
            elif data[i] > data[i+1]:
                type_list[i] = 1
            else:
                type_list[i] = 0
        
    for i in range(1,max_char+1):
        index_list[i] = index_list[i-1]+char_count_list[i-1]
        
    lms_block_induce_list = [-1 for i in range(len(data))]
    lms_starts = []
    lms_ends = {}
    
    for i in range(1,len(data)):
        if type_list[i] == 0 and type_list[i-1] == 1:
            lms_starts.append(i)
                
    for i in range(len(lms_starts)-1):
        lms_ends[lms_starts[i]] = lms_starts[i+1]
        
    lms_ends[lms_starts[-1]] = len(data)
    lms_block_induce_list = induced_sort(data,type_list,index_list,lms_starts)
    lms_set = set(lms_starts)
    lms_only_string = []
    
    for i in range(len(lms_block_induce_list)):
        if lms_block_induce_list[i] in lms_set:
            lms_only_string.append(lms_block_induce_list[i])
    
    reduced_namings = {}
    cur_name = 0
    reduced_namings[lms_only_string[0]] = 0
    
    for i in range(1,len(lms_only_string)):
        
        cur_consider = lms_only_string[i]
        prev_consider = lms_only_string[i-1]
        
        cur_lms = data[cur_consider:lms_ends[cur_consider]]
        prev_lms = data[prev_consider:lms_ends[prev_consider]]
        
        if cur_lms != prev_lms:
            cur_name += 1
        reduced_namings[lms_only_string[i]] = cur_name

    reduced_string = list(map(lambda x: reduced_namings[x],lms_starts))
    
    if max(reduced_string) == len(reduced_string)-1:
        reduced_string_suffix_array = [-1]*len(reduced_string)
        for i in range(len(reduced_string)):
            reduced_string_suffix_array[reduced_string[i]] = i
    else:        
        reduced_string_suffix_array = sais_numeric(reduced_string)[0]
    
    lms_sorted = [lms_starts[reduced_string_suffix_array[i]] for i in range(len(lms_starts))]
    
    return (induced_sort(data,type_list,index_list,lms_sorted),index_list)
    

def sais(input_string):
    """
    Constructs the suffix array of the input string via induced sorting
    """
    letter_dict = {"$":0}
    split = list(input_string)
    list_chars = sorted(list(set(split)))
    
    for i in range(len(list_chars)):
        letter_dict[list_chars[i]] = i+1

    num_string = list(map(lambda x: letter_dict[x],split))+[0]

    return sais_numeric(num_string)