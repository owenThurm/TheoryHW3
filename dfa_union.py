import sys
from dfa_functions import parse_dfa, union_dfas, dfa_to_xml

user_input = sys.stdin.read()

file_1, file_2 = user_input.split(" ")

dfa_1 = parse_dfa(file_1)
dfa_2 = parse_dfa(file_2)

union_dfa = union_dfas(dfa_1, dfa_2)

dfa_to_xml(union_dfa)
