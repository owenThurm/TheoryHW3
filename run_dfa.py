import sys
from dfa import dfa
from dfa_functions import run_dfa

user_input = sys.stdin.read()

print("accept" if run_dfa(dfa, user_input) else "reject")
