from sympy import *

# bitList is a list of 4 bits
# generateHamming return a list of 7 bits, which consists of the 4 input bits
# and 3 additional parity bits 
def generateHamming(bitList):
    # G is a 7x4 Matrix for encoding
    G = Matrix([[1, 1, 0, 1],
                [1, 0, 1, 1],
                [1, 0, 0, 0],
                [0, 1, 1, 1], 
                [0, 1, 0, 0], 
                [0, 0, 1, 0], 
                [0, 0, 0, 1]])
    x = Matrix(bitList)
    y = (G * x) % 2
    # y[0], y[1], y[3] are parity bits
    # y[2], y[4], y[5], y[6] are the bits from bitList
    return list(y)

# bitList is a list of 7 bits
# decodeHamming corrects up to 1 bit flip
# In this case, it returns a tuple consisting of the original
# 4 message bits and a string with information about the corrected bit
def decodeHamming(bitList):
    # H is a 3x7 Matrix for bit flip error checking
    H = Matrix([[1, 0, 1, 0, 1, 0, 1], 
                [0, 1, 1, 0, 0, 1, 1], 
                [0, 0, 0, 1, 1, 1, 1]])
    r = Matrix(bitList)
    zeros3 = zeros(3, 1)
    # The result of the Multiplication of H and r (mod 2)
    # tells if the parity and the message bits are in sync
    if zeros3 == (H * r) % 2:
        return ([r[2], r[4], r[5], r[6]], "Kein Bit korrigiert")
    else:
        # Test all possible bit flips
        for i in range(0, 7):
            e = zeros(7, 1)
            e[i] = 1
            rNew = (r + e) % 2
            # rNew differs from r in the i-th bit
            if zeros3 == (H * rNew) % 2:
                return ([rNew[2], rNew[4], rNew[5], rNew[6]], "Bit "+str(i+1)+" korrigiert")