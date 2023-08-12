# Input is an abstract class which provides inputs to the game
from abc import ABC, abstractmethod
from Board import Board



class Input(ABC):

    @abstractmethod
    def get_input(self, board: Board) -> Board.Move:
        pass


class TextInput(Input):

    def get_input(self, board: Board) -> Board.Move:
        valid_inputs = {
            'd': Board.Move.RIGHT,
            'a': Board.Move.LEFT,
            'w': Board.Move.UP,
            's': Board.Move.DOWN,
            'exit': -1
        }
        user_input = ''
        while user_input not in valid_inputs:
            user_input = input("--> ")

        if user_input == 'exit':
            exit(valid_inputs['exit'])

        return valid_inputs[user_input]

