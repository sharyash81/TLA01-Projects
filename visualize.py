from utils import read_fa, create_standard_fa
from FA.dfa import VisualDFA
from FA.nfa import VisualNFA


def visualize(jsonpath: str):
    """ visualize the FA :
        first check if its DFA , if yes -> plot it
        else check if its NFA , if yes -> plot it
        else raise Exception
    """

    try:
        read_fa(jsonpath)
        fa = create_standard_fa()
        dfa = VisualDFA(fa)
        dfa.show_diagram()
    except:
        try:
            read_fa(jsonpath)
            fa = create_standard_fa(1)
            nfa = VisualNFA(fa)
            nfa.show_diagram()
        except Exception as ex:
            raise Exception("The input file is neither DFA nor NFA\nCheck whether you "
                            "mentioned a correct file or its in the correct standard format")\
                from ex

