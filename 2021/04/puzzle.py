import fileinput

import numpy as np

x = "\n".join([line.strip() for line in fileinput.input()])
draws, *boards = x.split("\n\n")
draws = [int(num) for num in draws.split(",")]
boards = np.asarray([[int(num) for num in board.split()] for board in boards]).reshape(
    (-1, 5, 5)
)

winning_boards = set()
for draw in draws:
    for i_board, board in enumerate(boards):
        board[board == draw] = -1  # update boards
        wins = any(np.sum(board, axis=-1) == -5) or any(np.sum(board, axis=0) == -5)
        if wins:
            if len(winning_boards) == 0:
                print(f"part 1: {sum(board[board != -1])*draw}")  # first winning board
            winning_boards.add(i_board)

        if len(winning_boards) == len(boards):
            print(f"part 2: {sum(board[board != -1])*draw}")
            raise SystemExit
