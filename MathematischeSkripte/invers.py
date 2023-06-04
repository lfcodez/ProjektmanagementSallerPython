from sympy import *
from gauss import *

# Returns the inverse of the matrix A if it exists
# Returns None otherwise
def inverse(A):
    dim = shape(A)
    if dim[0] != dim[1]:
        return None
    else:
        n = dim[0]
        # For calculating the inverse, the unitary matrix is appended after A
        A = Matrix([[A, eye(n)]])
        G = gauss(A)
        # G[1] is the list of pivots
        # A invertible is equivalent to G[1] = [0, 1, ... , n-1]
        if G[1] == tuple(range(0,n)):
            # The first half of G is the unitary matrix
            # return the second half of the Matrix G
            return (gauss(A)[0])[:, list(range(n, 2*n))]
        else:
            return None