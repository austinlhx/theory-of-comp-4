import xml.etree.ElementTree as ET
from itertools import product

class NFA:
    def __init__(self, states, alpha, delta, start, accepts):
        self.states = states
        self.alpha = alpha
        self.delta = delta
        self.start = start
        self.accepts = accepts


file = ET.parse(input())
root = file.getroot()
if root.tag != "automaton":
    root = root.find("automaton")

states = []
initial = ""
final = []
dict = {}
for child in root:
   #print(child.tag)
   if child.tag == "state":
       states.append(child.attrib["name"])
       dict[child.attrib["id"]] = child.attrib["name"]
       if child.find('initial') is not None:
           initial = child.attrib["name"]
       elif child.find('final') is not None:
           final.append(child.attrib["name"])
    
transition = {}

for child in root:
    if child.tag == "transition":
        from_state = dict[child[0].text]
        to_state = dict[child[1].text]
        alphabet = child[2].text
        if transition.get((from_state, alphabet)):  
            transition[(from_state, alphabet)].append(to_state)
        else:
            transition[(from_state, alphabet)] =  [to_state]


myset = set()

for i in transition:
    myset.add(i[1])
my_nfa = NFA(states, list(myset), transition, initial, final)

string = ""

for char in my_nfa.alpha:
    if char is not None:
        string += char

iterator = 5
cartesian = []

while iterator != 0:
    for p in product(string, repeat=iterator): #Taken from itertools
        str_sets = str(p)
        str_sets = str_sets.replace("(", "")
        str_sets = str_sets.replace(")", "")
        str_sets = str_sets.replace(",", "")
        str_sets = str_sets.replace("'", "")
        str_sets = str_sets.replace(" ", "")
        cartesian.append(str_sets)

    iterator -= 1


def run(nfa, state, string):
    current_state = {state}
    for index, char in enumerate(string):
        next_state = set()
        for s in current_state:
            if nfa.delta.get((s, char)):
                for sta in nfa.delta[(s, char)]:
                    if nfa.delta.get((sta, None)):
                        epsilon_states = nfa.delta[(sta, None)]
                        for st in epsilon_states:
                            next_state.add(st) 
                    next_state.add(sta)
        current_state = next_state
    for st in current_state:
        if st in nfa.accepts:
            return "accept"
    return "reject"




    #     if nfa.delta.get((state, char)):
    #         for s in nfa.delta[(state, char)]:
    #             return run(nfa, s, string[index+1:])
    #     if nfa.delta.get((state, None)):
    #         for s in nfa.delta[(state, None)]:
    #             return run(nfa, s, string[index:])
    #     else:
    #         return "reject"
    # if state in nfa.accepts:    
    #     return "accept"
    # else:
    #     return "reject"


answer = []


for item in cartesian:
    #rint(run(my_dfa, item))
    if run(my_nfa, my_nfa.start, item) == "accept":
        
        answer.append(item)


if len(answer) == 0:
    print("")

for ans in answer:
    print(ans)