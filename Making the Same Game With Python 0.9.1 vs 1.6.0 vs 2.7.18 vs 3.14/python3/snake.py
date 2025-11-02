"""Snake for Python3."""

import curses
from enum import Enum
from random import choice, randint
from sys import version
from time import sleep

BOARD_ROWS = 20
BOARD_COLS = 20
ALL_POINTS = {(row, col) for row in range(20) for col in range(20)}
PYTHON_VERSION = version.replace("\n", " ")

Point = tuple[int, int]
Snake = list[Point]
Board = list[list[str]]


class Direction(Enum):
    """Directions for keyboard arrow keys."""

    up = 259
    down = 258
    left = 260
    right = 261


def format_board_string(
    board: Board, score: int, debug: dict | None = None, show_debug: bool = False
) -> str:
    """Format the board string for printing.

    :param board: The board to print.
    :param score: The score to print.
    :param debug: Debug information to print at the bottom of the board.
    :param show_debug: If the debug information should be shown.
    :return: The board string.
    """
    output_string = f"{PYTHON_VERSION}\n"
    output_string += f"score: {score}\n"

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            output_string += f"{board[row][col]} "
        output_string += "\n"

    output_string += f"{debug}\n" if show_debug else ""
    return output_string


def add_to_snake(snake: Snake, direction: Direction | None):
    """Add point to end of snake in the opposite direction of snake travel.

    :param snake: The snake to add a point to.
    :param direction: The snake's travel direction.
    """

    row = 0
    col = 0

    match direction:
        case Direction.up:
            row = (snake[-1][0] + 1) % BOARD_ROWS
            col = snake[-1][1]
        case Direction.down:
            row = (snake[-1][0] - 1) % BOARD_ROWS
            col = snake[-1][1]
        case Direction.left:
            row = snake[-1][0]
            col = (snake[-1][1] + 1) % BOARD_COLS
        case Direction.right:
            row = snake[-1][0]
            col = (snake[-1][1] - 1) % BOARD_COLS

    row = row if row >= 0 else BOARD_ROWS - 1
    col = col if col >= 0 else BOARD_COLS - 1

    snake.append((row, col))


def render_board(
    snake: Snake,
    direction: Direction | None,
    food_point: Point | None = None,
) -> tuple[Board, Point]:
    """Render board for printing.

    This function combines all of the elements on a single board and
    uses the knowledge of everything to determine the next food point
    location.

    :param snake: The snake to render.
    :param direction: The current direction of the snake.
    :param food_point: The location of the food.
    :return: The Updated board and food point
    """

    taken_points = set()

    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

    match direction:
        case Direction.up:
            board[snake[0][0]][snake[0][1]] = "^"
        case Direction.down:
            board[snake[0][0]][snake[0][1]] = "v"
        case Direction.left:
            board[snake[0][0]][snake[0][1]] = "<"
        case Direction.right:
            board[snake[0][0]][snake[0][1]] = ">"
        case _:
            board[snake[0][0]][snake[0][1]] = "*"

    taken_points.add(snake[0])

    for row, col in snake[1:]:
        board[row][col] = "*"
        taken_points.add((row, col))

    food_point = food_point or choice(list(ALL_POINTS - taken_points))

    board[food_point[0]][food_point[1]] = "F"

    return board, food_point


def move(snake: Snake, direction: Direction | None):
    """Move snake towards a direction.

    :param snake: The snake to move
    :param direction: The direction to move towards
    :return: Updated snake after move
    """

    key_to_head: dict[Direction | None, Point] = {
        Direction.up: ((snake[0][0] - 1) % BOARD_ROWS, snake[0][1]),
        Direction.down: ((snake[0][0] + 1) % BOARD_ROWS, snake[0][1]),
        Direction.left: (snake[0][0], (snake[0][1] - 1) % BOARD_COLS),
        Direction.right: (snake[0][0], (snake[0][1] + 1) % BOARD_COLS),
    }

    if new_head := key_to_head.get(direction):

        mutatated_snake: Snake = [new_head]

        for point in snake[0:-1]:
            mutatated_snake.append(point)

        return mutatated_snake

    return snake


def game_loop(win):
    win.nodelay(True)

    snake: Snake = [(randint(0, BOARD_ROWS - 1), randint(0, BOARD_COLS - 1))]
    food_point: Point | None = None
    current_direction: Direction | None = None
    next_direction = None
    board: Board | None = None
    score = 0

    lost = False

    while not lost:
        board, food_point = render_board(
            snake,
            current_direction,
            food_point,
        )

        try:
            next_direction = Direction(win.getch())
        except ValueError:
            pass

        next_snake = move(snake, next_direction)
        next_head_does_not_colide_with_itself = (
            len(next_snake) == 1 or next_snake[0] != snake[1]
        )

        # prevent moving in the opposite direction of travel
        if next_head_does_not_colide_with_itself:
            current_direction = next_direction
        else:
            next_direction = current_direction

        if next_head_does_not_colide_with_itself:
            snake = next_snake

        if snake[0] == food_point:
            add_to_snake(snake, current_direction)
            food_point = None
            score += 10

        if snake[0] in snake[1:]:
            lost = True

        win.addstr(
            0,
            0,
            format_board_string(
                board,
                score,
                {
                    "food_point": food_point,
                    "current_direction": str(current_direction),
                    "does_not_colide": next_head_does_not_colide_with_itself,
                    "next_snake": next_snake,
                    "snake": snake,
                },
                show_debug=False,
            ),
        )

        win.refresh()

        sleep(0.1)

    return board, score


if __name__ == "__main__":
    board, score = curses.wrapper(game_loop)

    if board:
        print(format_board_string(board, score))

    print("You lost.")
