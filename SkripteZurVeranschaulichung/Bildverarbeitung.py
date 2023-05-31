from sympy import *
import matplotlib.pyplot as plt
import numpy as np
import re
import ast


# rotiert die übergebene Liste an Punkten um den gegebenen Winkel in Grad
def rotateMatrix(points, alphaDeg):
    alphaRad = alphaDeg * pi / 180
    newMatrix = []
    rotate = Matrix([[cos(alphaRad), -sin(alphaRad)], [sin(alphaRad), cos(alphaRad)]])
    for i in range(len(points)):
        rotated = Matrix([points[i]]) * rotate
        newMatrix.append([rotated[0], rotated[1]])

    return newMatrix


# skaliert die points Liste mit dem gegebenen Lambda Wert
def scaleMatrix(points, lambdaValue):
    newMatrix = []
    scale = Matrix([[lambdaValue, 0], [0, lambdaValue]])
    for i in range(len(points)):
        scaled = Matrix([points[i]]) * scale
        newMatrix.append([scaled[0], scaled[1]])

    return newMatrix


# spiegelt die points Liste an der übergebenen Achse x, y oder die Ursprungsgerade mit dem angegebnenen Winkel zur x-Achse
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


# plottet die beiden listen
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
    # ueberprueft ob die laenge der neuen Liste groeßer ist als die der Originalen, denn bei der Spiegelung
    # an einer beliebigen Achse wird der Winkel der Achse zur x-Achse an der letzten Stelle gespeichert
    # um diese Achse spaeter zeichnen zu koennen
    if len(pointsList) != len(newPointsList):
        lenNewPointsList = len(newPointsList) - 1

    # plottet die zweite Liste
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
    # setzt die scalierung der beiden Achsen gleich
    ax.set_aspect('equal', adjustable='box')

    # Die obere und rechte Achse unsichtbar machen:
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Die linke Diagrammachse auf den Bezugspunkt '0' der x-Achse legen:
    ax.spines['left'].set_position(('data', 0))

    # Die untere Diagrammachse auf den Bezugspunkt '0' der y-Achse legen:
    ax.spines['bottom'].set_position(('data', 0))

    # zeichnet bei Spiegelung an einer beliebigen Achse diese Achse in den Plot ein
    if lenNewPointsList is not len(newPointsList):
        xmin, xmax = ax.get_xlim()
        x = np.linspace(xmin, xmax, 10)
        y = x * tan(newPointsList[lenNewPointsList])
        plt.plot(x, y, color="b", label="mirrorAxis")

    # Aktiviert ein Grid als Plot Hintergrund
    plt.grid()


    # Zeigt den Plot
    plt.show()


def start():
    pointsList = input("Enter your PointsList with following syntax: [[x1, y1], [x2, y2],...] or nothing for default: ")

    # default Liste
    if not pointsList:
        pointsList = [[1, 1], [5, 1], [5, 5], [3, 8], [1, 5], [5, 5], [1, 1], [1, 5], [5, 1]]

    # Pattern für [[x1, y1], [x2, y2], ...]
    pattern = r'\[\[\d+,\s*\d+\](,\s*\[\d+,\s*\d+\])*\]'

    # prueft, ob der Input einer solchen Liste wie das Pattern entspricht
    while not re.match(pattern, str(pointsList)):
        pointsList = input("Enter your PointsList with following syntax: [[x1, y1], [x2, y2],...] or nothing for "
                           "default: ")
        if not pointsList:
            pointsList = [[1, 1], [5, 1], [5, 5], [3, 8], [1, 5], [5, 5], [1, 1], [1, 5], [5, 1]]

    # konvertiert den eingebenen String mit dem Pattern einer Liste, zu einer Liste
    pointsList = ast.literal_eval(str(pointsList))
    method = input("Enter how you want to change the matrix: m for mirror, r for rotate and s for scale: ")
    newPointsList = []

    if method == "s":
        lambdaValue = input("Enter the lambda value to scale your matrix with: ")
        # isNumeric() ueberprueft ob der String nur Zahlen enthaelt. Negative oder Kommazahlen sind keine Zahlen da sie
        # "-" und "." enthaltenb
        check = lambdaValue.isnumeric()
        if not lambdaValue.isnumeric():
            # regex Ausdruck für Komma und negative Zahlen
            check = re.match("^[-\.\d]+[,]?[\d]*[\.]?[\d]?$", lambdaValue)

        while not check:
            lambdaValue = input("Enter the lambda value to scale your matrix with: ")
            check = lambdaValue.isnumeric()
            if not lambdaValue.isnumeric():
                check = re.match("^[-\.\d]+[,]?[\d]*[\.]?[\d]?$", lambdaValue)

        newPointsList = scaleMatrix(pointsList, float(lambdaValue))
    elif method == "r":
        alphaDeg = input("Enter with how many degrees you want to rotate your matrix: ")
        # als Grad eines Winkels nur ganzzahlige positive Werte erlaubt
        while not alphaDeg.isnumeric():
            alphaDeg = input("Enter with how many degrees you want to rotate your matrix: ")
        newPointsList = rotateMatrix(pointsList, int(alphaDeg))
    elif method == "m":
        axis = input("Enter the axis to mirror your matrix: x, y or number of degree for axis gradient: ")
        # Die Achse ist x oder y oder ein Grad Wert als Winkel zur x-Achse
        while not (axis == "x" or axis == "y" or axis.isnumeric()):
            axis = input("Enter the axis to mirror your matrix: x, y or number of degree for axis gradient: ")

        newPointsList = mirrorMatrix(pointsList, axis)
    else:
        while method not in ["m", "r", "s"]:
            method = input("Please enter m, r or s: ")
            if method == "s":
                lambdaValue = input("Enter the lambda value to scale your matrix with: ")
                check = lambdaValue.isnumeric()
                if not lambdaValue.isnumeric():
                    check = re.match("^[-\.\d]+[,]?[\d]*[\.]?[\d]?$", lambdaValue)

                while not check:
                    lambdaValue = input("Enter the lambda value to scale your matrix with: ")
                    check = lambdaValue.isnumeric()
                    if not lambdaValue.isnumeric():
                        check = re.match("^[-\.\d]+[,]?[\d]*[\.]?[\d]?$", lambdaValue)

                newPointsList = scaleMatrix(pointsList, float(lambdaValue))
            elif method == "r":
                alphaDeg = input("Enter with how many degrees you want to rotate your matrix: ")
                while not alphaDeg.isnumeric():
                    alphaDeg = input("Enter with how many degrees you want to rotate your matrix: ")
                newPointsList = rotateMatrix(pointsList, int(alphaDeg))
            elif method == "m":
                axis = input("Enter the axis to mirror your matrix: x, y or number of degree for axis gradient: ")
                while not (axis == "x" or axis == "y" or axis.isnumeric()):
                    axis = input("Enter the axis to mirror your matrix: x, y or number of degree for axis gradient: ")

                newPointsList = mirrorMatrix(pointsList, axis)

    # plot Funktion wird aufgerufen
    plotPoints(pointsList, newPointsList)


start()
