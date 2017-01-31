#TicTacToe

Here Minimax (or at least my spin on it) is being used in the logger program (BoardMapping.cpp) to log all possible board positions and code them using base 3 into integers for easier parsing and storage. These board positions are saved in text files (nonterminalBoards.txt and terminalBoards.txt in the OutputFiles folder) based on whether they are are terminal states, i.e. wins or draws, or nonterminal states. The nonterminal states are read into the best move evaluation program (BestMove.cpp). The states and the best moves are recorded in a labeled fashion (in bestMoves.txt in OutputFiles).

In order to play using the SVM compile and run Play.cpp:

g++ Play.cpp -o play
./play

Next steps (not in any order):
  
  * To do the same thing for Connect4 (since all of the above stuff was done for tic-tac-toe) and use it with the already existing genetic algorithm and neural network code in the Connect4 folder of this project
