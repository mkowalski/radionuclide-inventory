from scanner import scanner

def FMA1(SE_FMA, inventory):
    limits = []
    scanner('Andra_FMA_2', limits, "#")

    sum_activity = 0.

    inventoryWithFMA = []
    for a in inventory:
        for b in limits:
            if a[0] == b[0]:
                name = a[0]
                activity = a[1]
                # energy=a[2]
                limit = b[1]
                declaration = b[2]
                maxlimit = b[3]
                emission = b[4]
                FMA_fraction3 = (emission == 1)

                inventoryWithFMA.append(
                    [name, activity, FMA_fraction1, FMA_fraction3, declaration,
                     maxlimit, limit])

                sum_activity = sum_activity + activity

            # print (sum_activity)

    RN_list = []

    for c in inventoryWithFMA:
        if c[5] > c[1] / sum_activity * SE_FMA > c[4]:
            RN_list.append([c[0], c[1] / sum_activity * SE_FMA])

    # print(RN_list)
    return (RN_list)
