# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import GameState
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        moved = not newPos == currentGameState.getPacmanPosition()

        

        #minimize this
        numFoods = len(newFood.asList())
        distsToFoods = [util.manhattanDistance(f , newPos) for f in newFood.asList()]
        
        #maximize
        distToGhosts = [util.manhattanDistance(ghost.getPosition(),newPos) for ghost in newGhostStates]
        
        tooClose = min(distToGhosts) <= 1


        return 100000/(numFoods+1) + 10000/(sum(distsToFoods)+1) + sum(distToGhosts)+moved*10000 + tooClose *(-10000000)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        moves = gameState.getLegalActions()
        num = gameState.getNumAgents()
        #print "YO", self.depth
        return self.getAction2(gameState,0, depth = 0)[1]

    
    def getAction2(self, gameState, agentIndex, depth):

      #print depth, self.depth

      # print gameState

      if gameState.isWin():
        return (self.evaluationFunction(gameState),)
      elif gameState.isLose():
        return (self.evaluationFunction(gameState),)
      elif depth == self.depth:
        return (self.evaluationFunction(gameState),)



      #print agentIndex, gameState.getNumAgents()

      

      if agentIndex == 0:
        bs = -1000000
        bm = None
        for move in gameState.getLegalActions(agentIndex):
          suc = gameState.generateSuccessor(agentIndex, move)
          #print "Agent ", agentIndex, 1, gameState.getNumAgents()
          score = self.getAction2(suc, 1 , depth)[0]
          if score > bs:
            bs = score
            bm = move
        return (bs, bm)
      elif agentIndex < gameState.getNumAgents()-1:
        bm = None
        bs = 10000000
        for move in gameState.getLegalActions(agentIndex):
          suc = gameState.generateSuccessor(agentIndex, move )
          #print "Agent ", agentIndex, agentIndex+1 ,gameState.getNumAgents()
          score = self.getAction2(suc, agentIndex+1 , depth)[0]
          if score < bs:
            bs = score
            bm = move
        return (bs, bm)
      elif agentIndex == gameState.getNumAgents() -1:
        bs = 1000000
        bm = None
        for move in gameState.getLegalActions(agentIndex):
          suc = gameState.generateSuccessor(agentIndex, move)
          #print "Agent ", agentIndex, 0,gameState.getNumAgents()
          score = self.getAction2(suc, 0 , depth +1)[0]
          if score < bs:
            bs = score
            bm = move
        return (bs, bm)



        
        #isWin()
        #isLose()
        
    
# def terminalTest(gameState):
#   return False

# def miniMax(gameState, agentIndex):
#   numAgents = gameState.getNumAgents()
#   if gameState.isWin():
#     return 1000
#   elif gameState.isLose():
#     return -1000
#   elif
#   if agentIndex == 0:
#     #do packman shit and call on next agent
#     bestMove = None
#     bestScore = -999999

#     for action in gameState.getLegalActions(agentIndex):
#       newState = gameState.generateSuccessor(agentIndex, action)
#       if scoreEvaluationFunction(newState) > bestMove:
#         bestMove = action
#         bestScore = scoreEvaluationFunction(action)
    
#     return miniMax()

#   elif agentIndex < numAgents -1:
#     #do agent shit and call again on index + 1
#     pass
#   else:
#     #last agent
#     #do agent shit and call on apcman
#     pass



        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        toRet = self.alphaBeta(gameState,0, depth = 0, alpha = -100000, beta = 100000)
        #print toRet
        return toRet


    def alphaBeta (self, gameState, agentIndex = 0, depth = 0, alpha = -100000, beta = 100000):
      return self.maxValue(gameState, agentIndex, depth, alpha, beta)[1]

    def maxValue(self, gameState, agentIndex, depth, alpha, beta):
      if self.terminal(gameState, depth):
        return (self.evaluationFunction(gameState),)

      bm = None
      v = -10000000
      for move in gameState.getLegalActions(agentIndex):
          suc = gameState.generateSuccessor(agentIndex, move)

          #ghost one always goes after pacman, so we hardcode one here
          score = self.minValue(suc, 1 , depth, alpha, beta)[0]

          v = max(v, score)
          if v > beta:
            return (v, move)
          if (v > alpha):
            alpha = v
            bm = move


      
      return (v, bm)


    def minValue(self, gameState, agentIndex, depth, alpha, beta):
      if self.terminal(gameState, depth):
        return (self.evaluationFunction(gameState),)

      bm = None
      v = 10000000
      for move in gameState.getLegalActions(agentIndex):
          suc = gameState.generateSuccessor(agentIndex, move)

          #ghost one always goes after pacman, so we hardcode one here
          if (agentIndex == gameState.getNumAgents()-1 ):
            #back to pack man
            score = self.maxValue(suc, 0 , depth+1, alpha, beta)[0]
          elif (agentIndex < gameState.getNumAgents()-1 ):
            score = self.minValue(suc, agentIndex + 1 ,depth, alpha, beta)[0]

          v = min(v, score)
          if v < alpha:
            return (v, move)
          if (v < beta):
            beta = v
            bm = move

      return (v, bm)

    def terminal(self, gameState, depth):
      #print depth
      return gameState.isWin() or gameState.isLose() or depth == self.depth


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.getAction2(gameState,0, depth = 0)[1]

    
    def getAction2(self, gameState, agentIndex, depth):

      #print depth, self.depth

      # print gameState

      if gameState.isWin():
        return (self.evaluationFunction(gameState),)
      elif gameState.isLose():
        return (self.evaluationFunction(gameState),)
      elif depth == self.depth:
        return (self.evaluationFunction(gameState),)



      #print agentIndex, gameState.getNumAgents()

      

      #FUTURE: just get all of the scores in the loops below and average them.
      #pass a NOne for move if random


      if agentIndex == 0:
        bs = -1000000
        bm = None
        for move in gameState.getLegalActions(agentIndex):
          suc = gameState.generateSuccessor(agentIndex, move)
          #print "Agent ", agentIndex, 1, gameState.getNumAgents()
          score = self.getAction2(suc, 1 , depth)[0]
          if score > bs:
            bs = score
            bm = move
        return (bs, bm)
      elif agentIndex < gameState.getNumAgents()-1:
        bm = None
        bs = 10000000


        avg = sum([self.getAction2(gameState.generateSuccessor(agentIndex, move ), agentIndex+1 , depth)[0] for move in gameState.getLegalActions(agentIndex)])/len(gameState.getLegalActions(agentIndex))
        return (avg, None)
      elif agentIndex == gameState.getNumAgents() -1:
        bs = 1000000
        bm = None
        avg = sum([self.getAction2(gameState.generateSuccessor(agentIndex, move ), 0 , depth+1)[0] for move in gameState.getLegalActions(agentIndex)])/len(gameState.getLegalActions(agentIndex))
        return (avg, None)


    

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    

    

    #minimize this
    numFoods = len(newFood.asList())
    distsToFoods = [util.manhattanDistance(f , newPos) for f in newFood.asList()]
    
    #maximize
    distToGhosts = [util.manhattanDistance(ghost.getPosition(),newPos) for ghost in newGhostStates]
    
    tooClose = min(distToGhosts) <= 2

    if numFoods == 0:
      toRet = 100000000000
    else:
      #toRet = 1.0/(10000*min(distsToFoods))+ 100.0/(numFoods*100+1) + 10.0/(sum(distsToFoods)*10000+1) + tooClose *(-1000000000)#+ .00000001*sum(distToGhosts) 
      toRet = 100000000.0/(numFoods+1) + 100000000.0/(sum(distsToFoods)+1) + sum(distToGhosts)+ tooClose *(-10000000)
    #print toRet
    #print toRet
    #100000/(numFoods+1) + 10000/(sum(distsToFoods)+1) + sum(distToGhosts)+moved*10000 + tooClose *(-10000000)
    return toRet

# Abbreviation
better = betterEvaluationFunction

