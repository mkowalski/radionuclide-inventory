from scanner import scanner


def FMA(inventory):
    limits = []
    scanner('Andra_FMA', limits, '#')

    total_FMA = 0.
    inventoryWithFMA = []
    for a in inventory:
        try:
            b = next(x for x in limits if x['name'] == a[0])
        except StopIteration:
            raise("Missing data for " + a[0])

        name = a[0]
        activity = a[1]

        FMA_fraction1 = (activity / b['limit'] < 1)
        FMA_fraction3 = (b['emission'] == 1)

        inventoryWithFMA.append([name,
                                 activity,
                                 FMA_fraction1,
                                 FMA_fraction3,
                                 b['declaration'],
                                 b['maxlimit']])

        total_FMA = total_FMA + FMA_fraction1 + FMA_fraction3


    print inventoryWithFMA
    return
