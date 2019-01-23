import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth):
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        #legalMoves = game_rules.getLegalMoves(board, self.symbol)
        #if len(legalMoves) > 0: return legalMoves[0]
        #else: return None
        #print("Self.symbol is: {}".format(self.symbol))
        legal_moves = game_rules.getLegalMoves(board, self.symbol)
        #print("legal_moves are: {}".format(legal_moves))
        if len(legal_moves) == 0:
            #print("No possible Moves")
            return None
        else:
            top_move = legal_moves[0]
            new_value = NEG_INF
            for move in legal_moves:
                clone_board = game_rules.makePlayerMove(board, self.symbol, move)
                value = self.minimax_helper(clone_board,self.depth,False,self.symbol)
                if value > new_value:
                    top_move = move
                    new_value = value
            return top_move

    def minimax_helper(self,board,depth,max_player,symbol):
        if symbol == "x":
            symbol="o"
        else:
            symbol = "x"

        if max_player:
            moves = game_rules.getLegalMoves(board,symbol)
            new_value = NEG_INF
            depth = depth - 1
            if len(moves) == 0 or depth == 0:
                return self.h1(board, symbol)

            for move in moves:
                clone_board = game_rules.makePlayerMove(board, symbol, move)
                value = self.minimax_helper(clone_board,depth,False,symbol )
                if value > new_value:
                    new_value = value
            return new_value
        else:
            moves = game_rules.getLegalMoves(board, symbol)
            new_value = POS_INF
            depth = depth - 1
            if len(moves) == 0 or depth == 0:
                return self.h1(board, symbol)

            for move in moves:
                clone_board = game_rules.makePlayerMove(board, symbol, move)
                value = self.minimax_helper(clone_board,depth,True,symbol)
                if value < new_value:
                    new_value = value
            return new_value


# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth):
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        #legalMoves = game_rules.getLegalMoves(board, self.symbol)
        #if len(legalMoves) > 0: return legalMoves[0]
        #else: return None
        legal_moves = game_rules.getLegalMoves(board, self.symbol)
        top_move = legal_moves[0]
        new_value = NEG_INF
        alpha = NEG_INF
        beta = POS_INF
        for move in legal_moves:
            clone_board = game_rules.makePlayerMove(board, self.symbol, move)
            value = self.alphabeta_helper(clone_board,self.depth,False,alpha,beta,self.symbol)
            if value > new_value:
                top_move = move
                new_value = value
            if value > alpha:
                alpha = value
            if alpha>=beta:
                break

        return top_move

    def alphabeta_helper(self,board,depth,max_player,alpha,beta,symbol):
        if symbol == "x":
            symbol="o"
        else:
            symbol = "x"

        if max_player:
            moves = game_rules.getLegalMoves(board, symbol)

            depth = depth - 1
            if len(moves) == 0 or depth == 0:
                return self.h1(board, symbol)

            for move in moves:
                clone_board = game_rules.makePlayerMove(board, symbol, move)
                value = self.alphabeta_helper(clone_board, depth, False, alpha,beta,symbol)
                if value > alpha:
                    alpha = value
                if beta <= alpha:
                    return alpha
            return alpha

        else:
            moves = game_rules.getLegalMoves(board, symbol)

            depth = depth - 1
            if len(moves) == 0 or depth == 0:
                return self.h1(board, symbol)
            for move in moves:
                clone_board = game_rules.makePlayerMove(board, symbol, move)
                value = self.alphabeta_helper(clone_board, depth, True, alpha,beta,symbol)
                if value < beta:
                    beta = value
                if beta <= alpha:
                    return beta
            return beta


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
