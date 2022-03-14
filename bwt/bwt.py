"""
Code for computing the Burrows-Wheeler Transform of a string and for building
the FM-indices (Full Text, Minute Size) over it
"""

from suffix_array_sais import sais

def get_last(data,posit):
    """
    Helper for the bwt function below
    """
    if posit != -1:
        return data[posit]
    else:
        return "$"
    
def bwt(data):
    """
    Returns the BWT of a string as well as the full suffix array and the number
    of occurences of lower ranked characters for each character in the string
    """
    suff = sais(data)
    fin_array = [get_last(data,suff[0][i]-1) for i in range(len(data)+1)]
    
    return (fin_array,suff[0],suff[1])

def chars_and_occurences_to_dict(chars,occurences):
    """
    Combines a sorted list of characters and the occurences of lexicographically
    lower characters into a dictionary
    """
    final = {}
    
    for i in range(len(chars)):
        final[chars[i]] = occurences[i]
        
    return final


def create_count_tables(bwt_string,letters,gap_size):
    """
    Creates the count tables from a BWT string, a list of letters which may
    appear in the string and a gap size
    """
    final = {char:{0:0} for char in letters}
    str_len = len(bwt_string)
    cur_pos = 1
    cur_checkpoint = 0
    cur_counts = {char:0 for char in letters}
    while cur_pos < str_len+1:
        cur_char = bwt_string[cur_pos-1]
        cur_counts[cur_char] += 1
        if cur_pos % gap_size == 0:
            for let in letters:
                final[let][cur_pos] = final[let][cur_checkpoint]+cur_counts[let]
            cur_counts = {char:0 for char in letters}
            cur_checkpoint = cur_pos
        cur_pos += 1
    return final

def suffix_sampling(suff_array,gap_size):
    """
    Samples the suffix array to create a dictionary containing the locations 
    of every lexicographically sorted gap_size^th suffix.
    Returns a tuple containing a set of all elements which are keys in the 
    final sampled dictionary and the dictionary itself
    """
    fin_dict = {}
    fin_set = set([])
    for i in range(len(suff_array)):
        if suff_array[i] % gap_size == 0:
            fin_dict[i] = suff_array[i]
            fin_set.add(i)
    return (fin_set,fin_dict)

