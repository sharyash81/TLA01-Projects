"""Classes and methods for working with visual deterministic finite automata."""
from automata.fa.dfa import DFA
from graphviz import Digraph


class VisualDFA:
    """A wrapper for an automata-lib deterministic finite automaton."""

    def __init__(self, fa: dict):
        self.dfa = DFA(
            states=fa["states"],
            input_symbols=fa["input_symbols"],
            transitions=fa["transitions"],
            initial_state=fa["initial_state"],
            final_states=fa["final_states"],
        )

    @property
    def states(self):
        """Pass on .states from the DFA"""
        return self.dfa.states

    @states.setter
    def states(self, states: set):
        """Set .states on the DFA"""
        self.dfa.states = states

    @property
    def input_symbols(self):
        """Pass on .input_symbols from the DFA"""
        return self.dfa.input_symbols

    @input_symbols.setter
    def input_symbols(self, input_symbols: set):
        """Set .input_symbols on the DFA"""
        self.dfa.input_symbols = input_symbols

    @property
    def transitions(self):
        """Pass on .transitions from the DFA"""
        return self.dfa.transitions

    @transitions.setter
    def transitions(self, transitions: dict):
        """Set .transitions on the DFA"""
        self.dfa.transitions = transitions

    @property
    def initial_state(self):
        """Pass on .initial_state from the DFA"""
        return self.dfa.initial_state

    @initial_state.setter
    def initial_state(self, initial_state: str):
        """Set .initial_state on the DFA"""
        self.dfa.initial_state = initial_state

    @property
    def final_states(self):
        """Pass on .final_states from the DFA"""
        return self.dfa.final_states

    @final_states.setter
    def final_states(self, final_states: set):
        """Set .final_states on the DFA"""
        self.dfa.final_states = final_states

    @staticmethod
    def __transitions_pairs(transitions: dict) -> list:
        """
        Generates a list of all possible transitions pairs for all input symbols.
        Args:
            transition_dict (dict): DFA transitions.
        Returns:
            list: All possible transitions for all the given input symbols.
        """
        transition_possibilities: list = []
        for state, transitions in transitions.items():
            for symbol, transition in transitions.items():
                transition_possibilities.append((state, transition, symbol))
        return transition_possibilities

    def show_diagram(
        self,
        filename: str = None,
        format_type: str = "png",
        path: str = None
    ) -> Digraph:
        """
        Generates the graph associated with the given DFA.

        Args:
            dfa (DFA): Deterministic Finite Automata to graph.
            filename (str, optional): Name of output file. Defaults to None.
            format_type (str, optional): File format [svg/png/...]. Defaults to "png".
            path (str, optional): Folder path for output file. Defaults to None.
        Returns:
            Digraph: The graph in dot format.
        """
        cleanup = True
        horizontal = True
        reverse_orientation = False
        fig_size = "(8, 8)"
        font_size = "14.0"
        arrow_size = "0.85"
        state_seperation = "0.5"

        # Defining the graph.
        graph = Digraph(strict=False)
        graph.attr(
            size=fig_size,
            ranksep=state_seperation,
        )
        if horizontal:
            graph.attr(rankdir="LR")
        if reverse_orientation:
            if horizontal:
                graph.attr(rankdir="RL")
            else:
                graph.attr(rankdir="BT")

        # Defining arrow to indicate the initial state.
        graph.node("Initial", label="", shape="point", fontsize=font_size)

        # Defining all states.
        for state in sorted(self.dfa.states):
            if (
                state in self.dfa.initial_state and state in
                self.dfa.final_states
            ):
                graph.node(state, shape="doublecircle", fontsize=font_size)
            elif state in self.dfa.initial_state:
                graph.node(state, shape="circle", fontsize=font_size)
            elif state in self.dfa.final_states:
                graph.node(state, shape="doublecircle", fontsize=font_size)
            else:
                graph.node(state, shape="circle", fontsize=font_size)

        # Point initial arrow to the initial state.
        graph.edge("Initial", self.dfa.initial_state, arrowsize=arrow_size)

        # Define all tansitions in the finite state machine.
        all_transitions_pairs = self.__transitions_pairs(self.dfa.transitions)
        for pair in all_transitions_pairs:
            graph.edge(
                pair[0],
                pair[1],
                label=" {} ".format(pair[2]),
                arrowsize=arrow_size,
                fontsize=font_size,
            )

        # Write diagram to file. PNG, SVG, etc.
        if filename:
            graph.render(
                filename=filename,
                format=format_type,
                directory=path,
                cleanup=cleanup,
            )
        graph.render(view=True)
        return graph