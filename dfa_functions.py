from typing import Tuple, List
from xml.etree import ElementTree
from itertools import chain, product
from utils import print_iterable

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

    states = []
    start_state = None
    accept_states = []

    alphabet = []
    delta = {}

    for child in automation_tag:
        if child.tag == "state":
            attributes = child.attrib
            name = ""
            if attributes:
                name = attributes.get("id")
            states.append(name)

            for nested_child in child:
                if nested_child.tag == "initial":
                    start_state = name
                if nested_child.tag == "final":
                    accept_states.append(name)
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
                        alphabet.append(read_value)
                delta[from_state][read_value] = to_state

    return (states, alphabet, delta, start_state, accept_states)

def get_language_for_dfa(dfa: Tuple, max_length: int = 5) -> List:

    states, alpha, delta, start_state, accept_states = dfa

    all_strings = list(chain.from_iterable(
        product(alpha, repeat=x) for x in range(max_length+1)
    ))

    language = []

    for string in all_strings:
        if run_dfa(dfa, string):
            language.append(string)

    return language

def dfa_to_xml(dfa: Tuple) -> str:

    states, alpha, delta, start_state, accept_states = dfa

    automation = ElementTree.Element('automation')

    for state in states:
        state_tag = ElementTree.SubElement(automation, 'state', attrib={'id': state, 'name': f'q{state}'})
        if state == start_state:
            ElementTree.SubElement(state_tag, 'initial')
        elif state in accept_states:
            ElementTree.SubElement(state_tag, 'final')

    for state in states:
        for char in alpha:
            transition_tag = ElementTree.SubElement(automation, 'transition')

            from_tag = ElementTree.SubElement(transition_tag, 'from')
            to_tag = ElementTree.SubElement(transition_tag, 'to')
            read_tag  = ElementTree.SubElement(transition_tag, 'read')

            from_tag.text = str(state)
            to_tag.text = str(delta[state][char])
            read_tag.text = str(char)

    return ElementTree.dump(automation)


