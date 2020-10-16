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
    #Initialize counter and queue
    count = 0
    q = [initial]
    #While the queue is not empty, pop the initial value (the state to evaluate)
    while q:
        value = q.pop(0)
        state = dfa[value]
        #If we have reached the end of the string,
        # if the state we are in is final accept the string,
        # otherwise, reject it
        if count >= len(string):
            if value in final:
                return True
            return False
        #For every transition from the state being evaluated,
        # if there is a transition with the current character being processed
        # print the transition and add the resulting state to the queue
        # if there is no transition with the current character, go to sink state
        for transition in dfa[value]:
            if string[count] == transition:
                print("from ", value, " to ", dfa[value][transition], " with ", transition)
                q.append(dfa[value][transition])
            elif string[count] not in dfa[value]:
                print("from ", value, " to sink state with ", string[count])

        #Increase the counter to traverse the string
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
    #For every state in DFA
    for state in dfa:
        #For every transition
        for letter in dfa[state]:
            #If the state we are renaming is a result from any transition, change its name to the new state
            if state == dfa[state][letter]:
                dfa[state].update({letter : new_state})


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
    #Initialize deleted list, the minimized DFA and changed flag
    deleted = []
    min_dfa = copy.deepcopy(dfa)
    changed = True
    #While there is a change (deletion) in the DFA compare two states,
    # if they have the same transitions, they have not been deleted
    # and they are both final or non final, delete them from min_dfa then
    # add them to the deleted list and rename any transitions with the deleted state to the new state
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
                                    #Check if one of the states is initial, in order to avoid its deletion
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
    #Get the path to the file where the DFA description is contained
    path = 'Files/test2.txt'
    file = open(path, 'r')
    #Initialize the DFA
    dfa = dict(dict())
    #Extract all of the states, alphabet, initial states and final states from the file
    states = file.readline().strip().split(",")
    alphabet_sym = file.readline().strip().split(",")
    initial = file.readline().strip()
    final = file.readline().strip().split(",")
    #Print parsed data to terminal
    print("Data read from file: ")
    print()
    print("All states: ",states)
    print("Alphabet: ",alphabet_sym)
    print("Initial state: ", initial)
    print("Final states: ", final)

    #For each remaining line in the file, get the transition, and the states involved in the transition
    for line in file:
        input_array = line.strip().split(",")

        transition_data = input_array[1].split("=>")

        original_state = input_array[0]
        transition_character = transition_data[0]
        resulting_state = transition_data[1]

        #If the original state already has a transition in the DFA, add the new transition to it,
        # otherwise create the new state and its first transition
        if original_state in dfa:
            dfa[original_state].update({transition_character: resulting_state})
        else:
            dfa[original_state] = {transition_character: resulting_state}

    #Print the original DFA for comparison with minimized DFA
    print()
    print("Original dfa")
    print(dfa)
    print()
    #Minimize the DFA
    min_dfa = minimize(dfa)
    #Print the minimized version of the DFA
    print()
    print("Minimized dfa")
    print(min_dfa)
    print()
    #Print the new final states as well as the initial state of the minimzied DFA
    print("Final states ", final)
    print("Initial state ", initial)
    print()
    #Ask for a string to process
    string = input("Enter string to process: ")
    #Process the given string in the DFA
    if processString(min_dfa, string):
        print("Accepted")
    else:
        print("Not accepted")
