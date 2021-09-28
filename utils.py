def print_iterable(iterable, spaces=True):
    iterable_string = ""
    char_pointer = 0

    while char_pointer < len(iterable):
        iterable_string += iterable[char_pointer]
        if spaces:
            iterable_string += " "
        char_pointer += 1

    print(iterable_string)
