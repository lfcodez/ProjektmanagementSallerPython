from sympy import *
from random import seed, randint


# text is the text you want to encode and matrix is the matrix you want to use for encoding
def encode(text, matrix):
    # Hill Cipher works with blocks. The Blocksize is the Dimension of the nxn Matrix
    blockSize = shape(Matrix(matrix))[0]
    textToEncode = str(text)
    # prepare the asciiMatrix to safe the ascii codes for our characters in
    asciiMatrix = Matrix.zeros(1, blockSize)
    encodedText = ""

    # loops through the given text with steps of blockSize
    for i in range(0, len(textToEncode), blockSize):
        # loops through one block
        for j in range(0, blockSize):
            # if the length of the given text does fill all spaces in every block, it gets filled by -1
            if (i + j) >= len(textToEncode):
                asciiValue = -1
            else:
                # gets the ascii code from the given character and subtracts 32
                # because the first 32 ascii codes are not printable
                asciiValue = ord(textToEncode[i + j]) - 32
            asciiMatrix[j] = asciiValue
        # encodes the asciiMatrix. mod 94 at the end because there are 94 ascii codes we are using
        encodedMatrix = (asciiMatrix * Matrix(matrix)) % 94
        # converts the encodes ascii codes to characters
        for j in range(0, blockSize):
            encodedText = str(encodedText) + chr(encodedMatrix[j] + 32)

    return encodedText


# the same as the encode function with the only difference its using the Inverse Matrix to decode the text
def decode(text, invMatrix):
    blockSize = shape(Matrix(invMatrix))[0]
    textToDecode = str(text)
    asciiMatrix = Matrix.zeros(1, blockSize)
    decodedText = ""
    for i in range(0, len(textToDecode), blockSize):
        for j in range(0, blockSize):
            if (i + j) >= len(textToDecode):
                asciiValue = -1
            else:
                asciiValue = ord(textToDecode[i + j]) - 32
            asciiMatrix[j] = asciiValue
        decodedMatrix = (asciiMatrix * Matrix(invMatrix)) % 94
        for j in range(0, blockSize):
            decodedText = str(decodedText) + chr(decodedMatrix[j] + 32)

    print("Verschluesselter Text: " + textToDecode)
    print("Entschluesselter Text: " + decodedText)


# Generates a random Matrix and its Inverse for the given Dimension
def keyGenerator(dim):
    K = zeros(dim)
    seed()
    while gcd(K.det(), 94) != 1:
        for i in range(0, dim):
            for j in range(0, dim):
                K[i, j] = randint(0, 93)
    return K.inv_mod(94), K


def start():
    dim = input("Enter the Dimension of the Matrix to encode/decode to get a random generated one. "
                "For a Dimension > 10 it will be slower to generate a working Matrix. "
                "Do not enter anything if you want to use your own Matrix: ")
    if dim is None:
        matrix = input("Enter your own Matrix: ")
        invMatrix = input("Enter the Inverse for your Matrix: ")
    elif dim.isnumeric():
        matrix, invMatrix = keyGenerator(int(dim))
    else:
        while not (dim.isnumeric() or dim is None):
            dim = input("Enter the Dimension of the Matrix to encode/decode to get a random generated one. "
                        "For a Dimension > 10 it will be slower to generate a working Matrix. "
                        "Do not enter anything if you want to use your own Matrix: ")

        matrix, invMatrix = keyGenerator(int(dim))

    text = input("Enter the text you want to encode and decode: ")
    print("Matrix:")
    pprint(matrix)
    print("Inverse:")
    pprint(invMatrix)
    encoded = encode(text, matrix)
    decode(encoded, invMatrix)


start()
