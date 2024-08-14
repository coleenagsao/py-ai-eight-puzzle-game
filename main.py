# Exercise 3: A* Search (Agsao, Coleen Therese - CMSC 170 X2L)

#Before running: Install pygame and pygame_widgets

#import python libraries
import numpy as np                                  #import library to be used in returning an index of a specific element of a 2D Array
import copy                                         #import library to be used to copy an array

import pygame                                       #import library to be used UI
pygame.font.init()                                  # initialize font module

import pygame_widgets                               #import library to be used for dropdown and buttons
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

import tkinter                                     #import library for file dialog box
import tkinter.filedialog
#import time

BG_COLOR = (0, 0, 0)
LINE_COLOR = (54, 126, 24)
HOVER_COLOR = (54, 180, 24)
CLICK_COLOR = (54, 220, 24)
GOAL_STATE = [[1,2,3],[4,5,6],[7,8,0]]

#function that accepts a state and generates a list containing all possible actions that can be done in the state
def Action(state):
    index = indexLocator(state, 0)                 #store index of zero in variable index
    actions = []

    if index not in [(0, 0), (0, 1), (0, 2)]:   #check if index of zero is located in the uppermost part
        actions.append("U")
    if index not in [(0, 2), (1, 2), (2, 2)]:   #check if index of zero is located in the rightmost part
        actions.append("R")
    if index not in [(2, 0), (2, 1), (2, 2)]:   #check if index of zero is located in the bottom part
        actions.append("D")
    if index not in [(0, 0), (1, 0), (2, 0)]:   #check if index of zero is located in the leftmost part
        actions.append("L")

    return actions                              #return the list of possible actions

#function that generates a new state based on the action inputted with g, h, f
def Result(puzzle, action):
    index = indexLocator(puzzle.state, 0)          #store index of zero in variable index
    row, col = index[0], index[1]               #assign content of tuple as row and col
    newState = copy.deepcopy(puzzle.state)      #create another clone of the state, prevents the original state from being changed/manipulated

    if action == "U": #swap zero and the element above it
        newState[row][col], newState[row - 1][col] = newState[row - 1][col], newState[row][col]
    elif action == "R": #swap zero and the element in its right
        newState[row][col], newState[row][col + 1] = newState[row][col + 1], newState[row][col]
    elif action == "D": #swap zero and the element below it
        newState[row][col], newState[row+1][col] = newState[row + 1][col], newState[row][col]
    elif action == "L": #swap zero and the element in its left
        newState[row][col], newState[row][col - 1] = newState[row][col - 1], newState[row][col]

    newStateNode = State(newState, indexLocator(newState, 0), action, puzzle, 0, 0, 0) #create a State with the new 2D array generated
    g = computeG(newStateNode, game.initialState)                                   #call function that computes g of the state
    newStateNode.g = g

    h = computeH(newState)                                                          #call function for h that will save to newState.h
    newStateNode.h = h
    newStateNode.f = g + h                                                          #add g and h for f

    return newStateNode #return a new Node

#function that checks if the goal state is already reached
def GoalTest(currentState):
    GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]          #initialize the target state
    state = currentState.state                              #save the puzzle pattern in state variable to be used for comparing
    matchCount = 0                                          #initialize variable that will keep track number of elements matched in the goal state

    for row, x in enumerate(state):                         # iterate through the 2D array having row (index) and x (element)
        for col, tile in enumerate(x):                      # enumerate every element in self.tilesGrid
            if state[row][col] == GOAL_STATE[row][col]:     # check if elements are matched with the winning array
                matchCount += 1

    if matchCount == 9:                                     #if all matched, then return true
        print("[DONE] Search is done.")
        return True
    else:
        return False

#function that returns the number of actions taken
def PathCost(path):
    cost = len(path)
    return cost

# [function for BFS] mimic the enqueue by adding in the last portion
def enqueue(frontier, puzzle):
    frontier.append(puzzle)

# [function for BFS] mimic the dequeue by removing the first element
def dequeue(frontier):
    return frontier.pop(0)

# [function for BFS] implement BFSearch which uses queue
def BFSearch(initialState):
    frontier = [initialState]                   #add initial state node as the initial element of frontier
    frontierPuzzles = [initialState.state]      #store puzzles contained in frontier for the checking if in explored or frontier
    explored = []                               #initialize an empty list to contain explored nodes

    while len(frontier) != 0:                   #create loop that only stops once frontier is empty or goal state is already reached
        currentState = dequeue(frontier)        #pop out the first element in the list
        explored.append(currentState.state)     #add puzzle to the explored states' puzzle
        frontierPuzzles.pop(0)
        if GoalTest(currentState):              #call function that checks if goal state is already reached
            print("[EXPLORED STATES] " + str(len(explored)))
            return currentState
        else:
            for action in Action(currentState.state):                                                      #iterate through the action in the list generated from function Action()
                newState = Result(currentState, action)
                if newState.state not in explored and newState.state not in frontierPuzzles:               #check if not yet explored and inside frontier
                    frontierPuzzles.append(newState.state)                                                                    #add newly generated puzzles in node in frontierPuzzle for tracking
                    enqueue(frontier, Result(currentState, action))                                        #if satisfied, add new states based on the actions

# [function for DFS] mimic the push in stack
def push(frontier, puzzle):
    frontier.append(puzzle)                     #adds to the last element of frontier

# [function for DFS] mimic the pop in stack
def pop(frontier):
    return frontier.pop(-1)                     #removes the last element of frontier

# [function for DFS] implement the depth-first search which implements stack
def DFSearch(initialState):
    frontier = [initialState]                   #add initial state node as the initial element of frontier
    frontierPuzzles = [initialState.state]      #store puzzles contained in frontier for the checking if in explored or frontier
    explored = []                               #initialize an empty list to contain explored nodes

    while len(frontier) != 0:                   #create loop that only stops once frontier is empty or goal state is already reached
        currentState = pop(frontier)            #pop out the first element in the list
        explored.append(currentState.state)     #add puzzle to the explored states' puzzle
        frontierPuzzles.pop(0)
        if GoalTest(currentState):              #call function that checks if goal state is already reached
            print("[EXPLORED STATES] " +  str(len(explored)))
            return currentState
        else:
            for action in Action(currentState.state):                                                               #iterate through the action in the list generated from function Action()
                newState = Result(currentState, action)
                if newState.state not in explored and newState.state not in frontierPuzzles:                        #check if not yet explored and inside frontier
                    frontierPuzzles.append(newState.state)                                                          #add newly generated puzzles in node in frontierPuzzle for tracking
                    push(frontier, Result(currentState, action))                                                    #if satisfied, add new states based on the actions

#[function for A*] function that counts the number of paths from initial State to the current State
def computeG(currentState, initialState):
    g = 1                                    #initialize variable g to store path cost from initial state to current state
    tempParent = currentState.parentPointer  #create a temp pointer to hold the node of the currentState's parent

    while (arrCompare(tempParent.state,initialState.state) == False):   #continue as long as loop have not reached the root (initial state)
        g += 1                                                          #increment the number of paths taken
        tempParent = tempParent.parentPointer                           # change the tempParent to the parent's parent pointer

    return g

#[function for A*] compute for the manhattan distance of each number (1-8) and adds it to get the H
def computeH(currentState):
    h = 0
    for i in range(1, 9):
        currentPos = indexLocator(currentState, i)                                      #get index of each number in the current State
        correctPos = indexLocator(GOAL_STATE, i)                                        #get index of each number in the correct State

        currentPosX, currentPosY = currentPos[0], currentPos[1]                         #get the x, y in the array
        correctPosX, correctPosY = correctPos[0], correctPos[1]

        h += abs((currentPosX - correctPosX)) + abs((currentPosY - correctPosY))        #compute the manhattan distance through |x2 - x1| + |y2 - y1| then add to original counter

    return h

#[function for A*] get the minimum f in the openList then remove it from the list
def removeMinF(openList):
    bestNode = State(None, None, None, None, None, None, None)  #initialize an empty State
    indexofMinF = 0                                     # initialize index of MinF as first index of list which is 0

    if len(openList) != 1 and len(openList) != 0:       #if openList contains 2 or more elements, proceed
        minF = openList[0].f                            #get f of the first state in the open list to be used for comparison

        #get the minimum F
        for i, state in enumerate(openList):            #iterate through the openList
            minF = min(state.f, minF)                   #get minimum from the two values
            if minF == state.f:                         #if it is the same node, save the index of the current index of State with minF
                indexofMinF = i

        bestNode = openList.pop(indexofMinF)            #save the state with the minimum F

    elif len(openList) == 1:
        bestNode = openList.pop(0)

    result = [bestNode, indexofMinF]                    #returns a list with the bestNode and index of node with minimum f is to be used later for tracking
    return result

#[function for A*] check if nodes with duplicates have g larger than the new one generated
def getDuplicate(openList, x):
    for i in openList:
        if arrCompare(i.state, x.state):    #if a duplicate is found, compare their g
            if x.g < i.g:                   #if the duplicated.g is larger then return true
                return True
            else:
                return False
        else:
            return False

#[function for A*] implement the A* search
def ASearch(initialState):
    openList = [initialState]                   #initialize list to contain the openList nodes
    openListPuzzle = [initialState.state]       #initiallize list to contain the openList puzzles for comparing
    closedList = []                             #create an empty list for states to be explored

    while len(openList) != 0:
        bestNodeResult = removeMinF(openList)                           #get the node with the least F by calling the function that returns the best node for us with the index
        bestNode, indexofMinF = bestNodeResult[0], bestNodeResult[1]

        openListPuzzle.pop(indexofMinF)                                 #since bestNode is removed from the list, the equivalent puzzle in the same order will be removed
        closedList.append(bestNode.state)                               #add to the list of explored states

        if GoalTest(bestNode):
            print("[EXPLORED STATES] " + str(len(closedList)))
            return bestNode

        for action in Action(bestNode.state):
            x = Result(bestNode, action)
            if ((x.state not in (closedList or openList)) or (x.state in openList and getDuplicate(openList, x))):  #if newPuzzle is not in closed
                openList.append(x)
                openListPuzzle.append(x.state)


#function that returns the path from the initial state to the goal state and creates the .out puzzle with the answer
def traceBack(currentState, initialState):
    tempParent = currentState.parentPointer       #create a temp pointer to hold the node of the currentState's parent
    actions = [currentState.action]             #initialize an actions list with the current state's action as its first element since it will not be part of the iteration

    while (arrCompare(tempParent.state, initialState.state) == False): #continue as long as loop have not reached the root (initial state)
        actions.append(tempParent.action)               #add the action of the parent puzzle in the list
        tempParent = tempParent.parentPointer           #change the tempParent to the parent's parent pointer

    actions.reverse()           #reverse the array of actions, will be in the same array

    f = open("puzzle.out", "w") #create a new file named "puzzle.out"

    for i in actions:
        f.write(i + " ")

    return actions #returns the path

#function that returns a list of UI elements for the display of actions
def createList(path):
    listElements = []
    x = 450
    y = 250

    for i in path:
        if x > 945:                                 #if x is already outside the screen, reset x and move 20 units down
            x = 450
            y = 270

        actionElement = Element(x, y, i, 18)        #create an action text element then append to the listElement
        listElements.append(actionElement)
        x += 15

    return listElements

#function that returns the index of a number in a given puzzle
def indexLocator(puzzle, index):
    array = np.array(puzzle)
    loc = list(zip(*np.where(array == index)))[0]
    return loc

#function that compares two 2D arrays
def arrCompare(arr1, arr2):
    matchCount = 0

    for row, x in enumerate(arr1):                  #loop through the array (row (index) i (element))
        for col, tile in enumerate(x):              #enumerate every element inn self.tilesGrid
            if arr1[row][col] == arr2[row][col]:    # check if elements are matched with the winning array
                matchCount += 1

    if matchCount == 9:
        return True
    else:
        return False

#check if puzzle is solvable or not
def getInvCount(arr):                                               # create function that counts the number of inversions
    invCount, emptyValue  = 0, 0
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != emptyValue and arr[i] != emptyValue and arr[i] > arr[j]: # check if element is greater than elements next to it
                invCount += 1
    return invCount

def isSolvable(puzzle):                                             # create function that returns true if given 8 puzzle is solvable.
    invCount = getInvCount([j for i in puzzle for j in i])          # count inversions in given 8-puzzle
    return (invCount % 2 == 0)                                      # return true if inversion count is even.

#classes
class State:
    def __init__(self, state, emptyLoc, action, parent, g, h, f):
        self.state, self.emptyLoc, self.action, self.parentPointer, self.g, self.h, self.f = state, emptyLoc, action, parent, g, h, f

class Element:                                                      # class for the UI text element
    def __init__(self, x, y, text, fontSize):
        self.x, self.y, self.text, self.fontSize = x, y, text, fontSize

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", self.fontSize)       # create a font object
        text = font.render(self.text, True, LINE_COLOR)             # create surface with specified text rendered
        screen.blit(text, (self.x, self.y))                         # draws text surface to the screen

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, num):
        self.x, self.y, self.game, self.num = x, y, game, num
        self.groups = game.allSprites                               # create group that takes all of the sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface([128, 128])                     # creates a new image object for the tile
        self.rect = self.image.get_rect()

        if self.num != 0:
            self.image.fill(LINE_COLOR)                                 # set color of the tile

            self.font = pygame.font.SysFont("Montserrat", 60)
            self.fontSize = self.font.size(str(self.num))                    # return a tuple of font size height and weight
            fontX = (128 / 2) - self.fontSize[0] / 2                    # return x, y coordinate in the center of the tile
            fontY = (128 / 2) - self.fontSize[1] / 2
            fontSurface = self.font.render(str(self.num), True, BG_COLOR)    # set color of the text
            self.image.blit(fontSurface, (fontX, fontY))                # draws text to the tile

    def update(self):
        self.rect.x, self.rect.y = self.x * 128, self.y * 128

    def click(self, mouse_x, mouse_y):          # check if mouse pointer is inside tile
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def hasRight(self):                         #checks if there is a tile in the right
        return self.rect.x + 128 < 128 * 3

    def hasLeft(self):                          #checks if there is a tile in the left
        return self.rect.x - 128 >= 0

    def hasAbove(self):
        return self.rect.y - 128 >= 0

    def hasBelow(self):
        return self.rect.y + 128 < 128 * 3

class Game:
    def __init__(self):
        pygame.init()                                       # initialize pygame
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([1000, 384])   # create screen given the height and weight
        pygame.display.set_caption("8-Puzzle Game")         # set title of screen
        self.fileName = "puzzle.in"

    def loadPuzzleContent(self, filename):
        grid = []

        file = open(filename, "r")                          # read the given file in the args
        lines = file.readlines()

        for x in lines:                                     # for every line, split by the whitespace
            innerGrid = x.split(None)
            intInnerGrid = [eval(i) for i in innerGrid]
            grid.append(intInnerGrid)                         # add the array to the grid making a 2D array
        return grid

    def new(self):
        self.tilesGrid = self.loadPuzzleContent(self.fileName)                    # store grid to tilesGrid

        self.allSprites = pygame.sprite.Group()
        self.drawTiles()

        self.listElements = []
        self.path = []
        self.pathCost = 0
        self.isBFS = False

        self.pathCostElement = Element(450, 50, "", 15) #to be displayed only when done
        self.title = Element(450,100, "8-Puzzle Game", 40)


        def traverse():
            if len(self.path) != 0:
                action = self.path.pop(0)       #save popped out action to action
                self.listElements.pop(0)        #remove action Element when moved to the next in UI

                index = indexLocator(self.tilesGrid, 0)
                row, col = index[0], index[1]
                if action == "U":  # swap zero and the element above it
                    self.tilesGrid[row][col], self.tilesGrid[row - 1][col] = self.tilesGrid[row - 1][col], self.tilesGrid[row][col]
                if action == "R":  # swap zero and the element in its right
                    self.tilesGrid[row][col], self.tilesGrid[row][col + 1] = self.tilesGrid[row][col + 1], self.tilesGrid[row][col]
                if action == "D":  # swap zero and the element below it
                    self.tilesGrid[row][col], self.tilesGrid[row + 1][col] = self.tilesGrid[row + 1][col], self.tilesGrid[row][col]
                if action == "L":  # swap zero and the element in its left
                    self.tilesGrid[row][col], self.tilesGrid[row][col - 1] = self.tilesGrid[row][col - 1], self.tilesGrid[row][col]

                self.drawTiles()

                if len(self.path) == 0:                                                                 #check if after moving to next state, it is already the last one
                    self.pathCostElement = Element(450, 250, "Path Cost: " + str(self.pathCost), 15)    #if yes, display path cost element

                    nextBtn = Button( #overlaps a black button to the next button
                        self.screen, 450, 310, 120, 30,
                        font=pygame.font.SysFont('Consolas', 15),
                        inactiveColour=BG_COLOR, pressedColour=BG_COLOR, hoverColour=BG_COLOR,
                        onClick=traverse,
                        textVAlign='centre')

        def promptFile():
            top = tkinter.Tk()
            top.withdraw()  # hide window
            self.fileName = tkinter.filedialog.askopenfilename(parent=top)

            if self.fileName != "":                                        #conditional in case user choses to exit the file select prompt
                self.tilesGrid = self.loadPuzzleContent(self.fileName)
                self.drawTiles()

        def solutionChoice():
            self.tilesGrid = self.loadPuzzleContent(self.fileName)  # bring back the original state of the puzzle
            self.drawTiles()

            self.initialPuzzle = self.loadPuzzleContent(self.fileName)
            self.initialState = State(self.initialPuzzle, indexLocator(game.initialPuzzle, 0), None, None, 0, 0, 0)

            self.pathCostElement = Element(450, 50, "", 15)  #display in case solution is reselected

            if dropdown.getSelected() == 1 or dropdown.getSelected() == 2 or dropdown.getSelected() == 3:
                if dropdown.getSelected() == 1:
                    print("[BFS] Kindly wait as search is ongoing.")
                    self.path = traceBack(BFSearch(game.initialState), game.initialState)  #do BFS then generate a list of actions
                elif dropdown.getSelected() == 2:
                    print("[DFS] Kindly wait as search is ongoing.")
                    self.path = traceBack(DFSearch(game.initialState), game.initialState)  # do DFS then generate a list of actions
                else:
                    print("[A*] Kindly wait as search is ongoing.")
                    self.path = traceBack(ASearch(game.initialState), game.initialState)

                self.listElements = createList(self.path)                    #generate a list of text element for displaying
                self.pathCost = PathCost(self.path)                          #get path cost for displlay after traversal
                self.isBFS = True                                           #change isBFS to True to signal the display in the draw porition

                #display next button
                nextBtn = Button(
                    self.screen, 450, 310, 120, 30,
                    text='Next',
                    font=pygame.font.SysFont('Consolas', 15),
                    inactiveColour=LINE_COLOR, pressedColour=CLICK_COLOR, hoverColour=HOVER_COLOR,
                    onClick=traverse,
                    textVAlign='centre')
            else:
                print("NONE SELECTED. Select your searching algorithm first.")

        selectFileBtn = Button(
            self.screen, 450, 190, 120, 30,
            text = 'Select File',
            font = pygame.font.SysFont('Consolas', 15),
            inactiveColour = LINE_COLOR, pressedColour = CLICK_COLOR, hoverColour = HOVER_COLOR,
            onClick = promptFile,
            textVAlign='centre'
        )

        dropdown = Dropdown(self.screen, 600, 190, 120, 30,
            name='Search Type',
            font=pygame.font.SysFont('Consolas', 15),
            choices=['BFS','DFS', "A* Search"],
            inactiveColour= LINE_COLOR, pressedColour= CLICK_COLOR, hoverColour = HOVER_COLOR,
            values=[1, 2, 3],
            direction='down',
            textHAlign='centre'
        )

        button = Button(
            self.screen, 750, 190, 120, 30,
            text = 'Solution',
            font = pygame.font.SysFont('Consolas', 15),
            inactiveColour = LINE_COLOR, pressedColour = CLICK_COLOR, hoverColour = HOVER_COLOR,
            onClick = solutionChoice,
            textVAlign='centre'
        )


    def run(self):
        self.playing = True

        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()

            #draw
            self.screen.fill(BG_COLOR)          # fill color to the screen
            self.allSprites.draw(self.screen)   # draws all the sprite in the sprite group
            self.drawGrid()

            self.title.draw(self.screen)        # display element for the title
            self.isSolvable.draw(self.screen)

            if self.isBFS== True:
                for i in self.listElements:
                    i.draw(self.screen)

            self.pathCostElement.draw(self.screen)

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()

            pygame.display.flip()               # updates the contents of the entire display

    def checkIfWin(self):
        matchCount = 0
        for row, x in enumerate(self.tilesGrid):        # row (index) i (element)
            for col, tile in enumerate(x):              # enumerate every element inn self.tilesGrid
                if self.tilesGrid[row][col] == GOAL_STATE[row][col]: #check if elements are matched with the winning array
                    matchCount += 1

        if matchCount == 9:
            self.isSolvable = Element(450, 150, "You won. Congratulations!", 15)
        else:
            if isSolvable(self.tilesGrid):
                self.isSolvable = Element(450, 150, "Solvable. You got this, champ!", 15)
            else:
                self.isSolvable = Element(450, 150, "Non-Solvable. It's impossible, man!", 15)

        pygame.display.flip()

    def update(self):
        self.allSprites.update()
        self.checkIfWin()

    def drawGrid(self):
        for row in range(-1, 3 * 128, 128):
            pygame.draw.line(self.screen, BG_COLOR, (row, 0), (row, 3 * 128))  # draws horizontal line
        for col in range(-1, 3 * 128, 128):
            pygame.draw.line(self.screen, BG_COLOR, (0, col), (3 * 128, col))  # draws vertical line

    def drawTiles(self):
        self.tiles = []

        for row, x in enumerate(self.tilesGrid):    # row (index) i (element)
            self.tiles.append([])
            for col, tile in enumerate(x):             # enumerate every element inn self.tilesGrid
                self.tiles[row].append(Tile(self, col, row, tile))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if self.isBFS != True:                              #declare when BFS/DFS is already selected, user cannot move tiles anymore
                if event.type == pygame.MOUSEBUTTONDOWN:        # when the mouse is clicked
                    mouseX, mouseY = pygame.mouse.get_pos()
                    for row, tiles in enumerate(self.tiles):    # iterate through the 2D array
                        for col, tile in enumerate(tiles):      # iterate through the array
                            if tile.click(mouseX, mouseY):      # checks if mouse pointer is inside tile
                                # checks if the tile in the right,left,below,above is 0. If yes, swap
                                if tile.hasRight() and self.tilesGrid[row][col + 1] == 0:
                                    self.tilesGrid[row][col], self.tilesGrid[row][col + 1] = self.tilesGrid[row][col + 1], self.tilesGrid[row][col]
                                if tile.hasLeft() and self.tilesGrid[row][col - 1] == 0:
                                    self.tilesGrid[row][col], self.tilesGrid[row][col - 1] = self.tilesGrid[row][col - 1], self.tilesGrid[row][col]
                                if tile.hasBelow() and self.tilesGrid[row + 1][col] == 0:
                                    self.tilesGrid[row][col], self.tilesGrid[row + 1][col] = self.tilesGrid[row + 1][col], self.tilesGrid[row][col]
                                if tile.hasAbove() and self.tilesGrid[row - 1][col] == 0:
                                    self.tilesGrid[row][col], self.tilesGrid[row - 1][col] = self.tilesGrid[row - 1][col], self.tilesGrid[row][col]

                                self.drawTiles()

game = Game()                                                                                           #initialize a new Game class
game.initialPuzzle = game.loadPuzzleContent(game.fileName)
game.initialState = State(game.initialPuzzle, indexLocator(game.initialPuzzle, 0), None, None, 0,0,0)

while True:
    game.new()
    game.run()

# References
# PyGame Widgets Dropdown and Button. https://pygamewidgets.readthedocs.io/en/latest/widgets/dropdown/#optional-parameters
# Algorithm to determine if solvable: https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
# https://www.youtube.com/watch?v=qIy4U5EJgNE&list=PLOcNsDskpOqpKhkN6tLId128o0vFWWauV&index=4