"""Classes and methods for working with visual deterministic finite automata."""
from automata.fa.nfa import NFA
from graphviz import Digraph


class VisualNFA:
    """A wrapper for an automata-lib non-deterministic finite automaton."""

    def __init__(self, fa: dict):
        self.nfa = NFA(
            states=fa["states"],
            input_symbols=fa["input_symbols"],
            transitions=fa["transitions"],
            initial_state=fa["initial_state"],
            final_states=fa["final_states"],
        )

    @property
    def states(self) -> set:
        """Pass on .states from the NFA"""
        return self.nfa.states

    @states.setter
    def states(self, states: set):
        """Set .states on the NFA"""
        self.nfa.states = states

    @property
    def input_symbols(self) -> set:
        """Pass on .input_symbols from the NFA"""
        return self.nfa.input_symbols

    @input_symbols.setter
    def input_symbols(self, input_symbols: set):
        """Set .input_symbols on the NFA"""
        self.nfa.input_symbols = input_symbols

    @property
    def transitions(self) -> dict:
        """Pass on .transitions from the NFA"""
        return self.nfa.transitions

    @transitions.setter
    def transitions(self, transitions: dict):
        """Set .transitions on the NFA"""
        self.nfa.transitions = transitions

    @property
    def initial_state(self) -> str:
        """Pass on .initial_state from the NFA"""
        return self.nfa.initial_state

    @initial_state.setter
    def initial_state(self, initial_state: str):
        """Set .initial_state on the NFA"""
        self.nfa.initial_state = initial_state

    @property
    def final_states(self) -> set:
        """Pass on .final_states from the NFA"""
        return self.nfa.final_states

    @final_states.setter
    def final_states(self, final_states: set):
        """Set .final_states on the NFA"""
        self.nfa.final_states = final_states

    @staticmethod
    def _transitions_pairs(all_transitions: dict) -> list:
        """
        Generates a list of all possible transitions pairs for all input symbols.
        Args:
            transition_dict (dict): NFA transitions.
        Returns:
            list: All possible transitions for all the given input symbols.
        """
        transition_possibilities: list = []
        for state, state_transitions in all_transitions.items():
            for symbol, transitions in state_transitions.items():
                if len(transitions) < 2:
                    transition_possibilities.append((state, transitions, symbol))
                else:
                    for transition in transitions:
                        transition_possibilities.append(
                            (state, transition, symbol)
                        )
        return transition_possibilities


    def show_diagram(
        self,
        filename: str = None,
        format_type: str = "png",
        path: str = None,
    ) -> Digraph:
        """
        Generates the graph associated with the given NFA.

        Args:
            nfa (NFA): Deterministic Finite Automata to graph.
            filename (str, optional): Name of output file. Defaults to None.
            format_type (str, optional): File format [svg/png/...]. Defaults to "png".
            path (str, optional): Folder path for output file. Defaults to None.
        Returns:
            Digraph: The graph in dot format.
        """
        # Converting to graphviz preferred input type,
        # keeping the conventional input styles; i.e fig_size(8,8)
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
        for state in sorted(self.nfa.states):
            if (
                state in self.nfa.initial_state and state
                in self.nfa.final_states
            ):
                graph.node(state, shape="doublecircle", fontsize=font_size)
            elif state in self.nfa.initial_state:
                graph.node(state, shape="circle", fontsize=font_size)
            elif state in self.nfa.final_states:
                graph.node(state, shape="doublecircle", fontsize=font_size)
            else:
                graph.node(state, shape="circle", fontsize=font_size)

        # Point initial arrow to the initial state.
        graph.edge("Initial", self.nfa.initial_state, arrowsize=arrow_size)

        # Define all tansitions in the finite state machine.
        all_transitions_pairs = self._transitions_pairs(self.nfa.transitions)

        # Replacing '' key name for empty string (lambda/epsilon) transitions.
        for i, pair in enumerate(all_transitions_pairs):
            if isinstance(pair[1] , frozenset):
                all_transitions_pairs[i] = (pair[0] , list(pair[1])[0] , pair[2])
            if pair[2] == "":
                all_transitions_pairs[i] = (all_transitions_pairs[i][0], all_transitions_pairs[i][1], "λ")

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