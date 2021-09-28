from dfa_functions import dfa_to_xml

STATE_0 = "0"
STATE_1 = "1"
STATE_2 = "2"
STATE_3 = "3"
STATE_4 = "4"

SYMBOL_0 = "0"
SYMBOL_1 = "1"


states = set([STATE_0, STATE_1, STATE_2, STATE_3, STATE_4])

alpha = set([SYMBOL_0, SYMBOL_1])

delta = {
    STATE_0: {
        SYMBOL_0: STATE_0,
        SYMBOL_1: STATE_1,
    },
    STATE_1: {
        SYMBOL_0: STATE_1,
        SYMBOL_1: STATE_2,
    },
    STATE_2: {
        SYMBOL_0: STATE_2,
        SYMBOL_1: STATE_3,
    },
    STATE_3: {
        SYMBOL_0: STATE_3,
        SYMBOL_1: STATE_4,
    },
    STATE_4: {
        SYMBOL_0: STATE_4,
        SYMBOL_1: STATE_4,
    },
}

start_state = STATE_0

accept_states = set([STATE_3])


dfa = (states, alpha, delta, start_state, accept_states)


dfa_to_xml(dfa)

