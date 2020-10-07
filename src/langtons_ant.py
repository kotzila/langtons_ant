import os
import time
import argparse
from enum import Enum
from collections import namedtuple
from typing import Sequence

Direction = Enum('Direction', 'up right down left')

Position = namedtuple("Position", "x y direction")


class Color(Enum):
    black = True
    white = False

    def __str__(self):
        return "#" if self.value else '-'


DEFAULT_COLOUR = Color.white

Board = Sequence[Sequence[Color]]


class Ant:
    def __init__(self, x: int, y: int, color: Color, direction: Direction):
        self.x, self.y = x, y
        self.color = color
        self.direction = direction

    def move(self, board: Board) -> Board:
        if self.color == Color.black:
            self.turn_left()
        else:
            # color white
            self.turn_right()
        self.change_color(board)
        board = self.move_forvard(board)
        return board

    def turn_right(self):
        if self.direction == Direction.up:
            self.direction = Direction.right
        elif self.direction == Direction.right:
            self.direction = Direction.down
        elif self.direction == Direction.down:
            self.direction = Direction.left
        elif self.direction == Direction.left:
            self.direction = Direction.up

    def turn_left(self):
        if self.direction == Direction.up:
            self.direction = Direction.left
        elif self.direction == Direction.left:
            self.direction = Direction.down
        elif self.direction == Direction.down:
            self.direction = Direction.right
        elif self.direction == Direction.right:
            self.direction = Direction.up

    def change_color(self, board: Board) -> Board:
        new_color = Color(not self.color.value)
        self.color = new_color
        board[self.x][self.y] = new_color
        return board

    def regenerate_board(self, board: Board) -> Board:
        if self.direction == Direction.down:
            board.append([DEFAULT_COLOUR for x in range(len(board[0]))])
        elif self.direction == Direction.right:
            board = [item + [DEFAULT_COLOUR] for item in board]
        elif self.direction == Direction.up:
            board.insert(0, [DEFAULT_COLOUR for x in range(len(board[0]))])
            self.x += 1
        elif self.direction == Direction.left:
            board = [[DEFAULT_COLOUR] + item for item in board]
            self.y += 1

        self.color = board[self.x][self.y]
        return board

    def move_forvard(self, board: Board) -> Board:
        if self.direction == Direction.up:
            if self.x != 0:
                self.x -= 1
            else:
                return self.regenerate_board(board)

        elif self.direction == Direction.right:
            self.y += 1
        elif self.direction == Direction.down:
            self.x += 1
        elif self.direction == Direction.left:
            if self.y != 0:
                self.y -= 1
            else:
                return self.regenerate_board(board)
        try:
            self.color = board[self.x][self.y]
        except IndexError:
            board = self.regenerate_board(board)
        return board


class LangtonsAnt:
    def __init__(self, state: Board, position: Position):
        self._state, self.position = state, (position.x, position.y)
        ant_start_state = state[position.x][position.y]
        self.ant = Ant(*self.position, color=ant_start_state, direction=position.direction)

    def next(self):
        board = self.ant.move(self._state)
        self._state = board

    @property
    def state(self):
        return '\n'.join([''.join(['{} '.format(item) for item in row])
                          for row in self._state])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Langtons Ant')
    parser.add_argument('-x', action="store", type=int, default=0)
    parser.add_argument('-y', action="store", type=int, default=0)
    parser.add_argument('-direction', action="store", default="right")
    parser.add_argument('-iterations', action="store", type=int, default=1000)

    params = parser.parse_args()
    start_position = Position(params.x, params.y, getattr(Direction, params.direction))
    iterarions = params.iterations
    # initialize 2x2 matrix with filled default color values
    # [[<Color.white: False>, <Color.white: False>], [<Color.white: False>, <Color.white: False>]]
    initial_state = [[DEFAULT_COLOUR for item in range(2)] for item in range(2)]

    game = LangtonsAnt(initial_state, start_position)
    print(game.state)

    for i in range(iterarions):
        os.system('clear')
        game.next()
        print(game.state)
        time.sleep(0.1)
