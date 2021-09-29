from typing import Tuple, List
from xml.etree import ElementTree
from itertools import chain, product


def run_dfa(dfa: Tuple, input_string: str, curr_state=None) -> bool:

    states, alpha, delta, start_state, accept_states = dfa

    if curr_state is None:
        curr_state = start_state

    if not input_string:
        return curr_state in accept_states

    next_input = input_string[0]
    input_string = input_string[1:]

    return run_dfa(dfa, input_string, curr_state=delta[curr_state][next_input])


def parse_dfa(file_name: str) -> Tuple:
    tree = ElementTree.parse(file_name)
    root = tree.getroot()

    automation_tag = root if root.tag == "automaton" else root.find("automaton")

    states = set()
    start_state = None
    accept_states = set()

    alphabet = set()
    delta = {}

    for child in automation_tag:
        if child.tag == "state":
            attributes = child.attrib
            name = ""
            if attributes:
                name = attributes.get("id")
            states.add(name)

            for nested_child in child:
                if nested_child.tag == "initial":
                    start_state = name
                if nested_child.tag == "final":
                    accept_states.add(name)
        if child.tag == "transition":
            from_state = None
            to_state = None
            read_value = None
            for nested_child in child:
                if nested_child.tag == "from":
                    from_state = nested_child.text
                    if not delta.get(from_state):
                        delta[from_state] = {}
                elif nested_child.tag == "to":
                    to_state = nested_child.text
                elif nested_child.tag == "read":
                    read_value = nested_child.text
                    if read_value not in alphabet:
                        alphabet.add(read_value)
            delta[from_state][read_value] = to_state

    return (states, alphabet, delta, start_state, accept_states)


def get_language_for_dfa(dfa: Tuple, max_length: int = 5) -> List:

    states, alpha, delta, start_state, accept_states = dfa

    all_strings = list(
        chain.from_iterable(product(alpha, repeat=x) for x in range(max_length + 1))
    )

    language = []

    for string in all_strings:
        if run_dfa(dfa, string):
            language.append(string)

    return language


def dfa_to_xml(dfa: Tuple) -> str:

    states, alpha, delta, start_state, accept_states = dfa

    automation = ElementTree.Element("automaton")

    for state in states:
        state_tag = ElementTree.SubElement(
            automation, "state", attrib={"id": state, "name": state}
        )
        if state == start_state:
            ElementTree.SubElement(state_tag, "initial")
        elif state in accept_states:
            ElementTree.SubElement(state_tag, "final")

    for state in states:
        for char in alpha:
            transition_tag = ElementTree.SubElement(automation, "transition")

            from_tag = ElementTree.SubElement(transition_tag, "from")
            to_tag = ElementTree.SubElement(transition_tag, "to")
            read_tag = ElementTree.SubElement(transition_tag, "read")

            from_tag.text = str(state)
            to_tag.text = str(delta[state][char])
            read_tag.text = str(char)

    return ElementTree.dump(automation)


def union_dfas(dfa_1: Tuple, dfa_2: Tuple) -> Tuple:

    states_1, alpha_1, delta_1, start_state_1, accept_states_1 = dfa_1
    states_2, alpha_2, delta_2, start_state_2, accept_states_2 = dfa_2

    union_states = set()

    for one_state in states_1:
        for two_state in states_2:
            union_states.add((one_state, two_state))

    if alpha_1 != alpha_2:
        raise ValueError

    union_delta = {}

    for state in union_states:
        one_state, two_state = state
        for char in alpha_1:
            if not union_delta.get(state):
                union_delta[state] = {}
            union_delta[state][char] = (
                delta_1[one_state][char],
                delta_2[two_state][char],
            )

    union_start_state = start_state_1, start_state_2
    union_accept_states = set()
    for accept_1 in accept_states_1:
        for accept_2 in states_2:
            union_accept_states.add((accept_1, accept_2))

    for accept_1 in states_1:
        for accept_2 in accept_states_2:
            union_accept_states.add((accept_1, accept_2))

    print(union_accept_states)

    return (union_states, alpha_1, union_delta, union_start_state, union_accept_states)
