"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def weighted_move(game, pos):
    """
    :param game: Isolation's board
    :param pos: Position on the board
    :return: A score equal to square of the distance from the center of the
    board to the given position
    """
    w, h = game.width / 2., game.height / 2.
    y, x = pos
    return float((h - y)**2 + (w - x)**2)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    nb_own_moves = 0
    nb_opp_moves = 0
    for move in game.get_legal_moves(player):
        nb_own_moves += weighted_move(game, move)
    for move in game.get_legal_moves(game.get_opponent(player)):
        nb_opp_moves += weighted_move(game, move)

    return float(nb_own_moves - 3 * nb_opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # We try to retrain the opponent's moves

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    nb_own_future_moves = 0
    nb_opp_future_moves = 0
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    for move in own_moves:
        next_board = game.forecast_move(move)
        nb_own_future_moves += len(next_board.get_legal_moves(player))

    for move in opp_moves:
        next_board = game.forecast_move(move)
        nb_opp_future_moves += len(next_board.get_legal_moves(game.get_opponent(player)))

    return float(nb_own_future_moves - 3 * nb_opp_future_moves)



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # mix between 1 & 2
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    nb_own_future_moves = 0
    nb_opp_future_moves = 0
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    for move in own_moves:
        next_board = game.forecast_move(move)
        for next_move in next_board.get_legal_moves(player):
            nb_own_future_moves += weighted_move(game, next_move)

    for move in opp_moves:
        next_board = game.forecast_move(move)
        for next_move in next_board.get_legal_moves(game.get_opponent(player)):
            nb_opp_future_moves += weighted_move(game, next_move)

    return float(nb_own_future_moves - 3 * nb_opp_future_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)def play_round(cpu_agent, test_agents, win_counts, num_matches):

        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        def max_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if depth == 0:
                return self.score(game, self)

            score = float("-inf")
            for move in game.get_legal_moves():
                score = max(score, min_value(game.forecast_move(move), depth-1))
            return score

        def min_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if depth == 0:
                return self.score(game, self)

            score = float("inf")
            for move in game.get_legal_moves():
                score = min(score, max_value(game.forecast_move(move), depth-1))
            return score

        best_score = float('-inf')
        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if legal_moves:
            _, best_move = max([(weighted_move(game, m), m) for m in legal_moves])

        for move in game.get_legal_moves():
            score = min_value(game.forecast_move(move), depth-1)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize best_move with the center-most move
        # in case the search timeouts before setting a best_move
        legal_moves = game.get_legal_moves()
        if legal_moves:
            _, best_move = max([(weighted_move(game, m), m) for m in legal_moves])
        else:
            best_move = (-1,-1)

        depth = 1
        try:
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1
        except SearchTimeout:
            return best_move
            pass

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.

        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        def max_value(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            legal_moves = game.get_legal_moves()
            if depth == 0 or len(legal_moves) == 0:
                return self.score(game, self)

            best_score = float('-inf')
            for move in legal_moves:
                game_subbranch = game.forecast_move(move)
                score = min_value(game_subbranch, depth - 1, alpha, beta)
                best_score = max(best_score, score)
                if best_score >= beta:
                    return best_score
                alpha = max(alpha, best_score)

            return best_score

        def min_value(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            legal_moves = game.get_legal_moves()
            if depth == 0 or len(legal_moves) == 0:
                return self.score(game, self)

            best_score = float('inf')
            for move in legal_moves:
                game_subbranch = game.forecast_move(move)
                score = max_value(game_subbranch, depth - 1, alpha, beta)
                best_score = min(best_score, score)
                if best_score <= alpha:
                    return best_score
                beta = min(beta, best_score)

            return best_score

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if legal_moves:
            _, best_move = max([(weighted_move(game, m), m) for m in legal_moves])
        best_score = float('-inf')
        for move in legal_moves:
            game_subbranch = game.forecast_move(move)
            score = min_value(game_subbranch, depth - 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            if best_score >= beta:
                return best_move
            alpha = max(alpha, best_score)

        return best_move
