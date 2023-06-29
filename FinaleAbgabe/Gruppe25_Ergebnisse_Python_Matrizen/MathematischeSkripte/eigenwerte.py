from sympy import *
from laplace import *

# Calculates the list of eigenvalues of matrix A
def eigenVal(A):
    dim = shape(A)
    if dim[0] != dim[1]:
        return None
    else:
        n = dim[0]
        # Subtract the symoblic variable x form the diagonal of A
        x = symbols('x')
        A = A - x*eye(n)
        # Calculate characteristic polynominal
        charPoly = laplace(A)
        # get the roots of the characteristic polynominal
        return solve(charPoly, x)

# Calculates numeric values for the eigenvalues of matrix A 
def eigenValNumeric(A):
    return list(map(lambda x: x.evalf(), eigenVal(A)))