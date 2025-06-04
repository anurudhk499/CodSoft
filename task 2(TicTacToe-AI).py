import math
import random
import os
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.YELLOW + """
  _______ _        _______           _______         
 |__   __(_)      |__   __|         |__   __|        
    | |   _  ___     | | __ _  ___     | | ___   ___ 
    | |  | |/ __|    | |/ _` |/ __|    | |/ _ \ / _ \\
    | |  | | (__     | | (_| | (__     | | (_) |  __/
    |_|  |_|\___|    |_|\__,_|\___|    |_|\___/ \___|
        """ + Style.RESET_ALL)
        
        print(Fore.CYAN + "\n     Current Board:" + Style.RESET_ALL)
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            colored_row = []
            for item in row:
                if item == 'X':
                    colored_row.append(Fore.RED + item + Style.RESET_ALL)
                elif item == 'O':
                    colored_row.append(Fore.BLUE + item + Style.RESET_ALL)
                else:
                    colored_row.append(' ')
            print(Fore.WHITE + "     -------------" + Style.RESET_ALL)
            print("     | " + " | ".join(colored_row) + " |")
        print(Fore.WHITE + "     -------------" + Style.RESET_ALL)

    @staticmethod
    def print_board_nums():
        print(Fore.GREEN + "\nNumber Positions:" + Style.RESET_ALL)
        for row in [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]:
            print(Fore.WHITE + "     -------------" + Style.RESET_ALL)
            print("     | " + " | ".join(row) + " |")
        print(Fore.WHITE + "     -------------" + Style.RESET_ALL)

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind + 1)*3]
        if all([s == letter for s in row]):
            return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in column]):
            return True
        
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(Fore.MAGENTA + f"\nPlayer {self.letter}'s turn (0-8): " + Style.RESET_ALL)
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print(Fore.RED + "Invalid move. Try again." + Style.RESET_ALL)
        return val

class AIPlayer(Player):
    def get_move(self, game):
        print(Fore.BLUE + f"\n🤖 AI ({self.letter}) is thinking..." + Style.RESET_ALL)
        time.sleep(0.8)
        
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())
        return self.minimax(game, self.letter)['position']

    def minimax(self, state, player, alpha=-math.inf, beta=math.inf):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (len(state.available_moves()) + 1) if other_player == max_player else -1 * (len(state.available_moves()) + 1)}
        elif not state.available_moves():
            return {'position': None, 'score': 0}

        best = {'position': None, 'score': -math.inf if player == max_player else math.inf}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player, alpha, beta)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, best['score'])
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, best['score'])
            
            if alpha >= beta:
                break

        return best

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + """
  _______ _        _______           _______         
 |__   __(_)      |__   __|         |__   __|        
    | |   _  ___     | | __ _  ___     | | ___   ___ 
    | |  | |/ __|    | |/ _` |/ __|    | |/ _ \ / _ \\
    | |  | | (__     | | (_| | (__     | | (_) |  __/
    |_|  |_|\___|    |_|\__,_|\___|    |_|\___/ \___|
        """ + Style.RESET_ALL)
        
        print(Fore.YELLOW + "\n1. Play against AI")
        print("2. Quit")
        choice = input(Fore.MAGENTA + "\nSelect option (1-2): " + Style.RESET_ALL)
        
        if choice == '1':
            game = TicTacToe()
            play(game, HumanPlayer('X'), AIPlayer('O'))
            input(Fore.GREEN + "\nPress Enter to continue..." + Style.RESET_ALL)
        elif choice == '2':
            print(Fore.YELLOW + "\nThanks for playing! 👋" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "\nInvalid choice!" + Style.RESET_ALL)
            time.sleep(1)

def play(game, x_player, o_player):
    game.print_board_nums()
    letter = 'X'
    
    while game.available_moves():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            game.print_board()
            
            if game.current_winner:
                print(Fore.GREEN + """
                """ + Style.RESET_ALL)
                print(Fore.CYAN + f"\n{'🎉 Player' if letter == 'X' else '🤖 AI'} ({letter}) wins! 🎉" + Style.RESET_ALL)
                return

            letter = 'O' if letter == 'X' else 'X'
    
    print(Fore.YELLOW + """
1
        """ + Style.RESET_ALL)
    print(Fore.CYAN + "\nIt's a tie! No winner." + Style.RESET_ALL)

if __name__ == '__main__':
    main()
