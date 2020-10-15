'''DFA minimizer

This is a script to minimize a nested dictionary representation of a DFA, as well as to process strings
in the dfa.

This script accepts external .txt files formated in the following manner:

    - The first line indicates the set of states of the automata separated by commas. - The second line indicates the alphabet symbols separated by commas

    - The third line indicates the initial state

    - The fourth line indicates the set of final states separated by commas.

    - The following lines indicate the evaluation of the extended transition function with the elements of the alphabet in the following format:\n


    state, symbol = > state

    Example, the following line:\n
    q0, a = > q1 \n
    indicates that the DFA processes the following: d(q0,a) = q1




'''
import copy

def processString(dfa, string):
    """
    Function to process a given string in the DFA

    Parameters:
    ---------------
    dfa (dict(dict())): A nested dictionary representation of a DFA
    string (str) : The string to process

    Returns:
    ---------------
    bool: Wether the string was accepted or not

      """
    count = 0
    q = [initial]
    while q:
        value = q.pop(0)
        state = dfa[value]
        if count >= len(string):
            if value in final:
                return True
            return False
        for transition in dfa[value]:
            if string[count] == transition:
                print("from ", value, " to ", dfa[value][transition], " with ", transition)
                q.append(dfa[value][transition])
            elif string[count] not in dfa[value]:
                print("from ", value, " to sink state with ", string[count])
        count += 1
    return False

def changeName(dfa, state, new_state):
    """
       Function to rename dfa states while minimizing

       Parameters:
       ---------------
       dfa (dict(dict())): A nested dictionary representation of a DFA \n
       state (str): The state to rename \n
       new_state (str): The new name of the state

       Returns:
       ---------------
       None
         """
    for element in dfa:
        for letter in dfa[element]:
            if state == dfa[element][letter]:
                dfa[element].update({letter : new_state})


def minimize(dfa):
    """
           Function to minimize a DFA

           Parameters:
           ---------------
           dfa (dict(dict())): A nested dictionary representation of a DFA \n

           Returns:
           ---------------
           min_dfa (dict(dict())): A nested dictionary representation of a minimized DFA
             """
    deleted = []
    min_dfa = copy.deepcopy(dfa)
    changed = True
    while(changed):
        changed = False
        for one_state in dfa:
            for another_state in dfa:
                if one_state != another_state:
                    if one_state in min_dfa and another_state in min_dfa:
                        if min_dfa[one_state] == min_dfa[another_state]:
                            if another_state in min_dfa and another_state not in deleted:
                                if (another_state in final and one_state in final) or (another_state not in final and one_state not in final):


                                    deleted.append(another_state)
                                    deleted.append(one_state)
                                    changed = True
                                    if one_state in initial:
                                        print("state to delete: ", another_state)
                                        del min_dfa[another_state]
                                        if another_state in final:
                                            final.remove(another_state)
                                    elif another_state in initial:
                                        print("state to delete: ", one_state)
                                        if one_state in final:
                                            final.remove(one_state)
                                        del min_dfa[one_state]
                                    else:
                                        print("state to delete: ", another_state)
                                        if another_state in final:
                                            final.remove(another_state)
                                        del min_dfa[another_state]
                                    changeName(min_dfa, another_state, one_state)

    return min_dfa



if __name__ == '__main__':

    path = 'Files/test2.txt'
    file = open(path, 'r')
    dfa = dict(list())
    states = file.readline().strip().split(",")
    alphabet_sym = file.readline().strip().split(",")
    initial = file.readline().strip()
    final = file.readline().strip().split(",")
    print("Data read from file: ")
    print()
    print("All states: ",states)
    print("Alphabet: ",alphabet_sym)
    print("Initial state: ", initial)
    print("Final states: ", final)

    for line in file:
        transition = line.strip().split(",")
        nextState = transition[1].split("=>")
        tup = (nextState[0], nextState[1])
        if transition[0] in dfa:
            dfa[transition[0]].update({nextState[0]: nextState[1]})
        else:
            dfa[transition[0]] = {nextState[0]: nextState[1]}

    print()
    print("Original dfa")
    print(dfa)
    print()
    min_dfa = minimize(dfa)
    print()
    print("Minimized dfa")
    print(min_dfa)
    print()
    print("Final states ", final)
    print("Initial state ", initial)
    print()
    string = input("Enter string to process: ")
    if processString(min_dfa, string):
        print("Accepted")
    else:
        print("Not accepted")
