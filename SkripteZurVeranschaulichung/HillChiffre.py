import ast
from sympy import *
from random import seed, randint


# text is the text you want to encode and matrix is the matrix you want to use for encoding
def encode(text, matrix):
    # converts the input string or list, to a list
    if str(type(matrix)) != "<class 'sympy.matrices.dense.MutableDenseMatrix'>":
        matrix = ast.literal_eval(str(matrix))

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
    if str(type(invMatrix)) != "<class 'sympy.matrices.dense.MutableDenseMatrix'>":
        invMatrix = ast.literal_eval(str(invMatrix))
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

    return decodedText


# Generates a random Matrix and its Inverse for the given Dimension
def keyGenerator(dim):
    K = zeros(dim)
    seed()
    while gcd(K.det(), 94) != 1:
        for i in range(0, dim):
            for j in range(0, dim):
                K[i, j] = randint(0, 93)
    return K, K.inv_mod(94)


def is_square_matrix(matrix):
    try:
        matrix = ast.literal_eval(str(matrix))
    except (ValueError, SyntaxError):
        return False

    if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        return False

    rows = len(matrix)
    if rows == 0:
        return False

    cols = len(matrix[0])
    if any(len(row) != cols for row in matrix):
        return False

    return rows == cols


def start():
    dim = input("Enter the Dimension of the Matrix to encode/decode to get a random generated one. \n"
                "For a Dimension > 10 it will be slower to generate a working Matrix. \n"
                "Enter nothing if you want to use your own Matrix: ")
    matrix = None
    invMatrix = None
    case = None
    if not dim:
        userInput = input("To encode enter e, to decode enter d: ")
        if userInput == "e":
            matrix = input("Enter your own Matrix to encode: ")
            if not is_square_matrix(matrix):
                while not is_square_matrix(matrix):
                    matrix = input("Enter your own Matrix to encode: ")
            while gcd(Matrix(ast.literal_eval(matrix)).det(), 94) != 1:
                matrix = input("Enter your own Matrix to encode: ")
            invMatrix = Matrix(ast.literal_eval(matrix)).inv_mod(94)
            case = "e"

        elif userInput == "d":
            invMatrix = input("Enter your own Inverse Matrix to decode: ")
            if not is_square_matrix(invMatrix):
                while not is_square_matrix(invMatrix):
                    invMatrix = input("Enter your own Inverse Matrix to decode: ")
            case = "d"
        else:
            while userInput not in ["e", "d"]:
                userInput = input("To encode enter e, to decode enter d: ")
            if userInput == "e":
                matrix = input("Enter your own Matrix to encode: ")
                if not is_square_matrix(matrix):
                    while not is_square_matrix(matrix):
                        matrix = input("Enter your own Matrix to encode: ")
                while gcd(Matrix(ast.literal_eval(matrix)).det(), 94) != 1:
                    matrix = input("Enter your own Matrix to encode: ")
                invMatrix = Matrix(ast.literal_eval(matrix)).inv_mod(94)
                case = "e"

            elif userInput == "d":
                invMatrix = input("Enter your own Inverse Matrix to decode: ")
                if not is_square_matrix(invMatrix):
                    while not is_square_matrix(invMatrix):
                        invMatrix = input("Enter your own Inverse Matrix to decode: ")
                case = "d"

    elif dim.isnumeric():
        matrix, invMatrix = keyGenerator(int(dim))
        case = "dim"
    else:
        while not (dim.isnumeric() or not dim):
            dim = input("Enter the Dimension of the Matrix to encode/decode to get a random generated one. \n"
                        "For a Dimension > 10 it will be slower to generate a working Matrix. \n"
                        "Enter nothing if you want to use your own Matrix: ")

        if not dim:
            userInput = input("To encode enter e, to decode enter d: ")
            if userInput == "e":
                matrix = input("Enter your own Matrix to encode: ")
                if not is_square_matrix(matrix):
                    while not is_square_matrix(matrix):
                        matrix = input("Enter your own Matrix to encode: ")
                while gcd(Matrix(ast.literal_eval(matrix)).det(), 94) != 1:
                    matrix = input("Enter your own Matrix to encode: ")
                invMatrix = Matrix(ast.literal_eval(matrix)).inv_mod(94)
                case = "e"

            elif userInput == "d":
                invMatrix = input("Enter your own Inverse Matrix to decode: ")
                if not is_square_matrix(invMatrix):
                    while not is_square_matrix(invMatrix):
                        invMatrix = input("Enter your own Inverse Matrix to decode: ")
                case = "d"
            else:
                while userInput not in ["e", "d"]:
                    userInput = input("To encode enter e, to decode enter d: ")
                if userInput == "e":
                    matrix = input("Enter your own Matrix to encode: ")
                    if not is_square_matrix(matrix):
                        while not is_square_matrix(matrix):
                            matrix = input("Enter your own Matrix to encode: ")
                    while gcd(Matrix(ast.literal_eval(matrix)).det(), 94) != 1:
                        matrix = input("Enter your own Matrix to encode: ")
                    invMatrix = Matrix(ast.literal_eval(matrix)).inv_mod(94)
                    case = "e"
                elif userInput == "d":
                    invMatrix = input("Enter your own Inverse Matrix to decode: ")
                    if not is_square_matrix(invMatrix):
                        while not is_square_matrix(invMatrix):
                            invMatrix = input("Enter your own Inverse Matrix to decode: ")
                    case = "d"
        else:
            matrix, invMatrix = keyGenerator(int(dim))
            case = "dim"

    if case == "dim":
        text = input("Enter the text you want to encode and decode: ")
        print("Matrix:")
        print(matrix)
        print("")
        pprint(matrix)
        print("")
        print("Inverse:")
        print(invMatrix)
        print("")
        pprint(invMatrix)
        print("")
        encoded = encode(text, matrix)
        decoded = decode(encoded, invMatrix)
        print("Original Text: " + text)
        print("Verschluesselter Text: " + encoded)
        print("Entschluesselter Text: " + decoded)
    elif case == "e":
        text = input("Enter the text you want to encode: ")
        print("Matrix:")
        print(matrix)
        print("")
        pprint(Matrix(ast.literal_eval(str(matrix))))
        print("")
        print("Inverse:")
        print(invMatrix)
        print("")
        pprint(invMatrix)
        print("")
        encoded = encode(text, matrix)
        print("Original Text: " + text)
        print("Verschluesselter Text: " + encoded)

    elif case == "d":
        text = input("Enter the text you want to decode: ")
        print("Inverse:")
        print(invMatrix)
        print("")
        pprint(Matrix(ast.literal_eval(str(invMatrix))))
        print("")
        decoded = decode(text, invMatrix)
        print("Original Text: " + text)
        print("Entschluesselter Text: " + decoded)


start()
