

def bruteForce(text, items):
    # for i in range(3): 
    #     t1 = str(i)
    #     for k in range(3):
    #         t1 += str(k)
    #         print(t1)
    founded = False
    itemList = items.split(" ")
    for i1 in range(len(itemList)) :
        t1 = itemList[i1]
        for i2 in range(len(itemList)) :
            t1 += itemList[i2]
            if text.lower().strip() in t1.lower().strip() :
                founded = True
                break
    return founded