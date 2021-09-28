from dfa_functions import parse_dfa, get_language_for_dfa
import sys
from utils import print_iterable

user_input = sys.stdin.read()

dfa = parse_dfa(user_input)

language = get_language_for_dfa(dfa)

for word in language:
    print_iterable(word, spaces=False)
