from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())

def calcost(matrix,i,j,a,b):
    """Calculate cost in ij, return a tuple of (cost,operation)"""
    cost_del = matrix[i-1][j][0] + 1
    cost_ins = matrix[i][j-1][0] + 1
    if a[i-1] == b[j-1]:
        cost_sub = matrix[i-1][j-1][0]
    else:
        cost_sub = matrix[i-1][j-1][0] + 1
    cost = min([cost_del,cost_ins,cost_sub])

    if cost == cost_del:
        operation = Operation.DELETED
    elif cost == cost_ins:
        operation = Operation.INSERTED
    elif cost == cost_sub:
        operation = Operation.SUBSTITUTED
    #print("In" + str(i) + str(j) + "-->" + str((cost,operation)))
    return (cost,operation)


def distances(a, b):
    """Calculate edit distance from a to b"""

    # create correct dimension empty 2D list
    matrix = [[(0,None)]]
    for i in range(1,len(a)+1): # 1 to 3
        matrix.append([])



    # fill first row
    for j in range(1,len(b)+1):
        matrix[0].append((j,Operation.INSERTED))
    # fill first column
    for i in range(len(a)):
        matrix[i+1] = [(i+1,Operation.DELETED)]

    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
                matrix[i].append(calcost(matrix,i,j,a,b))
    #print(matrix)
    return matrix

#distances("cat","ate")