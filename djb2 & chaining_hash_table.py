#!/usr/bin/env python
# coding: utf-8

# ## Plagirism Detector


import math
class HashTableNode:
    '''
    This hash table node stores the key and value pairs.
    
    Innput:
        - key: the hash number of substring
        - value: the substring
        - index: start index in the original string
    '''
    def __init__(self, key, value,index,nextNode = None):
        self.key = key
        self.value = value
        self.indexes = []
        self.indexes.append(index)
        #Q2
        self.next = nextNode
    
class HashTable:
    '''
    This hash table uses open addressing to avoid collision. Each slot in the hashtable will only hold 1 element.
    Double Hashing is used to probe the hashtable.
    Source: Ha Nguyen and Quang Tran, “All you need to know about hashing (to build a plagiarism detector)”
    '''
    def __init__(self, m):
        #initialize the table
        self.capacity = m
        self.hash_table = [None for _ in range(m)]

    def double_hashing(self, key, i):
        #since our i keeps increasing by 1
        #we keep searching the next slot until we find an empty slot
        return (self.hash_function_1(key) + i * self.hash_function_2(key)) % self.capacity

    def hash_function_1(self, k):
        return k % self.capacity
    def hash_function_2(self, k):
        return 1 + k % (self.capacity - 1)
  
    def djb2_hash_function(self, text):
        """
        Implementation of djb2 hash algorithm that
        is popular because of it's magic constants.
        """
        hash = 5381
        for char in text:
            hash = ((hash << 5) + hash) + ord(char)
        return hash & 0xFFFFFFFF
    
    def chained_hash_insert(self, value, index):
        """
        insert nodes into chained hashtable.

        Input:
            - value: the substring's text
            - index: the substring's start index on th original string
        """
        #calculate hash key
        hashed_key = self.djb2_hash_function(value)
        #get table index to insert to
        hIndex = hashed_key % self.capacity
        
        #create the node to store our key and value
        node = HashTableNode(hashed_key, value, index)
        
        #if a node already exist
        if self.hash_table[hIndex] is not None:
            #go down the list to add node at the end
            cur = self.hash_table[hIndex]
            while cur is not None:     
                if cur.value == value:
                    #if there is duplicates, register
                    cur.indexes.append(index)
                    return
                if cur.next is None:
                    #if end of chain is reached, append
                    cur.next = node
                    return
                cur = cur.next
     
        #if the spot is empty
        self.hash_table[hIndex] = node
        
    def chained_hash_search(self, value):
        #find the key after hashing
        hashed_key = self.djb2_hash_function(value)
        #get table index to look for
        hIndex = hashed_key % self.capacity
        
        #start traversing from this node
        cur = self.hash_table[hIndex]
        #traversing the list to find the value
        while cur is not None:
            if cur.value == value:
                return cur.indexes
            cur = cur.next
        return False

# djb2 Hashing & Chaining 

# I choose the chaining method to avoid colluision and djb2 hash function.
# The djb2 hash function is chosen because it is known for distributing keys more evenly than other hash function("Hash Functions",2021).


def chained_table_size(strL):
    """
    Finds the appropriate table size for a given length of strings for the djb2 function. 
    The table size is bigger than the string length for more evenly distribution of space(less colluisions) 
    and should be a power of 2 for eaiser bitsize operations
    
    Input:
        - strL: length of string
    Output:
        - q: table size
    """  
    #return 2 if it's smaller string length
    if strL <= 2:
        return strL

    #find the next power of 2 bigger than string length
    q = strL
    while True:
        #if log2(q) is a integer
        if math.ceil(math.log(q, 2)) == math.floor(math.log(q, 2)):
            return q
        q += 1
    
def regular_get_match(x, y, k):
    '''
    Finds all common length-k substrings of x and y
    NOT using rolling hashing on both strings.
    
    Input:
        - x, y: strings
        - k: int, length of substring
    Output:
        - A list of tuples (i, j)
          where x[i:i+k] = y[j:j+k]
    '''
    #process strings
    x, y = process_string(x,y)
    
    #calculate hash table length
    size = chained_table_size(len(x))
    
    #create hash table
    hTable2 = HashTable(size)
    
    #insert all length-k substrings of x
    for i in range(len(x)-k+1):
        hTable2.chained_hash_insert(x[i:i+k],i)
        
    #duplicate list
    dup = []
    
    #the print_table function has been commented and its output for text case 1 is shown below.
    #UNCOMMENT THIS if you want to print contents in table
    #print_table(hTable2)
        
    #search all length-k substrings of y
    for j in range(len(y)-k+1):
        xIndex = hTable2.chained_hash_search(y[j:j+k])
        #if duplicates found
        if xIndex:
            for i in xIndex:
                dup.append((i,j))
    return dup


def print_table(table):
    '''
    Print out the hash table. Optional function. UNCOMMENT in regular_get_string
    
    Input:
        - table: hash table with sub-strings inserted
    '''
    index = 0
    for curNode in table.hash_table:
        #if node exist
        if curNode is not None:
            if curNode.next is None:
                #print information of node
                print("index:",index, "| text =",curNode.value, "| index in original string = ",
                      curNode.indexes)
            while curNode.next is not None:
                print("index:",index, "| text =",curNode.value, "| index in original string = ",
                  curNode.indexes, "| next node = ", curNode.next.value)
                curNode = curNode.next
        #visit next indx
        index += 1
    
regular_get_match("Today is Monday", "day", 3)


# - Take our first test case as the example(table output shown above). "Today is Monday" and "day" will be first processed into "todayismonday" and "day". Then, a hash table will be created. Every len-3 substrings will be inserted into the hash table, from "tod", "oda",...,"day". 
# - For each substring, a node will be created to store its text, integer value of text and duplicate substrings' index in the original string. In each insertion, the substring's hash value will be calculated by the djb2 function; the hash value will be mod by the table size to insure the insertion index does not exceed the table size. 
# - If a node is already present, the node will be inserted into the index chain and the previous node will mark the current node as its next node. For example, "ayi" and "nda" has index as 8, and "nda" is chained next to "ayi". 
# - If the same substring is already inserted, the index of substring in the orginal string will be registered in the same node. For example, when the second "day" is inserted, its index in original string (10) is added to the node that hold "day" as text value.
# - Upon searching, the substrings will be created and its hash value will be calculated. If a node with same text is found in the index chain, the function will append the all of its index in the original string to the return value. In our example, "day" in y-string match the "day" node; then, 2 and 10 is appended to the output.


#test duplicates handling
assert(regular_get_match("Today is Monday", "day", 3)) == [(2, 0), (10, 0)]

#test blank space, capitlized letters, and special characters
assert(regular_get_match("Ha HA hA h.Apple ", "ha", 2)) == [(0,0), (2, 0), (4, 0)]

#test real-life plagism examples(Direct Plagiarism, 2021)
text = "Normal science, the activity in which most scientists inevitably spend almost all their time,         is predicated on the assumption that the scientific community knows what the world is like."
assert(regular_get_match(text, text, 10)) == [(i,i) for i in range(148)]



#run the input from our presentation in the last session (shown in Figure 1)
text1 = "The legal system is made up of civil courts, criminal courts and specialty courts, such as family law         courts and bankruptcy courts. Each court has its own jurisdiction, which refers to the cases that the         court is allowed to hear. In some instances, a case can only be heard in one type of court."
text2 = "The legal system is made up of criminal and civil courts and specialty courts like  bankruptcy courts         and family law courts. Each court is vested with its own jurisdiction. Jurisdiction refers to the types         of cases the court is permitted to rule on. Sometimes, only one type of court can hear a particular case."
print(regular_get_match(text1, text2, 8))


# "Hash Functions". (2021). York University CSE. Retrieved from http://www.cse.yorku.ca/~oz/hash.html
