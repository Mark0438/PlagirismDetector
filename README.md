# Plagirism Detector
The Plagirism Dectector detect duplicate substrings in two strings. It can identify and return the start index of duplicate substrings in both strings. Although as the input string length increases, the output becomes long and hard to track manually, the functions provided robust, back-end groundwork for us to build a more intuitive plagiarism interface upon. For example, we can add a function that highlights the duplicate substrings based on the returned indexes. 

<img width="831" alt="Screenshot 2023-11-16 at 7 05 07 PM" src="https://github.com/extraordinary-yh/plagirism-detector/assets/49523649/645b86eb-915d-49ee-a6b2-436ae7ac1c8a">

## Data Structures
There are two implementations of has table. The first uses a **double hashing function in an open-addressing hash table** that avoids colluision by continuously finding unused spots for each hash node. The second uses the **djb2 hash function in a chaining hash table** that avoids collution by chaining the nodes that are given the same hash value. 


## Complexity Discussion
As Cormen et al.(2009) discussed, the operations of both open addressing hash table and chaining table should have O(1) complexity. This is proven as we plot the logN graph together with the runtime graph of two hashtable in complexity_analysis.py, and the logN function clearly dwarf the hash-table approaches. 

The differeces between the runtime of the two tables might be explained by: the choice of hash functions. Djb2 hash function used in the chaining table is proven to be excellent than many other hash functions, including the one we use in open adressing hash table.

<img width="344" alt="Screenshot 2023-11-16 at 7 05 36 PM" src="https://github.com/extraordinary-yh/plagirism-detector/assets/49523649/08fb1196-022d-49fa-9335-139ccd1df0eb">
<img width="367" alt="Screenshot 2023-11-16 at 7 06 00 PM" src="https://github.com/extraordinary-yh/plagirism-detector/assets/49523649/9347a892-7b2a-4f49-90c5-e1592a29f965">

## Advantages 
The code is perfect for detecting three types of plagiarism: direct plagiarism, direct "patchwork" plagiarism, and insufficient citation of partial quotation plagiarism, defined by Northern Illinois University Academic Integrity Tutorial(Plagiarism, 2021). Direct plagiarism or direct "patchwork" plagiarism refers to students directly copying sentences or paragraphs from one or multiple sources, respectively. Insufficient citation also involves using others' original words without citing. Because these plagiarisms include identical sentences or paragraphs, which are substrings of the input, our plagiarism detector can find these identical substrings. 

One concern is the "noise" of commonly used words, like "the" or "and." This can be addressed by a simple tweak: raising the length of substrings(the parameter "k") that we're checking. In the graph below, the detector only finds identical strings of at least 8 letters, and it very well avoided over-detection of duplicate words. In implementation, we can set the "k" parameter to be 8 to achieve the same effect.

## Limitations
The code does not provide adequate detection for paraphrasing or summarizing without citation(Plagiarism, 2021). This is because our data(substrings) is stored by the hash value, which in most cases will be different for different substrings(text). Moreover, our function only returns the index if two texts are exactly the same, preventing paraphrased substrings from being detected. Therefore, our code above cannot detect plagiarism in all cases, which would require further manual inspection. 


## Applications
To apply in real-life, we can put all the documents we like to check against into a single string "x" and store it into the hash table, as shown in the graph below. Then, we calculate the ratio of duplicate letters out of all letters in string "y", which is the document we want to detect plagiarism. We can implement a threshold of similarity, which is generally considered to be 10% (Kadam, 2018). If string "y"'s duplicate indexes surpass that threshold, the detector will push the document to a manual plagiarism review pool for further investigation.
