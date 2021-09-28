"""
  2021-09-20 - owenthurm

  An implementation of a DFA (according to the data spec defined in ./README.md)
  that models the one shown in Figure 1.4 of the textbook.
"""


STATE_1 = "q1"
STATE_2 = "q2"
STATE_3 = "q3"

SYMBOL_0 = "0"
SYMBOL_1 = "1"


states = set([STATE_1, STATE_2, STATE_3])

alpha = set([SYMBOL_0, SYMBOL_1])

delta = {
    STATE_1: {
        SYMBOL_0: STATE_1,
        SYMBOL_1: STATE_2,
    },
    STATE_2: {
        SYMBOL_0: STATE_3,
        SYMBOL_1: STATE_2,
    },
    STATE_3: {
        SYMBOL_0: STATE_2,
        SYMBOL_1: STATE_2,
    },
}

start_state = STATE_1

accept_states = set([STATE_2])


dfa = (states, alpha, delta, start_state, accept_states)
