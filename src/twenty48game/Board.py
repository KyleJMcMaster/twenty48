from __future__ import annotations
import random
from typing import List
from numpy import zeros, ndarray, log2
from enum import Enum



class Board:
    class Move(Enum):
        UP = 2
        DOWN = 3
        RIGHT = 0
        LEFT = 1

    class TextRepresentation:

        def __init__(self, board_string: str, score: int):
            self.board_string = board_string
            self.score = score

        @staticmethod
        def get_text_rep(board: Board) -> Board.TextRepresentation:
            # prints a 32 character string, representing the board
            # each tile has 2 digits to represent the power of 2 at that tile
            # where 0 is represented by 2^0
            text = ""
            for tile in board.get_tiles():
                tile_str = ""
                if tile == 0:
                    tile_str = "00"
                else:
                    tile_str = str(log2(tile).astype(int))

                if len(tile_str) == 1:
                    tile_str = "0" + tile_str
                text += tile_str
            return Board.TextRepresentation(text, board.get_score())

        def get_board_from_text_rep(self) -> Board:
            # TODO: fix bug where score is not assigned
            tiles_temp = list(self.get_tiles())
            tiles = [(2 ** int(tile), 0)[tile == "00"] for tile in tiles_temp]
            b = Board()
            b.set_tile_value([i for i in range(16)], tiles)
            b.__score = self.score      # not working
            return b

        def get_tiles(self):
            for i in range(0, len(self.board_string), 2):
                yield self.board_string[i:i + 2]

        def display(self):
            tiles_temp = list(self.get_tiles())
            tiles = [(2 ** int(tile), 0)[tile == "00"] for tile in tiles_temp]
            print(tiles[0:4])
            print(tiles[4:8])
            print(tiles[8:12])
            print(tiles[12:16])


    def __init__(self):
        self.__tiles: ndarray = zeros(16, dtype=int)
        self.__score: int = 0

        self.build_board()

    def build_board(self) -> Board:
        pos = random.sample(range(0, 15), 2)
        val = random.choices([2, 4], weights=[0.9, 0.1], k=2)
        self.set_tile_value(pos, val)
        return self

    def set_tile_value(self, pos: List[int], val: List[int]) -> Board:
        # length of pos and val should agree
        # sets corresponding positions on board to specified values
        # TODO: restrict values in pos and val
        for i in range(len(pos)):
            p = pos[i]
            self.__tiles[p] = val[i]
        return self

    def check_legal_move(self, move: Move) -> bool:
        # checks if move is legal, returns true if legal
        # 0:r,1:l,2:u,3:d
        if move == Board.Move.RIGHT:
            for i in range(len(self.__tiles)):
                if i % 4 == 3: continue
                if self.__tiles[i] != 0 and (self.__tiles[i + 1] == 0 or self.__tiles[i + 1] == self.__tiles[i]):
                    return True
        if move == Board.Move.LEFT:
            for i in range(len(self.__tiles)):
                if i % 4 == 0: continue
                if self.__tiles[i] != 0 and (self.__tiles[i - 1] == 0 or self.__tiles[i - 1] == self.__tiles[i]):
                    return True
        if move == Board.Move.UP:
            for i in range(len(self.__tiles)):
                if i < 4: continue
                if self.__tiles[i] != 0 and (self.__tiles[i - 4] == 0 or self.__tiles[i - 4] == self.__tiles[i]):
                    return True
        if move == Board.Move.DOWN:
            for i in range(len(self.__tiles)):
                if i > 11: continue
                if self.__tiles[i] != 0 and (self.__tiles[i + 4] == 0 or self.__tiles[i + 4] == self.__tiles[i]):
                    return True
        return False

    def get_empty_squares(self) -> List[int]:
        empty_squares = []
        for i in range(len(self.__tiles)):
            if self.__tiles[i] == 0:
                empty_squares.append(i)
        return empty_squares

    def get_score(self) -> int:
        return self.__score

    def get_tile(self, tile) -> int:
        return self.__tiles[tile]

    def get_tiles(self) -> ndarray:
        return self.__tiles.copy()

    def copy(self) -> Board:
        # returns a board object with the same board configuration
        b = Board()
        b.__tiles = self.__tiles.copy()
        b.__score = self.__score
        return b

    def move(self, move: Move) -> Board:
        # plays move
        # 0:r,1:l,2:u,3:d
        if move == Board.Move.RIGHT:
            for k in range(0, 3):
                for i in range(3 - k, 16 - k, 4):
                    for j in range(1, 4 - k):
                        if self.__tiles[i] == 0 and self.__tiles[i - j] != 0:
                            self.__tiles[i] = self.__tiles[i - j]
                            self.__tiles[i - j] = 0
                        if self.__tiles[i] != 0 and self.__tiles[i - j] == self.__tiles[i]:
                            self.__tiles[i] *= 2
                            self.__tiles[i - j] = 0
                            self.__score += self.__tiles[i]
                            break
                        if self.__tiles[i] != 0 and self.__tiles[i - j] != 0 and self.__tiles[i - j] != self.__tiles[i]:
                            break
        if move == Board.Move.LEFT:
            for k in range(0, 3):
                for i in range(0 + k, 13 + k, 4):
                    for j in range(1, 4 - k):
                        if self.__tiles[i] == 0 and self.__tiles[i + j] != 0:
                            self.__tiles[i] = self.__tiles[i + j]
                            self.__tiles[i + j] = 0
                        if self.__tiles[i] != 0 and self.__tiles[i + j] == self.__tiles[i]:
                            self.__tiles[i] *= 2
                            self.__tiles[i + j] = 0
                            self.__score += self.__tiles[i]
                            break
                        if self.__tiles[i] != 0 and self.__tiles[i + j] != 0 and self.__tiles[i + j] != self.__tiles[i]:
                            break
        if move == Board.Move.UP:
            for k in range(0, 3):
                for i in range(0 + 4 * k, 4 + 4 * k):
                    for j in range(1, 4 - k):
                        if self.__tiles[i] == 0 and self.__tiles[i + j * 4] != 0:
                            self.__tiles[i] = self.__tiles[i + j * 4]
                            self.__tiles[i + j * 4] = 0
                        if self.__tiles[i] != 0 and self.__tiles[i + j * 4] == self.__tiles[i]:
                            self.__tiles[i] *= 2
                            self.__tiles[i + j * 4] = 0
                            self.__score += self.__tiles[i]
                            break
                        if self.__tiles[i] != 0 and self.__tiles[i + j * 4] != 0 and self.__tiles[i + j * 4] != \
                                self.__tiles[i]:
                            break
        if move == Board.Move.DOWN:
            for k in range(0, 3):
                for i in range(12 - 4 * k, 16 - 4 * k):
                    for j in range(1, 4 - k):
                        if self.__tiles[i] == 0 and self.__tiles[i - j * 4] != 0:
                            self.__tiles[i] = self.__tiles[i - j * 4]
                            self.__tiles[i - j * 4] = 0
                        if self.__tiles[i] != 0 and self.__tiles[i - j * 4] == self.__tiles[i]:
                            self.__tiles[i] *= 2
                            self.__tiles[i - j * 4] = 0
                            self.__score += self.__tiles[i]
                            break
                        if self.__tiles[i] != 0 and self.__tiles[i - j * 4] != 0 and self.__tiles[i - j * 4] != \
                                self.__tiles[i]:
                            break
        return self

    def display(self) -> Board:
        print(self.__tiles[0:4])
        print(self.__tiles[4:8])
        print(self.__tiles[8:12])
        print(self.__tiles[12:16])
        return self

    def set_random_square(self) -> Board:
        # add random tile in empty square
        pos = random.sample(self.get_empty_squares(), 1)
        val = random.choices([2, 4], weights=[0.9, 0.1], k=1)
        self.set_tile_value(pos, val)
        return self

    def get_legal_moves(self) -> List[Move]:
        # returns a list of legal moves to play
        legal_moves = []
        for move in Board.Move:
            if self.check_legal_move(move):
                legal_moves.append(move)
        return legal_moves

    def list_possible_states(self, move: Move) -> List[Board]:
        boards = []
        b = self.copy().move(move)
        for pos in b.get_empty_squares():
            for val in [2, 4]:
                boards.append(b.copy().set_tile_value([pos], [val]))
        return boards


