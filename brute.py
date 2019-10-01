

def bruteForce(text, list):
    list2 = 'abcdefghijklmnopqrstuvwxyz'
    complete_list = []
    for current in range(10):
        a = [i for i in list2]
        for y in range(current):
            a = [x+i for i in list2 for x in a]
        complete_list = complete_list+a