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

def oldScanner(name, vector, comment):
    outcome=-1.0
## Read every line of the file called name
    if os.path.isfile(name): # Does the file exist?
      DataFile = open(name,'r')
    else:
			print "scanner: the file",name,"does not exist"
 			return -1.0
    for line_with_characters in DataFile.readlines():
## Skip the comments, which begin with "comment" (e.g., '#')
      if ( ( string.find( line_with_characters, comment) ) < 0 ):
# The element vector[0][4] will be the first line, fifth column
         numbers=[]
         for value in string.split(line_with_characters):
             try:
                 numbers.append(float(value))
             except:
                 numbers.append(value)
         if numbers!=[]:
             vector.append(numbers)
    DataFile.close()
    outcome=1.0
    return outcome
#
