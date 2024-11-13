from enum import Enum

class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    DIAGONAL_DOWN_RIGHT = (1, 1)
    DIAGONAL_DOWN_LEFT = (1, -1) 

    def __init__(self, row_step, col_step):
        self.row_step = row_step
        self.col_step = col_step