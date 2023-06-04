from sympy import *
import matplotlib.pyplot as plt
import numpy as np
import re
import ast


# rotates the passed list of points by the given angle in degrees
def rotateMatrix(points, alphaDeg):
    alphaRad = alphaDeg * pi / 180
    newMatrix = []
    rotate = Matrix([[cos(alphaRad), -sin(alphaRad)], [sin(alphaRad), cos(alphaRad)]])
    for i in range(len(points)):
        rotated = rotate * transpose(Matrix([points[i]]))
        newMatrix.append([rotated[0], rotated[1]])

    return newMatrix


# scales the points list with the given lambda value
def scaleMatrix(points, lambdaValue):
    newMatrix = []
    scale = Matrix([[lambdaValue, 0], [0, lambdaValue]])
    for i in range(len(points)):
        scaled = Matrix([points[i]]) * scale
        newMatrix.append([scaled[0], scaled[1]])

    return newMatrix


# mirrors the points list on the given axis x, y or the origin line with the given angle
# to the x-axis
def mirrorMatrix(points, axis):
    newMatrix = []
    if axis == "x" or axis == "y":
        if axis == "x":
            mirror = Matrix([[1, 0], [0, -1]])
            for i in range(len(points)):
                mirrored = (Matrix([points[i]])) * mirror
                newMatrix.append([mirrored[0], mirrored[1]])
        elif axis == "y":
            mirror = Matrix([[-1, 0], [0, 1]])
            for i in range(len(points)):
                mirrored = (Matrix([points[i]])) * mirror
                newMatrix.append([mirrored[0], mirrored[1]])
    else:
        alphaRad = int(axis) * pi / 180
        mirror = Matrix([[cos(2 * alphaRad), sin(2 * alphaRad)], [sin(2 * alphaRad), -cos(2 * alphaRad)]])
        for i in range(len(points)):
            mirrored = (Matrix([points[i]])) * mirror
            newMatrix.append([mirrored[0], mirrored[1]])
        newMatrix.append(alphaRad)
    return newMatrix


# plots the two lists
def plotPoints(pointsList, newPointsList):
    # plottet die originale Liste
    for j in range(len(pointsList)):
        if j == len(pointsList) - 1:
            x_values = [pointsList[j][0], pointsList[0][0]]
            y_values = [pointsList[j][1], pointsList[0][1]]
            plt.plot(x_values, y_values, color="r", label="before", linestyle="-")


        else:
            x_values = [pointsList[j][0], pointsList[j + 1][0]]
            y_values = [pointsList[j][1], pointsList[j + 1][1]]
            plt.plot(x_values, y_values, color="r", label="before", linestyle="-")

    lenNewPointsList = len(newPointsList)
    # checks if the length of the new list is greater than that of the original, because when mirroring
    # on any axis, the angle of the axis to the x-axis is stored at the last position
    # to be able to draw this axis later on
    if len(pointsList) != len(newPointsList):
        lenNewPointsList = len(newPointsList) - 1

    # plots the second list
    for j in range(lenNewPointsList):
        if j == lenNewPointsList - 1:
            x_values = [newPointsList[j][0], newPointsList[0][0]]
            y_values = [newPointsList[j][1], newPointsList[0][1]]
            plt.plot(x_values, y_values, color="g", label="after", linestyle="-")

        else:
            x_values = [newPointsList[j][0], newPointsList[j + 1][0]]
            y_values = [newPointsList[j][1], newPointsList[j + 1][1]]
            plt.plot(x_values, y_values, color="g", label="after", linestyle="-")

    ax = plt.gca()
    # equals the scaling of the two axes
    ax.set_aspect('equal', adjustable='box')

    # Make the upper and right axes invisible:
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Place the left diagram axis on the reference point '0' of the x-axis:
    ax.spines['left'].set_position(('data', 0))

    # Place the lower diagram axis on the reference point '0' of the y-axis:
    ax.spines['bottom'].set_position(('data', 0))

    # when mirrored on any axis, draws this axis in the plot
    if lenNewPointsList is not len(newPointsList):
        xmin, xmax = ax.get_xlim()
        x = np.linspace(xmin, xmax, 10)
        y = x * tan(newPointsList[lenNewPointsList])
        plt.plot(x, y, color="b", label="mirrorAxis")

    # Activates a grid as plot background
    plt.grid()

    # shows the plot
    plt.show()


def checkAndUseMatrix(pointsList):
    newPointsList = None
    method = input("Enter how you want to change the matrix: m for mirror, r for rotate and s for scale: ")

    if method == "s":
        lambdaValue = input("Enter the lambda value to scale your matrix with: ")
        # isNumeric() checks if the string contains only numbers. Negative or comma numbers are not numbers because they
        # contain "-" and ".".
        check = lambdaValue.isnumeric()
        if not lambdaValue.isnumeric():
            # regex expression for comma and negative numbers
            check = re.match("^[-\.\d]+[,]?[\d]*[\.]?[\d]?$", lambdaValue)

        while not check:
            lambdaValue = input("Enter the lambda value to scale your matrix with: ")
            check = lambdaValue.isnumeric()
            if not lambdaValue.isnumeric():
                check = re.match("^[-\.\d]+[,]?[\d]*[\.]?[\d]?$", lambdaValue)

        newPointsList = scaleMatrix(pointsList, float(lambdaValue))
    elif method == "r":
        alphaDeg = input("Enter with how many degrees you want to rotate your matrix: ")
        # as degree of an angle only integer positive values allowed
        while not alphaDeg.isnumeric():
            alphaDeg = input("Enter with how many degrees you want to rotate your matrix: ")
        newPointsList = rotateMatrix(pointsList, int(alphaDeg))
    elif method == "m":
        axis = input("Enter the axis to mirror your matrix: x, y or number of degree for axis gradient: ")
        # The axis is x or y or a degree value as an angle to the x-axis
        while not (axis == "x" or axis == "y" or axis.isnumeric()):
            axis = input("Enter the axis to mirror your matrix: x, y or number of degree for axis gradient: ")

        newPointsList = mirrorMatrix(pointsList, axis)

    return newPointsList


def start():
    pointsList = input("Enter your PointsList with following syntax: [[x1, y1], [x2, y2],...] or nothing for default: ")

    # default List
    if not pointsList:
        pointsList = [[1, 1], [5, 1], [5, 5], [3, 8], [1, 5], [5, 5], [1, 1], [1, 5], [5, 1]]

    # pattern for [[x1, y1], [x2, y2], ...]
    pattern = r'\[\[\d+,\s*\d+\](,\s*\[\d+,\s*\d+\])*\]'

    # checks if the input corresponds to such a list like the pattern
    while not re.match(pattern, str(pointsList)):
        pointsList = input("Enter your PointsList with following syntax: [[x1, y1], [x2, y2],...] or nothing for "
                           "default: ")
        if not pointsList:
            pointsList = [[1, 1], [5, 1], [5, 5], [3, 8], [1, 5], [5, 5], [1, 1], [1, 5], [5, 1]]

    # converts the input string with the pattern of a list, to a list
    pointsList = ast.literal_eval(str(pointsList))

    # input check method
    newPointsList = checkAndUseMatrix(pointsList)

    while newPointsList is None:
        newPointsList = checkAndUseMatrix(pointsList)

    # plot function is called
    plotPoints(pointsList, newPointsList)


start()
