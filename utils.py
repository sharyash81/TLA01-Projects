import json


global fa


def read_fa(jsonpath: str):
    """ read input file and store it in dict """
    global fa
    f = open(jsonpath)
    fa = json.load(f)


def standardize_nfa_transition():
    """ cast NFA transition from string to dict """
    global fa
    for state, state_transitions in fa["transitions"].items():
        for key in state_transitions.keys():
            fa["transitions"][state][key] = eval(fa["transitions"][state][key])


def create_standard_fa(vis_mod=0):
    """ cast FA properties from string to dic"""
    fa["states"] = eval(fa["states"])
    fa["input_symbols"] = eval(fa["input_symbols"])
    fa["final_states"] = eval(fa["final_states"])
    fa["initial_state"] = fa["initial_state"]
    if vis_mod == 1:
        standardize_nfa_transition()
    return fa




