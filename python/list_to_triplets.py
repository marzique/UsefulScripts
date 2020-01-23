def pack(_list):
    """Split list into list of lists, each child list consists of 3 items"""
    i = 0
    new_list = []
    while True:
        mini_list = _list[i:i+3]
        if mini_list:
            new_list.append(mini_list)
        else:
            break
        i += 3
    return new_list

