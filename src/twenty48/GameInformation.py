from Board import Board
from typing import List


class GameInformation:
    class Turn:
        def __init__(self, move: Board.Move, time: float, board: Board.TextRepresentation):
            self.move = move
            self.time = time
            self.board = board
            self.max_tile = 2 ** int(max(board.get_tiles()))

        '''def get_JSON(self):
            values = {
                'move': self.move,
                'time': self.time,
                'max tile':self.max_tile,
                'board': self.board
            }
            return values'''

    def __init__(self, num_turns: int, turns: List[Turn], time: float, score: int):
        self.num_turns = num_turns
        self.time = time
        self.score = score
        self.turns = turns

