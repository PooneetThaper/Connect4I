# Connect4I

Current:
Now, it is clear that the goal of the entire project was to try to do Reinforcement Learning so that seems to be the better route to go... Currently exploring Deep Q-Learning and other Deep Reinforcement Learning techniques that I will come back and try on these problems. Until then...

Post Hackathon Progress 3:
The SVM approach was abandoned in favor of an optimized minimax program that allowed much faster computation on TicTacToe (because the tree is not very deep). This approach is currently working on TicTacToe but not so much on Connect4 (too deep with too much branching). Other routes should be explored...

Post Hackathon Progress 2:
The game tree for TicTacToe was traversed to find all possible game states where each state was labeled as either terminating or non-terminating. Non-terminating states were taken and run through completely through using minimax in order to find the best move from that specific state. This data was then fed to SciKitLearn Support Vector Classifier to see if that would provide a less computationally intensive model than just a deep-dive minimax.

Post Hackathon Progress 1:
This project was started during the HackRPI Fall 2016 Student Hackathon and is being improved upon incrementally. Currently, I am trying to apply the minimax algorithm to map all possible board states of the games and evaluating the best move at each legal board configuration. Then, I hope to use supervised learning to train a model to recognize the best move to provide reasonably skilled players. A genetic algorithm will then be used to evolve the players.

Original HackRPI Idea:
An implemenation of the minimax algorithm, neural networks, and genetic algorithms to create skilled Connect4 and TicTacToe players (since they both rely on similar x-in-a-row goals and adversarial but the latter has a smaller game board). 
