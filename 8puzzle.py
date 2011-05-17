#!/usr/bin/python

# Christine Cheung
# CS170 Project 1 (8-Puzzle)

import sys, copy

goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']]

def main():
    input = puzzleInput() # puzzle input
    algoChoice = algorithm() # algorithm input
    puzzleSearch(input, algoChoice) # and searching for puzzle solution

def puzzleInput():

    # the default puzzle to use
    default = [['1', '2', '3'], ['4', ' ', '6'], ['7', '5', '8']]
    # set our main puzzle
    puzzle = []

    print "Greetings, this is Christine's 8-puzzle solver."

    # loop until we get correct input
    while 1:
        
        startinput = raw_input("Type 1 to use the default puzzle, 2 to enter your own, or 3 to quit.\n")

        # 1: default puzzle
        if (startinput == "1"):
            print "Using default puzzle...\n"
            puzzle = default
            return puzzle

        # 2: user defined puzzle
        elif (startinput == "2"):
            print "Enter your puzzle, use a zero to represent the blank:\n"
            firstrow = raw_input("Enter the first row, use a space between numbers ")
        
            # FIRST row
            firstrow = firstrow.split(' ')
            # change 0 to space
            if (firstrow.count('0') == 1):
                firstrow[firstrow.index('0')] = ' '
            
            # SECOND row
            secondrow = raw_input("Enter the second row, use a space between numbers ")
            secondrow = secondrow.split(' ')
            # change 0 to space
            if (secondrow.count('0') == 1):
                secondrow[secondrow.index('0')] = ' '

            # THIRD row
            thirdrow = raw_input("Enter the third row, use a space between numbers ")
            thirdrow = thirdrow.split(' ')
            # change 0 to space
            if (thirdrow.count('0') == 1):
                thirdrow[thirdrow.index('0')] = ' '

            # add the input to the puzzle
            puzzle.append(firstrow)
            puzzle.append(secondrow)
            puzzle.append(thirdrow)
            print "\n"

            return puzzle
            
        # 3: quit puzzle
        elif (startinput == "3"):
            sys.exit(0)


def algorithm():
    
    print "Choice of algorithms to use:"
    print "1. Uniform Cost Search"
    print "2. A* with misplaced tile heuristic"
    print "3: A* with Manhattan distance heuristic\n"
    # infinite loop until correct input of algorithm choice
    while 1:
        pickAlgo = raw_input("Enter: ")
        if(pickAlgo == '1'):
            return "costSearch"
        elif(pickAlgo == '2'):
            return "misplacedTile"
        elif(pickAlgo == '3'):
            return "manhattan"

    return pickAlgo


def expand(puzzle):

    expandList = []

    puzzleLeft = copy.deepcopy(puzzle)
    # move the tile left
    # search through the puzzle
    for x in puzzleLeft:
        # check where the blank tile is
        if (x.count(' ') == 1):
            # make sure it's not on the left side
            # so we can actually move it legally
            if (x.index(' ') != 0):
                spaceindex = x.index(' ')
                # set space to equal left tile
                x[spaceindex] = x[spaceindex - 1]
                x[spaceindex - 1] = ' '

                expandList.append(puzzleLeft)

    puzzleRight = copy.deepcopy(puzzle)
    # move the tile right
    for x in puzzleRight:
        # check where the blank tile is    print puzzle

        if (x.count(' ') == 1):
            # make sure it's not on the right side
            # so we can actually move it legally
            if (x.index(' ') != 2):
                spaceindex = x.index(' ')
                # set space to equal right tile
                x[spaceindex] = x[spaceindex + 1]
                x[spaceindex + 1] = ' '

                expandList.append(puzzleRight)

    puzzleUp = copy.deepcopy(puzzle)
    # move the tile up
    for x in puzzle:
        # check where the blank tile is
        if (x.count(' ') == 1):
            # make sure it's not on the top (first row)
            # so we can actually move it legally
            if (x != puzzleUp[0]):
                spaceindex = x.index(' ')
                # on second row?
                if(x == puzzle[1]):
                    puzzleUp[1][spaceindex] = puzzleUp[0][spaceindex]
                    puzzleUp[0][spaceindex] = ' '
                    expandList.append(puzzleUp)
                # or third
                else:
                    puzzleUp[2][spaceindex] = puzzleUp[1][spaceindex]
                    puzzleUp[1][spaceindex] = ' '
                    expandList.append(puzzleUp)


    puzzleDown = copy.deepcopy(puzzle)
    # move the tile down
    for x in puzzle:
        # check where the blank tile is
        if (x.count(' ') == 1):
            # make sure it's not on the bottom (third row)
            # so we can actually move it legally
            if (x != puzzle[2]):
                spaceindex = x.index(' ')
                # on first row?
                if(x == puzzle[0]):
                    puzzleDown[0][spaceindex] = puzzleDown[1][spaceindex]
                    puzzleDown[1][spaceindex] = ' '
                    expandList.append(puzzleDown)
                # or second
                else:
                    puzzleDown[1][spaceindex] = puzzleDown[2][spaceindex]
                    puzzleDown[2][spaceindex] = ' '
                    expandList.append(puzzleDown)

    return expandList


# create our node class for enqueuing puzzle states
class node:

    def __init__(self):
        self.heuristic = 0
        self.depth = 0
        
    def printPuzzle(self):
        print ''
        print self.puzzleState[0][0], self.puzzleState[0][1], self.puzzleState[0][2]
        print self.puzzleState[1][0], self.puzzleState[1][1], self.puzzleState[1][2]
        print self.puzzleState[2][0], self.puzzleState[2][1], self.puzzleState[2][2]

    def setPuzzle(self, puzzle):
        self.puzzleState = puzzle


def checkGoal(puzzle):
    # check if puzzle has been solved (equals goal state)
    return goal == puzzle


def misplacedTiles(puzzle):
    
    misplace = 0
    for x in range(3):
        for y in range(3):
            # make sure we don't check blank
            if (puzzle[x][y] != ' '):
                # if it's not at it's proper place, it's misplaced
                if (puzzle[x][y] != goal[x][y]):
                    misplace += 1

    return misplace


def manhattan(puzzle):

    mDistance = 0
    puzzleContents = ['1', '2', '3', '4', '5', '6', '7', '8']
    # search through the numbers in the puzzle
    for x in puzzleContents:
        for i in range(3):
            for j in range(3):
                # get where the number should be
                if (x == goal[i][j]):
                    goalRow = i
                    goalCol = j
                # get where the number is now
                if (x == puzzle[i][j]):
                    puzzleRow = i
                    puzzleCol = j
        # calculate the Manhattan Distance based on the points (row/col)
        mDistance += ( abs(goalRow - puzzleRow) + abs(goalCol - puzzleCol) )

    return mDistance


# from http://en.wikipedia.org/wiki/Bubble_sort
def bubblesort(queue):

    for passesLeft in xrange(len(queue)-1, 0, -1):
        for index in xrange(passesLeft):
            if (queue[index].heuristic + queue[index].depth) > \
                   (queue[index + 1].heuristic + queue[index + 1].depth):
                queue[index], queue[index + 1] = queue[index + 1], queue[index]

    return queue


def puzzleSearch(puzzle, algorithm):

    nodesExpanded = 0
    maxQueueSize = 0
    queue = []

    # make the new node (set to intial puzzle)
    puzzleNode = node()
    puzzleNode.setPuzzle(puzzle)
    # the initial depth
    puzzleNode.depth = 0
    # pick our heuristics
    if (algorithm == "costSearch"):
        puzzleNode.heuristic = 1
    if (algorithm == "misplacedTile"):
        puzzleNode.heuristic = misplacedTiles(puzzleNode.puzzleState)
    if (algorithm == "manhattan"):
        puzzleNode.heuristic = manhattan(puzzleNode.puzzleState)

    # append first node (initial state) to the queue
    queue.append(puzzleNode)

    # infinite loop until we find our solution
    while 1:

        if (len(queue) == 0):
            print "Puzzle search exhausted"
            sys.exit(0)

        # make the puzzleNode equal to the front of queue
        checkNode = node()
        checkNode.puzzleState = queue[0].puzzleState
        checkNode.heuristic = queue[0].heuristic
        checkNode.depth = queue[0].depth

        # print depth and heuristics stats
        print ''
        print "The best node to expand with g(n) =", checkNode.depth, \
              "and h(n) =", checkNode.heuristic, "is..."
        checkNode.printPuzzle()
        print "Expanding this node..."
        
        # then remove the front of queue
        queue.pop(0)

        # check if it is the solution
        if (checkGoal(checkNode.puzzleState)):
            # then print solution and return
            print ''
            print "Solution found!!"
            checkNode.printPuzzle()
            print ''
            print "Expanded a total of", nodesExpanded, "nodes"
            print "Maximum number of nodes in the queue was", maxQueueSize
            print "The depth of the goal node was", checkNode.depth
            return

        # expand the node
        expandedPuzzle = expand(checkNode.puzzleState)

        for x in expandedPuzzle:
            # make each expansion a node...
            # and then add them to the queue
            tempNode = node()
            tempNode.setPuzzle(x)
            # determine the heuristic to use
            if (algorithm == "costSearch"):
                tempNode.heuristic = 1
            if (algorithm == "misplacedTile"):
                tempNode.heuristic = misplacedTiles(tempNode.puzzleState)
            if (algorithm == "manhattan"):
                tempNode.heuristic = manhattan(tempNode.puzzleState)
            # every time you expand, you add a depth
            tempNode.depth = checkNode.depth + 1
            # and then add it to the queue, of course
            queue.append(tempNode)
            nodesExpanded += 1

            if(len(queue) > maxQueueSize):
                maxQueueSize = len(queue)

        queue = bubblesort(queue)

    
if __name__ == "__main__":
    main()

