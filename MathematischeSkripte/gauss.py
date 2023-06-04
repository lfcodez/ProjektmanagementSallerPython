from sympy import *

# Multiplication with elementary matrices
# func is the type of row operation to be performed
# z1 and z2 are row numbers
# A is a matrix
def common(func, z1, z2, c, A):
    dim = shape(A)
    E = eye(dim[0])
    # Define conresponding Matrix E depending of the row operation func
    if func == multRow or func == multRowAdd:
        E[z1, z2] = c
    if func == swapRows:
        E[z1,z1] = 0
        E[z2,z2] = 0
        E[z1,z2] = 1
        E[z2,z1] = 1
    B = E*A
    # B is the resulting Matrix after the row operation on A
    B.applyfunc(simplify)
    return B

# Multiplication of row z from matrix A with the constant c
def multRow(z, c, A):
    return common(multRow, z, z, c, A)

# Add c times row z2 to the row z1 of matrix A
def multRowAdd(z1, z2, c, A):
    return common(multRowAdd, z1, z2, c, A)

# Swap the rows z1 and z2 of matrix A
def swapRows(z1, z2, A):
    return common(swapRows, z1, z2, None, A)

# Returns the row echelon form of the matrix A 
# and a list of the columns form the pivot elements
def gauss(A):
    dim = shape(A)
    rows, columns = dim[0], dim[1]
    [i, j] = [0, 0]
    A.applyfunc(simplify)
    # store pivot elements
    pivots = []
    # start in top left corner of the matrix
    while(i < rows and j < columns):
        # try finding pivot element in column j
        if (A[i,j]==0):
            for k in range(i+1, rows):
                if 0 != A[k,j]:
                    A = swapRows(i, k, A)
                    break
        # use pivot element to eliminate below in column j
        if A[i,j] != 0:
            pivots.append(j)
            # normalize A[i,j]
            A = multRow(i, 1/A[i,j], A)
            for k in range(i+1, rows):
                # eliminate A[k,j]
                A = multRowAdd(k, i, -A[k,j], A)
            # go to next row and column
            i += 1
            j += 1
        else:
            # go to next column
            j += 1
    # eliminate above pivot elements
    i = 0
    for j in pivots:
        for k in range(0, i):
            # eliminate A[k,j]
            A = multRowAdd(k, i, -A[k,j], A)
        i += 1
    return (A, tuple(pivots))