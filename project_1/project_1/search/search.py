# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

from hashlib import new
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    """Implimentation is backed buy a stack and a set. Set tracks visited nodes, and stack is a first-in-last-out structure.
       Data is stored in the stack as a triple, so that it is immutable. Element 1 is a tuple with the game state and the moves 
       to get to state, respectively. Element 2 is last move. Element 3 is cost (unused in DFS). Further searches are based mostly
       on this implimentation, and store data in the backing data structure in the same way
    """
    visited = set()
    stack =  util.Stack()
    stack.push(((problem.getStartState(), list()),None,None))
    while (not stack.isEmpty()):
        
        striple = stack.pop()
        s = striple[0]
        
        if problem.isGoalState(s[0]):
            return s[1]
        if s[0] not in visited:
            visited.add(s[0])
            successorList = problem.getSuccessors(s[0])
            
            for triple in successorList:
                temp = triple[0]
                newtuple = (temp, s[1] + [triple[1]])
                newtriple = (newtuple,triple[1],triple[2])
                stack.push(newtriple)
    return None


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    """ This implimentation is backed by a set and a queue, a first in first out stucture. There are no differences to how the data is pushed into 
        backing structure. 
    """
    visited = set()
    queue =  util.Queue()
    queue.push(((problem.getStartState(), list()),None,None))
    while (not queue.isEmpty()): 
        
        striple = queue.pop()
        s = striple[0]
        if problem.isGoalState(s[0]):
            return s[1]
        if s[0] not in visited:
            visited.add(s[0])
            successorList = problem.getSuccessors(s[0])
            
            for triple in successorList:
                temp = triple[0]
                newtuple = (temp, s[1] + [triple[1]])
                newtriple = (newtuple,triple[1],triple[2])
                queue.push(newtriple)
    return None


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    """This implimentation is backed buy a set and a Prioirty Queue, and is pushed into the stack with the cumulitive cost. The cost is tracked using the third element
    of the main tuple that is pushed every exploration step. There are no other changes to data i8s pushed into the backing structure. 
    """
    visited = set()
    queue =  util.PriorityQueue()
    queue.push(((problem.getStartState(), list()),None,0),0)
    while (not queue.isEmpty()):
        
        striple = queue.pop()
        s = striple[0]
        
        if problem.isGoalState(s[0]):
            return s[1]
        if s[0] not in visited:
            visited.add(s[0])
            successorList = problem.getSuccessors(s[0])
            
            for triple in successorList:
                temp = triple[0]
                newtuple = (temp, s[1] + [triple[1]])
                newtriple = (newtuple,triple[1],striple[2] + triple[2])
                queue.push(newtriple, newtriple[2])
    return None



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    visited = set()
    queue =  util.PriorityQueue()
    queue.push(((problem.getStartState(), list()),None,0),0)
    while (not queue.isEmpty()):
        
        striple = queue.pop()
        s = striple[0]
        
        if problem.isGoalState(s[0]):
            return s[1]
        if s[0] not in visited:
            visited.add(s[0])
            successorList = problem.getSuccessors(s[0])
            
            for triple in successorList:
                temp = triple[0]
                newtuple = (temp, s[1] + [triple[1]])
                newtriple = (newtuple,triple[1],striple[2] + triple[2] + heuristic(temp, problem))
                queue.push(newtriple, newtriple[2])
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
