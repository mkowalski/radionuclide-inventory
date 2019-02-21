import collections


def parseResults(inputFile, outputFile):
    data = collections.defaultdict(list)

    with open(inputFile, 'r') as f:
        content = f.readlines()

    for line in content:
        lparsed = line.rstrip("\n").split(',')
        lparsed = zip(lparsed[0::2], lparsed[1::2])

        for item in lparsed:
            data[item[0]].append(item[1])

    with open(outputFile, 'w') as f:
        for item, val in data.items():
            # print '{},{}'.format(item, ",".join(val))
            f.write('{},{}\n'.format(item, ",".join(val)))
