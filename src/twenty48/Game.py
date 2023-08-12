# Game controls elements like displaying the board and when game ends
# there should only be one game object made at a time, and AIs can test by duplicating
# boards
# AIs can only interface with up,down,left,right movements, this will prevent possible
# cheating

from twenty48.Board import Board
from twenty48.Display import Display, TextDisplay
from twenty48.Input import Input, TextInput
import time
from twenty48.GameInformation import GameInformation

class Game:

    def __init__(self, display: Display = None, input: Input = None):
        if display is None:
            self.display = TextDisplay()
        else:
            self.display = display

        if input is None:
            self.input = TextInput()
        else:
            self.input = input
        self.__board = Board()


    def get_board(self) -> Board:
        return self.__board.copy()

    def play_game(self) -> GameInformation:

        self.display.display_board(self.__board)
        turns = []
        turn_num = 0
        gameover = False
        game_time = time.perf_counter()

        while not gameover:
            turn_num += 1
            turn_time = time.perf_counter()
            user_input = self.input.get_input(self.__board.copy())
            turn_time = time.perf_counter() - turn_time

            # print(t)
            if self.__board.check_legal_move(user_input):
                self.__board.move(user_input).set_random_square()
                turn = GameInformation.Turn(time=turn_time, move=user_input, board=Board.TextRepresentation.get_text_rep(self.__board))
                turns.append(turn)
                self.display.display_board(self.__board)
            if not self.__board.get_legal_moves():
                gameover = True
        game_time = time.perf_counter()-game_time
        self.display.display_board(self.__board)
        info = GameInformation(num_turns=turn_num, turns=turns, time=game_time, score=self.__board.get_score())
        return info





