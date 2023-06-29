from sympy import *

# return the determinant of the matrix A
def laplace(A):
    dim = shape(A)
    # Square matrix is needed
    if dim[0] != dim[1]:
        return None
    else:
        # We use recursion on the dimension to calculate the determinant
        n = dim[0]
        if n == 1:
            return A[0,0]
        else:
            detA = 0
            parity = 1
            columns = list(range(0,n))
            # columns = [0, 1, ... , n-1]
            # Laplace expansion on the first row
            for j in range(0,n):
                columns.remove(j)
                # A[1:,columns] is the matrix A without row 1 and column j
                # A[1:,columns] has dimension (n-1)x(n-1)
                c = parity * A[0,j] * laplace(A[1:,columns])
                detA += c
                columns.insert(j,j)
                parity *= -1
            return detA