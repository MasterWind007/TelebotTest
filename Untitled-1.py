
lst = {'a': 8,
       'b': 4,
       'c': 13,
       'd': 10,
       'e': 170,
       'f': 30}

def sort (list):
    prev_key = ''
    max_val = 0
    max_key = ''
    for i in list:
        if list.get(i) > max_val: 
            prev_key = max_key  
            max_val = list.get(i)
            max_key = i
    return((prev_key, max_key))

def sort_next(list):
    prev_key = []
    max_val = 0
    max_key = ''
    for i in list:
        if list.get(i) >= max_val: 
            prev_key.append(max_key)  
            max_val = list.get(i)
            max_key = i
    return((prev_key[1:], max_key))
       

print (sort (lst))
# print (sort_next (lst))