from sympy import *

# Matrixmultiplikation zweier sympy Matrizen
def mult(A, B):
    # get dimensions of A and B
    [dimA, dimB] = [shape(A), shape(B)]
    if dimA[1] != dimB[0]:
        return None
    else:
        C = zeros(dimA[0], dimB[1])
        # Rows times columns
        for i in range(0, dimA[0]):
            for j in range(0, dimB[1]):
                for k in range(0, dimA[1]):
                    C[i,j] += A[i,k]*B[k,j]
        # Simplify expressions before return
        return simplify(C)