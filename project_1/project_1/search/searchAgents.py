# searchAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
This file contains all of the agents that can be selected to
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the
project description.

Please only change the parts of the file you are asked to.
Look for the lines that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.

Good luck and happy searching!
"""
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search


class GoWestAgent(Agent):
    """
    An agent that goes West until it can't.
    """

    def getAction(self, state):
        # The agent receives a GameState (defined in pacman.py).

        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP


#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search algorithm for a
    supplied search problem, then returns actions to follow that path.

    As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game board. Here, we
        choose a path to the goal.  In this phase, the agent should compute the path to the
        goal and store it in a local variable.  All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction is None:
            raise Exception("No search function provided for SearchAgent")

        starttime = time.time()
        problem = self.searchType(state)  # Makes a new search problem
        self.actions = self.searchFunction(problem)  # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in registerInitialState).  Return
        Directions.STOP if there is no further action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self):
            self.actionIndex = 0

        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test,
    successor function and cost function.  This search problem can be
    used to find paths to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start is not None:
            self.startState = start

        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):  # @UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist)  # @UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999
        """
        if actions is None:
            return 999999

        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += self.costFn((x, y))
        return cost


class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """

    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)


class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """

    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)


def manhattanHeuristic(position, problem, info={}):
    """
    The Manhattan distance heuristic for a PositionSearchProblem
    """
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclideanHeuristic(position, problem, info={}):
    """
    The Euclidean distance heuristic for a PositionSearchProblem
    """
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0  # Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"

    def getStartState(self):
        "Returns the start state (in your state space, not the full Pacman state space)"
        "*** YOUR CODE HERE ***"
        return (self.startingPosition, tuple())

    def isGoalState(self, state):
        "Returns whether this search state is a goal state of the problem"
        "*** YOUR CODE HERE ***"

        return len(state[1]) == 4

        

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.EAST, Directions.WEST, Directions.NORTH, Directions.SOUTH]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]

            x,y = state[0]
            cornersHit = state[1]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x+dx), int(y+dy)
            hitsWall = self.walls[nextx][nexty]
            if not hitsWall:
                nextState = nextx,nexty
                cost = 1
                nextTuple = state[1]
                if nextState in self.corners and nextState not in state[1]:
                    cornersVisted = list(state[1])
                    cornersVisted.append(nextState)
                    nextTuple = tuple(cornersVisted)
                successors.append(((nextState,nextTuple),action,cost))
        self._expanded += 1
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions is None:
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
        return len(actions)


def cornersHeuristic(state, problem: CornersProblem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem; i.e.
    it should be admissible (as well as consistent).

    NOTE:
        Do NOT use the mazeDistance function found at the bottom of this file in this heuristic.
        Can you figure out why not?
        Hint: mazeDistance executes a BFS. How inefficient would A-star be if we did this?
        In other words, A-star would be doing a BFS for each state it expanded.

    Submissions with mazeDistance will receive a 0 for this question.
    """
    corners = problem.corners  # These are the corner coordinates
    walls = problem.walls  # These are the walls of the maze, as a Grid (game.py)
    
    "*** YOUR CODE HERE ***"
    unvisted = [x for x in corners if x not in state[1]]
    cumulitiveLength = 0
    fromHere = state[0]
    while len(unvisted) > 0:
        length, index = closestCorner(fromHere, unvisted)
        cumulitiveLength += length
        fromHere =  unvisted.pop(index)
    
    return cumulitiveLength
    

def manhattanDistance(pos, goal):
    return abs(pos[1]-goal[1]) + abs(pos[0]-goal[0])

def closestCorner(state, corners):
    dists = list()
    for corner in corners:
        dists.append(manhattanDistance(state, corner))
    return min(dists), dists.index(min(dists))



        
        
    


class AStarCornersAgent(SearchAgent):
    """
    A SearchAgent for FoodSearchProblem using A* and your foodHeuristic
    """

    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem


class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0
        self.heuristicInfo = {}  # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """
        successors = []
        self._expanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999
        """
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


class AStarFoodSearchAgent(SearchAgent):
    """
    A SearchAgent for FoodSearchProblem using A* and your foodHeuristic
    """

    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem


def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a
    Grid (see game.py) of either True or False. You can call foodGrid.asList()
    to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, problem.walls gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use. For example,
    if you only want to count the walls once and store that value, try:
      problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']

    NOTE:
        Do NOT use the mazeDistance function found at the bottom of this file in this heuristic.
        Can you figure out why not?
        Hint: mazeDistance executes a BFS. How inefficient would A-star be if we did this?
        In other words, A-star would be doing a BFS for each state it expanded.

    Submissions with mazeDistance will receive a 0 for this question.
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    if foodGrid.count() == 0:
        return 0
    
    foodList = foodGrid.asList()

    strategySwitch = 1
    # niave farthest Distance, 3/4 points
    if (strategySwitch == 0):
        maxCords, maxDist = findFarthestFood(position, foodList)    
        return maxDist

    #naive farthest within subset
    if (strategySwitch == 1):
        if len(foodList) == 1:
            return manhattanDistance(position, foodList[0])
        max_key, maxval = naiveFarthestFromSubset(foodList, problem)
        if max_key == -1:
            if not len(foodList) == 0:
                return manhattanDistance(position, foodList[0])
            return 0
        else:
            toClosest = findClosestFood(position, list(max_key))
            retVal = maxval + toClosest[1]
            return maxval + toClosest[1]


def findFarthestFood(cords, foodList):
    """
    naive hurestic that simply the finds the farthest food in the 
    remaining foodlist and uses the manhattan distance as a hureistic
    """
    realDist = lambda xy1, xy2: ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5
    max = -1
    maxCords = 0,0
    for food in foodList:
        tempMax = manhattanDistance(cords, food)
        if tempMax > max or max <= 0:
            max = tempMax
            maxCords = food
    return (maxCords, max)

def naiveFarthestFromSubset(foodlist: list, problem: FoodSearchProblem):
    """
    Dynamic programming approach to finding the farthest pair of remaining food. Every possible 
    length of food to food is calculated once at the beginning of the problem and is continually
    referenced for the remaining iterations. Comments will describe the process in more detail!
    """
    
    #catching edgecase
    if len(foodlist) == 0:
        return -1, 0
    
    listcpy = foodlist.copy() #create copy of foodlist to perserve for later comparison
    if not problem.heuristicInfo: # if problem.huersticInfo is empty
        while len(listcpy):
                food = listcpy.pop(0) # pop first element of list to avoid duplicate reverse order comparisons
                # calculate and add manhattan distance between two points as a key value pair. Key = tuple of compared coodinates.
                # Value = manhattan distance
                for compare in listcpy: 
                    dist = manhattanDistance(food,compare) 
                    problem.heuristicInfo[(food, compare)] = dist
    
    # find key for max value
    max_key = max(problem.heuristicInfo, key = problem.heuristicInfo.get)
    tempDict = dict()
    # test if both keys are in the foodlist. If not, we pop the key value pair and store it in a temporary dictionary to be recombined later. 
    # This way, we can keep popping kv pairs until we find the largest valid pair, or return if there is none left. It is important to 
    # perserve the orginal dictionary becuase if the search traverses to a dead end, it must return to some previous parent, and the food 
    # state will change
    while(max_key[1] not in foodlist or max_key[0]  not in foodlist): 
        poppedValue = problem.heuristicInfo.pop(max_key) # pop!
        tempDict[max_key] = poppedValue # saving for recombination
        if not problem.heuristicInfo: # If there are no valid food pairs left!
            problem.heuristicInfo.update(tempDict)
            return -1,0
        
        max_key = max(problem.heuristicInfo, key = problem.heuristicInfo.get) # find the next largest value
    # recombine 
    problem.heuristicInfo.update(tempDict)
    maxVal = problem.heuristicInfo[max_key]
    return max_key, maxVal


def farthestFromSubset(foodList: list):
    return 0
def grahamScan(foodList:  list):
    """returns a list of points denoting the convex

    Args:
        foodList (list): [description]
    """
    copyList = foodList.copy()
    stack = util.Stack()
    #compute the bottom left coordinate 
    bottomLeft = min(foodList, key = lambda coords: (coords[1], coords[0])) 
    
    #calculate the cross product between two points (used to sort the given list of points)
    crossPoints = lambda p1, p2: p1[0]*p2[1] - p1[1]*p2[0]
    #given three points, with p1 repersenting a starting point, calculate the cross product of the end points of vectors p1p2 and p1p3
    crossProduct = lambda p1, p2, p3: crossPoints((p3[0]-p1[0], p3[1]-p1[1]), (p2[0]-p1[0],p2[1]-p1[0]))
    
    copyList.sort(key = lambda food: crossProduct(bottomLeft, food))
    
    # The way graham scan works is it takes the bottom left corner and compares the cross product of it to the first item in the sorted list (call it p1), and the second point
    # in the sorted list, call it p2. Note that the earlier the point in the list the lower the polar angle. It compares the location of p1 and p2 relative to the bottom left
    # corner. If it has to "turn left" to reach the next point p3, then p3 is on the outside of the shape is pushed onto the stack. If p1
    #
    
    
def findClosestFood(cords, foodList):
    realDist = lambda xy1, xy2: ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5
    min = -1
    minCords = 0,0
    for food in foodList:
        tempMin = realDist(cords, food)
        if tempMin < min or min <= 0:
            min = tempMin
            minCords = food
            
    return (minCords, min)
        


class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches
    """

    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while currentState.getFood().count() > 0:
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    
    
    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)
        "*** YOUR CODE HERE ***"
        foodList = food.asList()
        return self.modbfs(startPosition, foodList, problem)
    
    def modbfs(self, gameState, foodList: list, problem):
        """ 
        This implimentation is a modified version of bfs that returns after it hits ANY food, and returns the path
        """
        visited = set()
        queue =  util.Queue()
        queue.push(((gameState, list()),None,None))
        while (not queue.isEmpty()): 
            
            striple = queue.pop()
            s = striple[0]
            if s[0] in foodList:
                return s[1]
            if s[0] not in visited:
                visited.add(s[0])
                successorList = problem.getSuccessors(s[0])
                
                for triple in successorList:
                    temp = triple[0]
                    newtuple = (temp, s[1] + [triple[1]])
                    newtriple = (newtuple,triple[1],triple[2])
                    queue.push(newtriple)
        print("hit")
        return None
    
    

        
    


class AnyFoodSearchProblem(PositionSearchProblem):
    """
      A search problem for finding a path to any food.

      This search problem is just like the PositionSearchProblem, but
      has a different goal test, which you need to fill in below.  The
      state space and successor function do not need to be changed.

      The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
      inherits the methods of the PositionSearchProblem.

      You can use this search problem to help you fill in
      the findPathToClosestDot method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test
        that will complete the problem definition.
        """
        x, y = state

        "*** YOUR CODE HERE ***"
        goal = min(self.food.asList(), key = lambda food: manhattanDistance(state, food))
        if state == goal:
            return True
        else:
            return False


##################
# Mini-contest 1 #
##################

class ApproximateSearchAgent(Agent):
    """
    Implement your contest entry here.  Change anything but the class name.
    """

    def registerInitialState(self, state):
        """
        This method is called before any moves are made.
        """
        "*** YOUR CODE HERE ***"

    def getAction(self, state):
        """
        From game.py:
        The Agent will receive a GameState and must return an action from
        Directions.{North, South, East, West, Stop}
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built.  The gameState can be any game state -- Pacman's position
    in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + point1
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
