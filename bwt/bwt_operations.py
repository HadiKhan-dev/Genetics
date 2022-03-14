"""
Code for computing the original string given a BWT of a text and FM indices 
on that text, as well for finding exact matches of a test string inside the 
text efficiently 
"""


from bwt import bwt,chars_and_occurences_to_dict,create_count_tables,suffix_sampling


def count_times(char,position,bwt_string,count_tables,gap_size):
    """
    Return the number of times char has appeared up to (but not including) a 
    given position in the bwt_string, gap_size is the size of the gap in the
    elements of count_tables
    """

    lower = (position//gap_size)*gap_size
    return count_tables[char][lower]+bwt_string[lower:position].count(char)    
    
def LF(char,position,bwt_string,occ,count_tables,gap_size):
    """
    Returns the rank ordering of a letter and position in the BWT to where
    it is would be in the sorted array of characters
    """
    return occ[char]+count_times(char,position,bwt_string,count_tables,gap_size)
    
    
def get_orig_string(bwt_string,occ,count_tables,gap_size):
    """
    Returns the original string given a BWT of the string, and a dictionary of 
    how many lower occuring characters there are for each element which may 
    appear in the string as well as a dictionary of count_tables (FM index) of 
    the string
    """
    cur_pos = 0
    stri = "$"
    cur_sym = bwt_string[0]
    i = 0
    
    while cur_sym != "$":
        next_val = LF(cur_sym,cur_pos,bwt_string,occ,count_tables,gap_size)
        stri = cur_sym+stri
        cur_pos = next_val
        cur_sym = bwt_string[cur_pos]
        i += 1
    return stri


def exact_locate(position,bwt_string,occ,count_tables,gap_size,suff):
    """
    Locates the exact position in the text string a position in the bwt
    corresponds to given a uniform sampling of the suffix array.
    """
    cur_pos = position
    cur_sym = bwt_string[position]
    back_move = 0
    while cur_pos not in suff[0]:
        next_val = LF(cur_sym,cur_pos,bwt_string,occ,count_tables,gap_size)
        back_move += 1
        cur_pos = next_val
        cur_sym = bwt_string[cur_pos]
    return back_move+suff[1][cur_pos]

    
def find_matchings(test,bwt_string,occ,count_tables,gap_size,suff):
    """
    Finds the locations of the exact matches of a test string in a text given 
    the BWT of the text and a uniform sampling of the suffix array. Runs in 
    time proportional to the length of the test string
    """
    low = 0
    up = len(bwt_string)
    rev = test[::-1]
    for i in range(len(rev)):
        cur_let = rev[i]
        low = LF(cur_let,low,bwt_string,occ,count_tables,gap_size)
        up = LF(cur_let,up,bwt_string,occ,count_tables,gap_size)
    
    locations = []
    for i in range(low,up):
        corr_location = exact_locate(i,bwt_string,occ,count_tables,gap_size,suff)
        locations.append(corr_location)
    return sorted(locations)
    

