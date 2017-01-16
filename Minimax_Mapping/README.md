#Minimax mapping

Here Minimax (or at least my spin on it) is being used in the logger program (minimax_tictactoe_logger.cpp) to log all possible board positions and code them using base 3 into integers for easier parsing and storage. These board positions are saved in text files (nonterminalBoards.txt and terminalBoards.txt) based on whether they are are terminal states,ie wins or draws, or nonterminal states. The nonterminal states are read into the best move evaluation program (minimax_tictactoe_best_move.cpp). The states and the best moves are recorded in a labeled fashion (in bestMoves.txt). 

Next steps (not in any order):
  * To do the same thing for Connect4 (since all of the above stuff was done for tic-tac-toe) and use it with the already existing genetic algorithm and neural network code in the Genetic Model folder of this project
  * Create a tic-tac-toe neural network, train using regression, and use genetic algorithms to improve it further
