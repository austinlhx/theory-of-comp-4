import xml.etree.ElementTree as ET
import itertools

class NFA:
    def __init__(self, states, alpha, delta, start, accepts):
        self.states = states
        self.alpha = alpha
        self.delta = delta
        self.start = start
        self.accepts = accepts

def generate_nfa(file):
    file = ET.parse(file)
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
            #print(child.find('final').attrib['name'])
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
                transition[(from_state, alphabet)] = [to_state]


    myset = set()

    for i in transition:
        myset.add(i[1])

    return NFA(states, list(myset), transition, initial, final)

def nfa_to_xml(nfa):
    root = ET.Element("automaton")
    dict = {}
    iterator = 0
    initial = ET.SubElement(root, "state", id= nfa.start, name=nfa.start)

    # dict[nfa.start] = str(0)

    ET.SubElement(initial, "initial")

    state_left = nfa.states
    for accept in nfa.accepts:
        state_left.remove(accept)

    try:
        state_left.remove(nfa.start)
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

        for state in to_state:
            ET.SubElement(trans, "from").text = str(transition[0])
            ET.SubElement(trans, "to").text = state
            if transition[1] is None:
                ET.SubElement(trans, "read")
            else:
                ET.SubElement(trans, "read").text = str(transition[1])
            


        

    return str(ET.tostring(root))[2:-1]



our_input = input().split(" ")

first_nfa = generate_nfa(our_input[0])
second_nfa = generate_nfa(our_input[1])

new_states = []
new_accept = []
new_transition = {}

for state in second_nfa.states:
    new_states.append(state + "1")

    if state in second_nfa.accepts:
        new_accept.append(state + "1")

for k, v in second_nfa.delta.items():
    first_state = k[0] + "1"
    alphabet = k[1]
    to_state = []
    for to in v:
        to_state.append(to + "1")

    new_transition[(first_state, alphabet)] = to_state



new_states = new_states + first_nfa.states
if isinstance(first_nfa.accepts, list):
    new_accept = new_accept + first_nfa.accepts
else:
    new_accept.append(first_nfa.accepts)


new_transitions = first_nfa.delta


for k, v in new_transition.items():
    first_state = k[0]
    alphabet = k[1]
    to_state = v
    new_transitions[(first_state, alphabet)] = to_state

new_start = "q217"

new_transitions[(new_start, None)] = [first_nfa.start, second_nfa.start + "1"]
new_alpha = first_nfa.alpha + second_nfa.alpha
new_alpha = set(new_alpha)

combined_nfa = NFA(new_states, new_alpha, new_transitions, new_start, new_accept)


# print(combined_nfa.start)
# print(combined_nfa.accepts)
# print(combined_nfa.alpha)
# print(combined_nfa.states)
# print(combined_nfa.delta)



print(nfa_to_xml(combined_nfa))




#print(first_nfa.delta)






#combined_dfa = NFA(combined_states, alphabet, combined_transitions, new_start,accept_states)
#print(nfa_to_xml(combined_dfa))
#print(combined_states)
#print(first_nfa.delta)

#combined_nfa = NFA(combined_states, alphabet, combined_transitions,initial_state,accept_states)
#print(nfa_to_xml(combined_nfa))