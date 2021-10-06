import xml.etree.ElementTree as ET
from itertools import chain,combinations

class NFA:
    def __init__(self, states, alpha, delta, start, accepts):
        self.states = states
        self.alpha = alpha
        self.delta = delta
        self.start = start
        self.accepts = accepts

class DFA:
    def __init__(self, states, alpha, delta, start, accepts):
        self.states = states
        self.alpha = alpha
        self.delta = delta
        self.start = start
        self.accepts = accepts

def dfa_to_xml(nfa):
    root = ET.Element("automaton")
    dict = {}
    iterator = 0
    start = "(" + nfa.start + ")"
    if start in nfa.accepts:
        initial = ET.SubElement(root, "state", id= start, name=start)
        ET.SubElement(initial, "initial")
        ET.SubElement(initial, "final")
    else:
        initial = ET.SubElement(root, "state", id= start, name=start)

    # dict[nfa.start] = str(0)

        ET.SubElement(initial, "initial")

    state_left = nfa.states
    for accept in nfa.accepts:
        state_left.remove(accept)

    try:
        state_left.remove(start)
    except ValueError:
        pass

    #print(state_left)
    # #print(state_left)
    for state in state_left:
        ET.SubElement(root, "state", id = state, name = state)


    
    for state in nfa.accepts:
        final = ET.SubElement(root, "state", id= state, name=state)
        ET.SubElement(final, "final")

    
    for transition, to_state in nfa.delta.items():
        trans = ET.SubElement(root, "transition")

        ET.SubElement(trans, "from").text = str(transition[0])
        ET.SubElement(trans, "to").text = to_state

        ET.SubElement(trans, "read").text = str(transition[1])


        

    return str(ET.tostring(root))[2:-1]


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
       if child.find('initial') is not None and child.find('final') is not None:
                initial = child.attrib["name"]
                final = child.attrib["name"]
       elif child.find('initial') is not None:
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

# print(my_nfa.states)
# print(my_nfa.accepts)
# print(my_nfa.start)

dfa_state = []
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

for result in powerset(my_nfa.states):
    str_sets = str(result)
    str_sets = str_sets.replace(",", "")
    str_sets = str_sets.replace("'", "")
    dfa_state.append(str_sets)
#print(dfa_state)
accept_state = []

#print(my_nfa.accepts)
for state in dfa_state:
    for accept in my_nfa.accepts:
        if accept in state:
            accept_state.append(state)
            break



#print(dfa_state)

#print(my_nfa.delta)

dfa_transition = {}
if None in my_nfa.alpha:
    my_nfa.alpha.remove(None)
for alpha in my_nfa.alpha:
    for state in dfa_state:
        current_state = state.replace("(", "")
        current_state = current_state.replace(")", "")
        current_state = current_state.split(" ")
        new_state = set()
        for s in current_state:
            
            if my_nfa.delta.get((s, alpha)):
                for sta in my_nfa.delta[(s, alpha)]:
                    new_state.add(sta)
                    if my_nfa.delta.get((sta, None)):
                        for sta in my_nfa.delta[(sta, None)]:
                            new_state.add(sta)
                            
            

        #                     next_state = set()
        # for s in current_state:
        #     if nfa.delta.get((s, char)):
        #         for sta in nfa.delta[(s, char)]:
        #             if nfa.delta.get((sta, None)):
        #                 epsilon_states = nfa.delta[(sta, None)]
        #                 for st in epsilon_states:
        #                     next_state.add(st) 
        #             next_state.add(sta)
        # current_state = next_state
            temp = list(new_state)
            temp.sort(key=lambda x:x[1])
            my_string = "("
            for n in temp:
                my_string += n + " "
            my_string = my_string[:-1]
            my_string += ")"
            if len(new_state) != 0:
                dfa_transition[(state, alpha)] = my_string
            else:
                dfa_transition[(state, alpha)] = "()"



my_dfa = DFA(dfa_state, my_nfa.alpha, dfa_transition, my_nfa.start, accept_state)
print(dfa_to_xml(my_dfa))


#print("hi".split(" "))

#my_dfa = DFA(dfa_state, my_nfa.alpha, transition, my_nfa.start, accept_state)

