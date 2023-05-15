from sympy import *

def mult(A, B):
    [dimA, dimB] = [shape(A), shape(B)]
    if dimA[1] != dimB[0]:
        return None
    else:
        C = zeros(dimA[0], dimB[1])
        for i in range(0, dimA[0]):
            for j in range(0, dimB[1]):
                for k in range(0, dimA[1]):
                    C[i,j] += A[i,k]*B[k,j]
        return simplify(C)


# Multiplikation mit Elementarmatirzen
def common(func, z1, z2, c, A):
    dim = shape(A)
    E = eye(dim[0])
    if func == multRow or func == multRowAdd:
        E[z1, z2] = c
    if func == swapRows:
        E[z1,z1] = 0
        E[z2,z2] = 0
        E[z1,z2] = 1
        E[z2,z1] = 1
    B = E*A
    B.applyfunc(simplify)
    return B

def multRow(z, c, A):
    return common(multRow, z, z, c, A)

def multRowAdd(z1, z2, c, A):
    return common(multRowAdd, z1, z2, c, A)

def swapRows(z1, z2, A):
    return common(swapRows, z1, z2, None, A)


def gauß(A):
    dim = shape(A)
    rows, columns = dim[0], dim[1]
    [i, j] = [0, 0]
    A.applyfunc(simplify)
    pivots = []
    pivotVars = []
    while(i < rows and j < columns):
        if (A[i,j]==0):
            for k in range(i+1, rows):
                if 0 != A[k,j]:
                    A = swapRows(i, k, A)
                    break
        if A[i,j] != 0:
            pivots.append((i,j))
            pivotVars.append(j)
            A = multRow(i, 1/A[i,j], A)
            for k in range(i+1, rows):
                A = multRowAdd(k, i, -A[k,j], A)
            i += 1
            j += 1
        else:
            j += 1
    for (i,j) in pivots:
        for k in range(0, i):
            A = multRowAdd(k, i, -A[k,j], A)
    return (A, tuple(pivotVars))


def inverse(A):
    dim = shape(A)
    if dim[0] != dim[1]:
        return None
    else:
        n = dim[0]
        A = Matrix([[A, eye(n)]])
        G = gauß(A)
        if G[1] == tuple(range(0,n)):
            return (gauß(A)[0])[:, list(range(n, 2*n))]
        else:
            return None
        
        
def laplace(A):
    dim = shape(A)
    if dim[0] != dim[1]:
        return None
    else:
        n = dim[0]
        if n == 1:
            return A[0,0]
        else:
            detA = 0
            parity = 1
            columns = list(range(0,n))
            for j in range(0,n):
                columns.remove(j)
                
                c = parity * A[0,j] * laplace(A[1:,columns])
                detA += c
                columns.insert(j,j)
                parity *= -1
            return detA


def eigenVal(A):
    dim = shape(A)
    if dim[0] != dim[1]:
        return None
    else:
        n = dim[0]
        x = symbols('x')
        A = A - x*eye(n)
        charPoly = laplace(A)
        return solve(charPoly, x)