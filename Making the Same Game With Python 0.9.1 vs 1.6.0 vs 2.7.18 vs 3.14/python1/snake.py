"""Snake for Python1."""

import curses
from random import choice, randint
from sys import version
from time import sleep

BOARD_ROWS = 20
BOARD_COLS = 20
ALL_POINTS = [] 
for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
        ALL_POINTS.append((row, col))

PYTHON_VERSION = version.replace("\n", " ")

UP = 259
DOWN = 258
LEFT = 260
RIGHT = 261
NONE = -1

def format_board_string(board, score, debug=None, show_debug=None):
    """Format the board string for printing.

    :param board: The board to print.
    :param score: The score to print.
    :param debug: Debug information to print at the bottom of the board.
    :param show_debug: If the debug information should be shown.
    :return: The board string.
    """
    output_string = version + "\n"
    output_string = output_string + "score: " + str(score) + "\n"

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            output_string = output_string + board[row][col] + " "
        output_string = output_string + "\n"

    if show_debug:
        output_string = output_string + str(debug) + "\n"

    return output_string


def add_to_snake(snake, direction):
    """Add point to end of snake in the opposite direction of snake travel.

    :param snake: The snake to add a point to.
    :param direction: The snake's travel direction.
    """

    row = 0
    col = 0

    direction_map = {
        UP: ((snake[-1][0] + 1) % BOARD_ROWS, snake[-1][1]),
        DOWN: ((snake[-1][0] - 1) % BOARD_ROWS, snake[-1][1]),
        LEFT: (snake[-1][0], (snake[-1][1] + 1) % BOARD_COLS),
        RIGHT: (snake[-1][0], (snake[-1][1] - 1) % BOARD_COLS),
    }

    row, col = direction_map[direction]

    if row >= 0:
        row = row
    else:
        row = BOARD_ROWS - 1

    if col >= 0:
        col = col
    else:
        col = BOARD_COLS - 1

    snake.append((row, col))


def render_board(
    snake,
    direction,
    food_point,
):
    """Render board for printing.

    This function combines all of the elements on a single board and
    uses the knowledge of everything to determine the next food point
    location.

    :param snake: The snake to render.
    :param direction: The current direction of the snake.
    :param food_point: The location of the food.
    :return: The Updated board and food point
    """

    taken_points = [] 

    board = []

    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(" ")
        board.append(row)

    direction_map = {
        UP: "^",
        DOWN: "v",
        LEFT: "<",
        RIGHT: ">",
        NONE: "*",
    }

    board[snake[0][0]][snake[0][1]] = direction_map[direction]
    taken_points.append(snake[0])

    for row, col in snake[1:]:
        board[row][col] = "*"
        taken_points.append((row, col))

    all_points_copy = ALL_POINTS[:]

    for point in taken_points:
        all_points_copy.remove(point)

    food_point = food_point or choice(all_points_copy)

    board[food_point[0]][food_point[1]] = "F"

    return board, food_point


def move(snake, direction):
    """Move snake towards a direction.

    :param snake: The snake to move
    :param direction: The direction to move towards
    :return: Updated snake after move
    """

    key_to_head = {
        UP: ((snake[0][0] - 1) % BOARD_ROWS, snake[0][1]),
        DOWN: ((snake[0][0] + 1) % BOARD_ROWS, snake[0][1]),
        LEFT: (snake[0][0], (snake[0][1] - 1) % BOARD_COLS),
        RIGHT: (snake[0][0], (snake[0][1] + 1) % BOARD_COLS),
    }

    new_head = key_to_head.get(direction)

    if new_head:

        mutatated_snake = [new_head]

        for point in snake[0:-1]:
            mutatated_snake.append(point)

        return mutatated_snake

    return snake


def game_loop(win):
    win.nodelay(1)

    snake = [(randint(0, BOARD_ROWS - 1), randint(0, BOARD_COLS - 1))]
    food_point = None
    current_direction = NONE 
    next_direction = NONE 
    board = None
    score = 0

    lost = 0 

    while not lost:
        board, food_point = render_board(
            snake,
            current_direction,
            food_point,
        )

        ch = win.getch()
        if ch in [UP,DOWN,LEFT,RIGHT]:
            next_direction = ch

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
            score = score + 10

        if snake[0] in snake[1:]:
            lost = 1 

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
                show_debug=0,
            ),
        )

        win.refresh()

        sleep(0.1)

    return board, score


if __name__ == "__main__":
    board, score = curses.wrapper(game_loop)

    if board:
        print format_board_string(board, score)

    print "You lost."
