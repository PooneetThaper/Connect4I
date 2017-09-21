# Connect4I

Current:
Now, it has been clear for a while that the goal of the entire project is to create an agent that performs well on a Markov Decision Process so Reinforcement Learning seems to be the better route to go... Currently exploring Deep Q-Learning and other Deep Reinforcement Learning techniques that I will come back and try on these problems. So far, I have implemented an environment for TicTacToe modeled after OpenAI Gym environments to maintain and update state and provide rewards in response to actions for RL agents.

Post Hackathon Progress 3:
The SVM approach was abandoned in favor of an optimized minimax program that allowed much faster computation on TicTacToe (because the tree is not very deep). This approach is currently working on TicTacToe but not so much on Connect4 (too deep with too high a branching factor for even a single move). Other routes should be explored... (Alpha-beta? RL?)

Post Hackathon Progress 2:
The game tree for TicTacToe was traversed to find all possible game states where each state was labeled as either terminating or non-terminating. Non-terminating states were taken and run through completely using minimax in order to find the best move from that specific state. This data was then fed to SciKitLearn Support Vector Classifier to see if that would provide a less computationally intensive model than just a deep-dive minimax program.

Post Hackathon Progress 1:
This project was started during the HackRPI Fall 2016 Student Hackathon and is being improved upon incrementally. The initial implementation, while functional, failed to (efficiently?) produce a capable agent. The focus instead has shifted to map all possible board states (terminal and non-terminal) of the games and use the minimax algorithm to evaluate the best move at each legal, non-terminal board configuration. This dataset would then be utilized through supervised learning to train a model to recognize the best move to provide reasonably skilled players.

Original HackRPI Idea:
An implemenation of neural networks and genetic algorithms to create skilled Connect4 and TicTacToe players (since they both rely on similar x-in-a-row goals and adversarial tactics but the latter has a smaller game board so it is good for quick testing). The neural networks would be agents playing the game and would be trained using genertic algorithms by passing on the weights of the most successful networks (with cross breeding and mutations) to each successive generation. 
