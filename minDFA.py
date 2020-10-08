import copy
def processString(dfa, string):
    count = 0
    q = [initial]
    while q:
        value = q.pop(0)
        state = dfa[value]
        if count >= len(string):
            if value in final:
                return True
            return False
        for tuple in state:
            if string[count] in tuple:
                q.append(tuple[1])
        count += 1
    return False


def changeName(dfa, state, newState):
    for element in dfa:
        for i in range(len(dfa[element])):
            tuple = dfa[element][i]
            if state in tuple:
                new_tuple = (tuple[0], newState)
                dfa[element][i] = new_tuple

def minimize(dfa):
    deleted = []
    min_dfa = copy.deepcopy(dfa)
    changed = True
    while(changed):
        for one_state in dfa:
            for another_state in dfa:
                if one_state != another_state:
                    changed = False
                    if dfa[one_state] == dfa[another_state]:
                        if another_state in min_dfa and another_state not in deleted:
                            if (another_state in final and one_state in final) or (another_state not in final and one_state not in final):
                                print("state to delete: ", another_state)
                                deleted.append(one_state)
                                deleted.append(another_state)
                                changed = True
                                del min_dfa[another_state]
                                changeName(min_dfa, another_state, one_state)

    return min_dfa


path = 'Files/test1.txt'
file = open(path, 'r')
dfa = dict(list())
states = file.readline().strip().split(",")
alphabet_sym = file.readline().strip().split(",")
initial = file.readline().strip()
final = file.readline().strip().split(",")
print(states)
print(alphabet_sym)
print("Initial: ", initial)
print("Final states: ",final)

for line in file:
    transition = line.strip().split(",")
    nextState = transition[1].split("=>")
    tup = (nextState[0], nextState[1])
    if transition[0] in dfa:
        dfa[transition[0]].append(tup)
    else:
        dfa[transition[0]] = [tup]

print(dfa)
min_dfa = minimize(dfa)
print(min_dfa)
print(processString(min_dfa, "abba"))