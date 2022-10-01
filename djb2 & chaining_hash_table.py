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

#show that the two approaches give the same answer.
assert(regular_get_match(text1, text2, 8)) == rh_get_match(text1, text2, 8)


# "Hash Functions". (2021). York University CSE. Retrieved from http://www.cse.yorku.ca/~oz/hash.html


# ## Q4: Contrasting two approaches

#input texts
#text3 is the first chapter of 2001:A Space Odyssey(Clarke, 1968)
text3 = "The Road to Extinction The drought had lasted now for ten million years, and the reign of the terrible lizards had long since ended. Here on the Equator, in the continent which would one day be known as Africa, the battle for existence had reached a new climax of ferocity, and the victor was not yet in sight. In this barren and desiccated land only the small or the swift or the fierce could flourish, or even hope to survive.The man-apes of the veldt were none of these things, and they were not flourishing; indeed, they were already far down the road to racial extinction. About fifty of them occupied a group of caves overlooking a small, parched valley, which was divided by a sluggish stream fed from snows in the mountains two hundred miles to the north. In bad times the stream vanished completely, and the tribe lived in the shadow of thirst.It was always hungry, and now it was starving. When the first faint glow of dawn crept into the cave Moon-Watcher saw that his father had died in the night. He did not know that the Old One was his father, for such a relationship was utterly beyond his understanding, but as he looked at the emaciated body he felt a dim disquiet that was the ancestor of sadness.The two babies were already whimpering for food, but became silent when Moon-Watcher snarled at them. One of the mothers, defending the infant she could not properly feed, gave him an angry growl in return; he lacked the energy even to cuff her for her presumption.Now it was light enough to leave. Moon-Watcher picked up the shrivelled corpse, and dragged it after him as he bent under the low overhang of the cave. Once outside, he threw the body over his shoulder and stood upright – the only animal in all this world able to do so.Among his kind, Moon-Watcher was almost a giant. He was nearly five feet high, and though badly under-nourished weighed over a hundred pounds. His hairy, muscular body was half-way between ape and man, but his head was already much nearer to man than ape. The forehead was low, and there were ridges over the eye-sockets, yet he unmistakably held in his genes the promise of humanity. As he looked out upon the hostile world of the Pleistocene there was already something in his gaze beyond the capacity of any ape. In those dark, deep-set eyes was a dawning awareness – the first intimations of an intelligence that could not possibly fulfil itself for ages yet, and might soon be extinguished for ever.There was no sign of danger, so Moon-Watcher began to scramble down the almost vertical slope outside the cave, only slightly hindered by his burden. As if they had been waiting for his signal, the rest of the tribe emerged from their own homes further down the rock-face, and began to hasten towards the muddy waters of the stream for their morning drink.Moon-Watcher looked across the valley to see if the Others were in sight, but there was no trace of them. Perhaps they had not yet left their caves, or were already foraging further along the hillside. Since they were nowhere to be seen, Moon-Watcher forgot them; he was incapable of worrying about more than one thing at a time.First he must get rid of the Old One, but this was a problem that demanded little thought. There had been many deaths this season, one of them in his own cave; he had only to put the corpse where he had left the new baby at the last quarter of the moon, and the hyenas would do the rest.They were already waiting, where the little valley farmed out into the savannah, almost as if they had known that he was coming. Moon-Watcher left the body under a small bush – all the earlier bones had already gone – and hurried back to rejoin the tribe. He never thought of his father again.His two mates, the adults from the other cave, and most of the youngsters were foraging among the drought-stunted trees further up the valley, looking for berries, succulent roots and leaves, and occasional windfalls like small lizards or rodents. Only the babies and the feeblest of the old folk were left in the caves; if there was any surplus food at the end of the day’s searching they might be fed. If not, the hyenas would soon be in luck once more.But this day was a good one – though as Moon-Watcher had no real remembrance of the past, he could not compare one time with another. He had found the hive of bees in the stump of a dead tree, and so had enjoyed the finest delicacy that his people could ever know; he still licked his fingers from time to time as he led the group homewards in the late afternoon. Of course, he had also collected a fair number of stings, but he had scarcely noticed them. He was now as near to contentment as he was ever likely to be; for though he was still hungry, he was not actually weak with hunger. That was the most for which any man-ape could ever aspire.His contentment vanished when he reached the stream. The Others were there. They were there every day, but that did not make it any the less annoying.There were about thirty of them, and they could not have been distinguished from the members of Moon-Watcher’s own tribe. As they saw him coming they began to dance, shake their arms, and shriek on their side of the stream, and his own people replied in kind.And that was all that happened. Though the man-apes often fought and wrestled among each other, their disputes very seldom resulted in serious injuries. Having no claws or fighting canines, and being well protected by hair, they could not inflict much harm on one another. In any event, they had little surplus energy for such unproductive behaviour; snarling and threatening was a much more efficient way of asserting their points of view.The confrontation lasted about five minutes; then the display died out as quickly as it had begun, and everyone drank his fill of the muddy water. Honour had been satisfied; each group had staked its claim to its own territory. This important business having been settled, the tribe moved off along its side of the river. The nearest worthwhile grazing was now more than a mile from the caves, and they had to share it with a herd of large, antelope-like beasts who barely tolerated their presence. They could not be driven away, for they were armed with ferocious daggers on their foreheads – the natural weapons which the man-apes did not possess.So Moon-Watcher and his companions chewed berries and fruit and leaves and fought off the pangs of hunger – while all around them, competing for the same fodder, was a potential source of more food than they could ever hope to eat. Yet the thousands of tons of succulent meat roaming over the savannah and through the bush was not only beyond their reach; it was beyond their imagination. In the midst of plenty they were slowly starving to death.The tribe returned to its cave without incident, in the last light of the day. The injured female who had remained behind cooed with pleasure as Moon-Watcher gave her a berry-covered branch he had brought back, and began to attack it ravenously. There was little enough nourishment here, but it would help her to survive until the wound the leopard had given her had healed, and she could forage for herself again.Over the valley, a full moon was rising, and a chill wind was blowing down from the distant mountains. It would be very cold tonight – but cold, like hunger, was not a matter for any real concern; it was merely part of the background of life.Moon-Watcher barely stirred when the shrieks and screams echoed up the slope from one of the lower caves, and he did not need to hear the occasional growl of the leopard to know exactly what was happening. Down there in the darkness old White Hair and his family were fighting and dying, and the thought that he might help in some way never crossed Moon-Watcher’s mind. The harsh logic of survival ruled out such fancies, and not a voice was raised in protest from the listening hillside. Every cave was silent, lest it also attract disaster.The tumult died away, and presently Moon-Watcher could hear the sound of a body being dragged over rocks. That lasted only a few seconds; then the leopard got a good hold on its kill. It made no further noise as it padded silently away, carrying its victim effortlessly in its jaws.For a day or two there would be no further danger here, but there might be other enemies abroad, taking advantage of this cold Little Sun that shone only by night. If there was sufficient warning the smaller predators would sometimes be scared away by shouts and screams. Moon-Watcher crawled out of the cave, clambered on to a large boulder beside the entrance, and squatted there to survey the valley.Of all the creatures who had yet walked on Earth, the man-apes were the first to look steadfastly at the Moon. And though he could not remember it, when he was very young Moon-Watcher would sometimes reach out and try to touch that ghostly face rising above the hills.He had never succeeded, and now he was old enough to understand why. For first, of course, he must find a high enough tree to climb.Sometimes he watched the valley, and sometimes he watched the Moon, but always he listened. Once or twice he dozed off, but he slept with a hair-trigger alertness, and the slightest sound would have disturbed him. At the great age of twenty-five he was still in full possession of all his faculties; if his luck continued, and he avoided accidents, disease, predators and starvation, he might survive for as much as another ten years.The night wore on, cold and clear, without further alarms, and the Moon rose slowly amid equatorial constellations that no human eye would ever see. In the caves, between spells of fitful dozing and fearful waiting, were being born the nightmares of generations yet to be.And twice there passed slowly across the sky, rising up the zenith and descending into the east, a dazzling point of light more brilliant than any star."
#text4 is the a portion of first chapter of The Three-Body Problem(Liu, 2008)
text4 = "Silent Spring 1 The Madness Years China, 1967 The Red Union had been attacking the headquarters of the April Twenty-eighth Brigade for two days. Their red flags fluttered restlessly around the brigade building like flames yearning for firewood.The Red Union commander was anxious, though not because of the defenders he faced. The more than two hundred Red Guards of the April Twenty-eighth Brigade were mere greenhorns compared with the veteran Red Guards of the Red Union, which was formed at the start of the Great Proletarian Cultural Revolution in early 1966. The Red Union had been tempered by the tumultuous experience of revolutionary tours around the country and seeing Chairman Mao in the great rallies in Tiananmen Square. But the commander was afraid of the dozen or so iron stoves inside the building, filled with explosives and connected to each other by electric detonators. He couldn’t see them, but he could feel their presence like iron sensing the pull of a nearby magnet. If a defender flipped the switch, revolutionaries and counter-revolutionaries alike would all die in one giant ball of fire.And the young Red Guards of the April Twenty-eighth Brigade were indeed capable of such madness. Compared with the weathered men and women of the first generation of Red Guards, the new rebels were a pack of wolves on hot coals, crazier than crazy.The slender figure of a beautiful young girl emerged at the top of the building, waving the giant red banner of the April Twenty-eighth Brigade. Her appearance was greeted immediately by a cacophony of gunshots. The weapons attacking her were a diverse mix: antiques such as American carbines, Czech-style machine guns, Japanese Type-38 rifles; newer weapons such as standard-issue People’s Liberation Army rifles and submachine guns, stolen from the PLA after the publication of the “August Editorial”*; and even a few Chinese dadao swords and spears. Together, they formed a condensed version of modern history.* Translator’s Note: This refers to the August 1967 editorial in Red Flag magazine (an important source of propaganda during the Cultural Revolution), which advocated for “pulling out the handful [of counter-revolutionaries] within the army.” Many read the editorial as tacitly encouraging Red Guards to attack military armories and seize weapons from the PLA, further inflaming the local civil wars waged by Red Guard factions.Numerous members of the April Twenty-eighth Brigade had engaged in similar displays before. They’d stand on top of the building, wave a flag, shout slogans through megaphones, and scatter flyers at the attackers below. Every time, the courageous man or woman had been able to retreat safely from the hailstorm of bullets and earn glory for their valor.The new girl clearly thought she’d be just as lucky. She waved the battle banner as though brandishing her burning youth, trusting that the enemy would be burnt to ashes in the revolutionary flames, imagining that an ideal world would be born tomorrow from the ardor and zeal coursing through her blood.… She was intoxicated by her brilliant, crimson dream until a bullet pierced her chest.Her fifteen-year-old body was so soft that the bullet hardly slowed down as it passed through it and whistled in the air behind her. The young Red Guard tumbled down along with her flag, her light form descending even more slowly than the piece of red fabric, like a little bird unwilling to leave the sky.The Red Union warriors shouted in joy. A few rushed to the foot of the building, tore away the battle banner of the April Twenty-eighth Brigade, and seized the slender, lifeless body. They raised their trophy overhead and flaunted it for a while before tossing it toward the top of the metal gate of the compound.Most of the gate’s metal bars, capped with sharp tips, had been pulled down at the beginning of the factional civil wars to be used as spears, but two still remained. As their sharp tips caught the girl, life seemed to return momentarily to her body.The Red Guards backed up some distance and began to use the impaled body for target practice. For her, the dense storm of bullets was now no different from a gentle rain, as she could no longer feel anything. From time to time, her vinelike arms jerked across her body softly, as though she were flicking off drops of rain.And then half of her young head was blown away, and only a single, beautiful eye remained to stare at the blue sky of 1967. There was no pain in that gaze, only solidified devotion and yearning.And yet, compared to some others, she was fortunate. At least she died in the throes of passionately sacrificing herself for an ideal.Battles like this one raged across Beijing like a multitude of CPUs working in parallel, their combined output, the Cultural Revolution. A flood of madness drowned the city and seeped into every nook and cranny.At the edge of the city, on the exercise grounds of Tsinghua University, a mass “struggle session” attended by thousands had been going on for nearly two hours. This was a public rally intended to humiliate and break down the enemies of the revolution through verbal and physical abuse until they confessed to their crimes before the crowd.As the revolutionaries had splintered into numerous factions, opposing forces everywhere engaged in complex maneuvers and contests. Within the university, intense conflicts erupted between the Red Guards, the Cultural Revolution Working Group, the Workers’ Propaganda Team, and the Military Propaganda Team. And each faction divided into new rebel groups from time to time, each based on different backgrounds and agendas, leading to even more ruthless fighting.But for this mass struggle session, the victims were the reactionary bourgeois academic authorities. These were the enemies of every faction, and they had no choice but to endure cruel attacks from every side.Compared to other “Monsters and Demons,”* reactionary academic authorities were special: during the earliest struggle sessions, they had been both arrogant and stubborn. That was also the stage in which they had died in the largest numbers. Over a period of forty days, in Beijing alone, more than seventeen hundred victims of struggle sessions were beaten to death. Many others picked an easier path to avoid the madness: Lao She, Wu Han, Jian Bozan, Fu Lei, Zhao Jiuzhang, Yi Qun, Wen Jie, Hai Mo, and other once-respected intellectuals had all chosen to end their lives.*** Translator’s Note: Originally a term from Buddhism, “Monsters and Demons” was used during the Cultural Revolution to refer to all the enemies of the revolution.** Translator’s Note: These were some of the most famous intellectuals who committed suicide during the Cultural Revolution. Lao She: writer; Wu Han: historian; Jian Bozan: historian; Fu Lei: translator and critic; Zhao Jiuzhang: meteorologist and geophysicist; Yi Qun: writer; Wen Jie: poet; Hai Mo: screenwriter and novelist.Those who survived that initial period gradually became numb as the ruthless struggle sessions continued. The protective mental shell helped them avoid total breakdown. They often seemed to be half asleep during the sessions and would only startle awake when someone screamed in their faces to make them mechanically recite their confessions, already repeated countless times.Then, some of them entered a third stage. The constant, unceasing struggle sessions injected vivid political images into their consciousness like mercury, until their minds, erected upon knowledge and rationality, collapsed under the assault. They began to really believe that they were guilty, to see how they had harmed the great cause of the revolution. They cried, and their repentance was far deeper and more sincere than that of those Monsters and Demons who were not intellectuals.For the Red Guards, heaping abuse upon victims in those two latter mental stages was utterly boring. Only those Monsters and Demons who were still in the initial stage could give their overstimulated brains the thrill they craved, like the red cape of the matador. But such desirable victims had grown scarce. In Tsinghua there was probably only one left. Because he was so rare, he was reserved for the very end of the struggle session.Ye Zhetai had survived the Cultural Revolution so far, but he remained in the first mental stage. He refused to repent, to kill himself, or to become numb. When this physics professor walked onto the stage in front of the crowd, his expression clearly said: Let the cross I bear be even heavier.The Red Guards did indeed have him carry a burden, but it wasn’t a cross. Other victims wore tall hats made from bamboo frames, but his was welded from thick steel bars. And the plaque he wore around his neck wasn’t wooden, like the others, but an iron door taken from a laboratory oven. His name was written on the door in striking black characters, and two red diagonals were drawn across them in a large X.Twice the number of Red Guards used for other victims escorted Ye onto the stage: two men and four women. The two young men strode with confidence and purpose, the very image of mature Bolshevik youths. They were both fourth-year students* majoring in theoretical physics, and Ye was their professor. The women, really girls, were much younger, second-year students from the junior high school attached to the university.** Dressed in military uniforms and equipped with bandoliers, they exuded youthful vigor and surrounded Ye Zhetai like four green flames. * Translator’s Note: Chinese colleges (and Tsinghua in particular) have a complicated history of shifting between four-year, five-year, and three-year systems up to the time of the Cultural Revolution. I’ve therefore avoided using American terms such as “freshman,” “sophomore,” “junior,” and “senior” to translate the classes of these students."


