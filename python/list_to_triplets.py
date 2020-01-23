def pack(_list, divider=3):
    """
    Split list into list of lists, each child list consists of 3 items by default.
    """
    i = 0
    new_list = []
    while True:
        mini_list = _list[i:i+divider]
        if mini_list:
            new_list.append(mini_list)
        else:
            break
        i += divider
    return new_list
