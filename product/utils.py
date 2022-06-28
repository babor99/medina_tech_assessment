
def decimalize_list(arr):
    lst = []
    for item in arr:
        i = 0
        while i <= 0.9:
            lst.append( int(item) + i)
            i += 0.1
    return lst