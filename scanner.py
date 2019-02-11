import os
import string


def scanner(name, vector, comment):
    outcome = -1.0
    if os.path.isfile(name):
        DataFile = open(name, 'r')
    else:
        print("scanner: the file", name, "does not exist")
        raise ("scanner: the file", name, "does not exist")

    for line in DataFile.readlines():
        if not comment in line:
            sline = string.split(line)

            if not len(sline) in [3, 4, 5]:
                raise("Data not supported for " + sline[0])

            parsed_line = {'name': sline[0],
                           'emission': sline[-1],
                           'limit': float(sline[1]) if len(sline) == 5 else float(1),
                           'declaration': float(sline[2]) if len(sline) == 5 else float(sline[1]),
                           'maxlimit': float('inf') if len(sline) == 3 else float(sline[len(sline)-2])}

            vector.append(parsed_line)
    DataFile.close()
    outcome = 1.0
    return outcome
