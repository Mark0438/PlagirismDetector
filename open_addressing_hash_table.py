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
    
    def open_addressing_insert(self, key, value, index): 
        i=0
        while i < self.capacity:
            j = self.double_hashing(key, i)
            #if we find an empty slot
            if self.hash_table[j] is None:
                #we insert the key-value pair into the hash table
                self.hash_table[j] = HashTableNode(key, value, index)
                return
            #if already registared, record it in the index list 
            if self.hash_table[j].value == value:
                self.hash_table[j].indexes.append(index)
                return
            #else we increase i and continue probing
            i += 1
        raise Exception("All slots in hash table is filled!")
        
    def open_addressing_search(self, key, value): 
        i=0
        while i < self.capacity:
          #we go through all slots
            j = self.double_hashing(key, i)
            if self.hash_table[j] is None:
                #until we find an empty one, which means the value doesn't exist
                return False
            if self.hash_table[j].key == key and value == self.hash_table[j].value:
                #or we find the value itself          
                return self.hash_table[j].indexes
            i += 1
        return False
 


# ## Double Hashing & Rolling Hashing 

# - I choose the double hashing in open adressing method to avoid colluision. 
# - In the Rolling Hashing technique, I choose q to be 10, which is consistant with the example provided in "All you need to know about hashing (to build a plagiarism detector)"(Nguyen & Tran, 2021). 
# - For the hash table size, I choose it to be a prime number bigger than 1.3 times the maximum keys to be inserted in the table because it is considered a general "rule of thumb"("Hash table size", 2021). The rolling_table_size function will calculate the hash table. 

def process_string(x,y):
    """
    get rid of the blank space in string x and y and lowercase all letters
    
    Input:
        - x, y: strings
    Output: 
        - x1, y1: processed string with no blank space and all letters lowercased.
    """
    #check empty string
    if x == None:
        raise Exception("String X cannot be empty!")
    
    #x1, y1 will hold the processed strings
    x1 = ""
    y1 = ""
    
    x1 = x.replace(" ", "")
    y1 = y.replace(" ", "")
            
    #lowercase the letters
    x1 = x1.lower()
    y1 = y1.lower()
    
    return x1, y1

def str_to_int(sub):
    """
    This function will convert a substring into integer value.
    
    Input:
        - sub: strings
    Output:
        - num: the integer that substring is converted to
    """
    num = 0
    base = 7
    k = len(sub)
    
    #loop through each character
    for i in range(k):
        #the exponent
        exp = k-1-i
        #repeatly add 
        num += ord(sub[i]) * base ** exp

    return num

def _hash(sub):
    """
    This function will produce hash value for each sub_string.
    
    Input:
        - sub: sub string to be converted
    Output:
        - hash value
    """    
    #convert to interger
    num = str_to_int(sub)
    
    #produce hash value
    hashVal = num % 10
    
    return hashVal
    
def rolling_hashing(x,k):
    """
    This function will produce hash value for every k-length substring using rolling hashing technique
    
    Input:
        - x: strings
        - k: length of substring 
    Output:
        - a list of hash values of each substring
    """
    #list to store substrings
    hashVal = []
    
    #number of substrings
    numOfSub = len(x)-k+1
    base = 7
    
    #calculate the hash value of first substring
    sub1 = x[0:k]
    sub1Hash = _hash(sub1)
    hashVal.append(sub1Hash)
    
    #start the rolling hashing from kth character
    tempSub = sub1
    tempHash = sub1Hash
    for char in x[k:]:
        #append one character at the end and calculate the hash value
        tempHash = (tempHash * base + str_to_int(char)) % 10
        #remove one character from the front and calculate the current hash value
        currentHash = (tempHash - str_to_int(tempSub[0])*(base**k%10))% 10
        hashVal.append(currentHash)
        #update tempHash and tempSub
        tempSub = tempSub[1:] + char
        tempHash = currentHash
    
    return hashVal 

def rolling_table_size(keyNum):
    """
    Finds the appropriate table size for a given length of strings. The table size should be around 1.3 times
    the number of keys in the table and it should be a prime number.
    
    Input:
        - l: length of string
    Output:
        - q: table size
    """
    #minimum length
    minL = int(keyNum * 1.3)
    
    #return minimum length if it's smaller than 3
    if minL <= 3:
        return minL

    #find the next prime number bigger than minimum length
    q = minL
    while True:
        for i in range(2,q//2):
            #if not prime number
            if q % i == 0:
                q += 1
                continue
        return q

def rh_get_match(x, y, k):
    """
    Finds all common length-k substrings of x and y
    using rolling hashing on strings.
    Input:
        - x, y: strings
        - k: int, length of substring
    Output:
        - A list of tuples (i, j) where x[i:i+k] = y[j:j+k]
    """
    #process strings
    x, y = process_string(x,y)
    
    #calculate hash table length
    keyNum = len(x) - k + 1
    size = rolling_table_size(keyNum)
    
    #create hash table
    hTable1 = HashTable(size)
    
    #hash every substring
    hashVal = rolling_hashing(x,k)
    
    #append substring in the table
    for i in range(len(hashVal)):
        hTable1.open_addressing_insert(hashVal[i], x[i:i+k], i)

    #duplicate list
    dup = []
    
    #search duplicate substring from y
    for j in range(len(y)-k+1):
        currentSub = y[j:j+k]
        #if duplicate sub_string is found, search will return the duplicate substrings index list
        indexes = hTable1.open_addressing_search(_hash(currentSub), currentSub)
        if indexes:
            for i in indexes:
                dup.append((i,j))      
    return dup


#test cases

#test duplicates handling
assert(rh_get_match("Today is Monday", "day", 3)) == [(2, 0), (10, 0)]

#test blank space, capitlized letters, and special characters
assert(rh_get_match("Ha HA hA h.Apple ", "ha", 2)) == [(0,0), (2, 0), (4, 0)]

#test real-life plagism examples(Direct Plagiarism, 2021)
text = "Normal science, the activity in which most scientists inevitably spend almost all their time,         is predicated on the assumption that the scientific community knows what the world is like."
assert(rh_get_match(text, text, 10)) == [(i,i) for i in range(148)]
 


# Nguyen, H., Tran, Q. (2021). “All you need to know about hashing (to build a plagiarism detector)". Minerva University.
# 
# 
# "Hash Table Size". (2021). University of California, San Diego CSE Department. Retrieved from https://cseweb.ucsd.edu/~kube/cls/100/Lectures/lec16/lec16-8.html
# 
# Direct Plagiarism. (2021). Academic tutorials. NORTHERN ILLINOIS UNIVERSITY. Retrieved from https://www.niu.edu/academic-integrity/faculty/committing/examples/direct-plagiarism.shtml

