import numpy as np

class TicTacToe:
    # board: numpy array of 9 values of board
    #               0   1   2
    #               3   4   5
    #               6   7   8
    # history: list of tuples of (board, current_player, action, done, winner)

    def __init__(self):
        self.board = np.zeros(9)
        self.current_player = 1
        self.over = False
        self.winner = 0
        self.history = []

    def is_over(self, last_move):
        win = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for w in win:
            if last_move in w:
                if np.abs(self.board[w[0]] + self.board[w[1]] +self.board[w[2]]) == 3:
                    self.over = True
                    self.winner = self.board[w[0]]
                    return True
        return not 0 in self.board

    # Show state functions
    def print_board(self):
        print(self.board)

    def print_history(self):
        for entry in self.history:
            print(entry)

    def print_current_player(self):
        print(self.current_player)

    # Get functions
    def get_over(self):
        return self.over

    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player

    def get_current_view(self):
        # Returns the board from the view of the current playerNum
        # where current players marks are 1 and opposing players marks are -1
        return self.board*self.current_player

    # Modifier functions
    def make_move(self, position):
        if (self.over) or self.board[position] != 0:
            return -1
        # Creating record of state and action taken
        record = (np.copy(self.board), self.current_player, position)
        # Executing action to get resulting state
        self.board[position] = self.current_player
        self.current_player *= -1
        record += (self.is_over(position),int(self.winner),)
        # Appending record to history
        self.history.append(record)

        return int(self.over)

    def update(self, position):
        reward = self.make_move(position)
        # Return in OpenAI Gym Style
        # (state, reward, done, info)
        return (self.board, reward, self.over, self.history)

    # Reset functions
    def reset_game(self):
        self.board = np.zeros(9)
        self.current_player = 1
        self.over = False
        self.history = []



if __name__ == "__main__":
    game = TicTacToe()
    while not game.get_over():
        print(game.update(np.random.randint(9))[0:3])
    game.print_history()
