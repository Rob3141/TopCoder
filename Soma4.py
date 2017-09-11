from copy import deepcopy

# function to translate in direction of given axis (back to front)
def translate(piece,distance, ax):

    for i in range(0,len(piece)):
        if piece[i][ax] + distance > 2 or piece[i][ax] + distance < 0:
            return 0
        else:
            piece[i][ax] += distance

    return piece

# currently checks along x dimension but doesn't check along any other
# dimension
def addpieces(pieceList):

    # cube to record which spaces have been occupied by pieces and which haven't
    cube = [[[0 for i in range(1,4)] for i in range(1,4)] for i in range(1,4)]

    for j in range(0,len(pieceList)):
        # Assumes piece is in format of list of x, y, z co-ordinates
        # Checks whether any spaces in the cube are already occupied
        for i in range(0, len(pieceList[j])):
            if cube[pieceList[j][i][2]][pieceList[j][i][1]][pieceList[j][i][0]] == 1:
                    return

        # Now have checked that piece does not clash with the cube we can
        # go ahead and add it
        for i in range(0, len(pieceList[j])):
            cube[pieceList[j][i][2]][pieceList[j][i][1]][pieceList[j][i][0]] = 1

    return cube

# function that takes a piece and number of desired rotations and then returns
# the cordinates of the rotated piece based on the number of rotations req'd
def rotation(rotations, listCoords, ax):

    xmatrix = [[1,0,0],[0,0,1],[0,-1,0]]
    ymatrix = [[0,0,-1],[0,1,0],[1,0,0]]
    zmatrix = [[0,1,0],[-1,0,0],[0,0,1]]

    if ax == 1:
        matrix = xmatrix
    elif ax == 2:
        matrix = ymatrix
    elif ax == 3:
        matrix = zmatrix

    rotCoords = []

    for j in range(0,len(listCoords)):

        i = 0
        rotCoords.append(listCoords[j])
        while(i < rotations):
            rotCoords[j] = matrixMult(rotCoords[j],matrix)
            i += 1

    return rotCoords

# function that takes co-ordinates and matrix and multiplies the two together
# returns resulting co-ordinates
def matrixMult(coords,matrix):
    resultCoords = [0,0,0]

    for i in range(0,3):
        for j in range(0,3):
            resultCoords[i] += coords[j]*matrix[j][i]

    return resultCoords

# function to obtain x,y and z co-ordinates based on spaces occupied within
# the cube. Assumes that (0,0,0) is at the centre of the cube so that
# rotated pieces are not outside of the cube
def coordsConv(piece):
    listCoords = []

    for z in range(0,3):
        for y in range(0,3):
            for x in range(0,3):
                if piece[z][y][x] == 1:
                    listCoords.append([x-1,y-1,z-1])

    return listCoords

# generate different combinations of x,y,z rotations and return combinations
# in a list
def pieceGen(piece):
    stack = []
    listCoords = coordsConv(piece)
    rotations = []

    for i in range(0,4):
        for j in range(0,4):
            for k in range(0,4):
                stack.append([i,j,k])

    for i in range(0,len(stack)):
        listCoordsTemp = deepcopy(listCoords)
        listCoordsTemp = rotation(stack[i][0],listCoordsTemp,1)
        listCoordsTemp = rotation(stack[i][1],listCoordsTemp,2)
        listCoordsTemp = rotation(stack[i][2],listCoordsTemp,3)

        # in between i = 0 and i = 1 listCoords changes?!
        for k in range(0,len(listCoordsTemp)):
            for j in range(0,3):
                listCoordsTemp[k][j] += 1

        # eliminate duplicates by only adding if not already in the list
        if listCoordsTemp not in rotations:
            rotations.append(listCoordsTemp)

    for i in range(0,len(rotations)):
        for k in range(0,len(stack)):
            listCoordsTemp = deepcopy(rotations[i])

            if translate(listCoordsTemp,stack[k][0],0) == 0:
                listCoordsTemp = deepcopy(rotations[i])
            if translate(listCoordsTemp,stack[k][1],1) == 0:
                listCoordsTemp = deepcopy(rotations[i])
            if translate(listCoordsTemp,stack[k][2],2) == 0:
                listCoordsTemp = deepcopy(rotations[i])

            if listCoordsTemp not in rotations:
                rotations.append(listCoordsTemp)

    for i in range(0,len(rotations)):
        for k in range(0,len(stack)):
            listCoordsTemp = deepcopy(rotations[i])

            if translate(listCoordsTemp,-stack[k][0],-0) == 0:
                listCoordsTemp = deepcopy(rotations[i])
            if translate(listCoordsTemp,-stack[k][1],-1) == 0:
                listCoordsTemp = deepcopy(rotations[i])
            if translate(listCoordsTemp,-stack[k][2],-2) == 0:
                listCoordsTemp = deepcopy(rotations[i])

            if listCoordsTemp not in rotations:
                rotations.append(listCoordsTemp)


    return rotations

def cubeGen(piecelist):

    # new list to store all possible permuations for each piece
    GenPieceList = []
    # list to store selected permutation for each 7 pieces
    TrialPieces = []

    # use pieceGen function to generate permutations for each of the pieces
    # add the set of permutations for each piece as a separate list
    for piece in piecelist:
        GenPieceListTemp = []
        for generatedPiece in pieceGen(piece):
            GenPieceListTemp.append(generatedPiece)
        GenPieceList.append(GenPieceListTemp)

    # stack now contains all permutations for each piece
    GenPieceStack = deepcopy(GenPieceList)

    # generate initial try by popping from each piece permutation list
    for i in range(0,len(GenPieceStack)):
        TrialPieces.append(GenPieceStack[i].pop())

    # once all permutations for piece 1 have been explored, terminate the loop
    while(GenPieceStack[0] != []):
        # start by trying to add first two piece permutations
        # if successful then try adding the first three and so on...
        # if counter hits 7 then all 7 pieces add together
        counter = 2
        while(addpieces(TrialPieces[:counter]) != None):
            counter += 1
            if counter == 7:
                print "success"
                print TrialPieces
                print " "
                
        # assuming adding all 7 pieces has failed, then the counter records the
        # piece that didn't fit

        # if permutations for piece which failed not empty, then move onto next
        # piece
        if GenPieceStack[counter-1] != []:
            TrialPieces[counter-1] = GenPieceStack[counter-1].pop()
            # Reset to list of complete permutations for subsequent pieces
            for i in range(counter,7):
                GenPieceStack[i] = deepcopy(GenPieceList[i])
                TrialPieces.append(GenPieceStack[i].pop())
        # else permutations for piece which failed is empty
        else:
            # starting from position one in list check whether stack
            # is empty if so, move onto next position in n-1 and refresh all
            # downstream permutations
            flag = 0
            counter = 0
            while(flag == 0):
                if GenPieceStack[counter] == []:
                    print counter
                    TrialPieces[counter-1] = GenPieceStack[counter-1].pop()
                    flag = 1

                    for i in range(counter,7):
                        GenPieceStack[i] = deepcopy(GenPieceList[i])
                        TrialPieces.append(GenPieceStack[i].pop())
                else:
                    counter += 1

# order of co-ordinates are z,y,x
twodimensions = [[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
piece1 = [[1,1,1],[1,0,0],[0,0,0]]
piece2 = [[1,1,1],[0,1,0],[0,0,0]]
piece3 = [[0,1,1],[1,1,0],[0,0,0]]
piece4 = [[1,1,0],[1,0,0],[0,0,0]]

piece1 = [piece1] + twodimensions
piece2 = [piece2] + twodimensions
piece3 = [piece3] + twodimensions
piece4 = [piece4] + twodimensions

thirddimension = [[0,0,0],[0,0,0],[0,0,0]]
piece5 = [[[0,1,0],[1,1,0],[0,0,0]],[[0,1,0],[0,0,0],[0,0,0]]]
piece6 = [[[1,0,0],[1,1,0],[0,0,0]],[[1,0,0],[0,0,0],[0,0,0]]]
piece7 = [[[1,1,0],[0,1,0],[0,0,0]],[[0,1,0],[0,0,0],[0,0,0]]]

piece5.append(thirddimension)
piece6.append(thirddimension)
piece7.append(thirddimension)

pieceList = [piece1,piece2,piece3,piece4,piece5,piece6,piece7]

# first dimension is back wall and last dimension is front wall
pattern = [[3,3,3],[3,3,3],[3,3,3]]

print cubeGen(pieceList)
