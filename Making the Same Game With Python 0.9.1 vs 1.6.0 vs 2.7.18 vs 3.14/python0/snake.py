# Snake for Python0.
from rand import choice, rand

BOARD_ROWS = 20
BOARD_COLS = 20
ALL_POINTS = [] 
for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
        ALL_POINTS.append((row, col))
PYTHON_VERSION = '0.9.1' 
UP = 'k'
DOWN = 'j'
LEFT = 'h'
RIGHT = 'l'
NONE = '-1'
def base10_to_string(num,res_string):
    last_digit = num % 10 
    if last_digit = 1:
        res_string = '1' + res_string 
    if last_digit = 2:
        res_string = '2' + res_string 
    if last_digit = 3:
        res_string = '3' + res_string 
    if last_digit = 4:
        res_string = '4' + res_string 
    if last_digit = 5:
        res_string = '5' + res_string 
    if last_digit = 6:
        res_string = '6' + res_string 
    if last_digit = 7:
        res_string = '7' + res_string 
    if last_digit = 8:
        res_string = '8' + res_string 
    if last_digit = 9:
        res_string = '9' + res_string 
    if num = 0:
        return res_string
    if last_digit = 0:
        res_string = '0' + res_string 
    base10_to_string(num/10, res_string)
def format_board_string(board, score):
    # Format the board string for printing.
    # :param board: The board to print.
    # :param score: The score to print.
    # :return: The board string.
    score_string = ''
    base10_to_string(score,score_string)
    output_string = PYTHON_VERSION + '\n'
    output_string = output_string + 'score: ' + score_string + '\n'
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            output_string = output_string + board[row][col] + ' '
        output_string = output_string + '\n'
    return output_string
def add_to_snake(snake, direction):
    #Add point to end of snake in the opposite direction of snake travel.
    #:param snake: The snake to add a point to.
    #:param direction: The snake's travel direction.
    row = 0
    col = 0
    direction_map = {}
    direction_map[UP] =  ((snake[len(snake)-1][0] + 1) % BOARD_ROWS, snake[len(snake)-1][1])
    direction_map[DOWN]= ((snake[len(snake)-1][0] - 1) % BOARD_ROWS, snake[len(snake)-1][1])
    direction_map[LEFT]= (snake[len(snake)-1][0], (snake[len(snake)-1][1] + 1) % BOARD_COLS)
    direction_map[RIGHT]= (snake[len(snake)-1][0], (snake[len(snake)-1][1] - 1) % BOARD_COLS)
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
def render_board(snake,direction,food_point):
    # Render board for printing.
    # This function combines all of the elements on a single board and
    # uses the knowledge of everything to determine the next food point
    # location.
    # :param snake: The snake to render.
    # :param direction: The current direction of the snake.
    # :param food_point: The location of the food.
    # :return: The Updated board and food point
    taken_points = [] 
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(' ')
        board.append(row)
    direction_map = {}
    direction_map[UP]= '^'
    direction_map[DOWN]= 'v'
    direction_map[LEFT]= '<'
    direction_map[RIGHT]= '>'
    direction_map[NONE]= '*'
    board[snake[0][0]][snake[0][1]] = direction_map[direction]
    taken_points.append(snake[0])
    for row, col in snake[1:]:
        board[row][col] = '*'
        taken_points.append((row, col))
    all_points_copy = ALL_POINTS[:]
    for point in taken_points:
        for i in range(len(all_points_copy) -1):
            if all_points_copy[i] = point:
                del all_points_copy[i]
    if food_point:
        food_point = food_point
    else:
        food_point = choice(all_points_copy)
    board[food_point[0]][food_point[1]] = 'F'
    return board, food_point
def move(snake, direction):
    # Move snake towards a direction.
    # :param snake: The snake to move
    # :param direction: The direction to move towards
    # :return: Updated snake after move
    key_to_head = {}
    key_to_head[UP] = ((snake[0][0] - 1) % BOARD_ROWS, snake[0][1])
    key_to_head[DOWN] = ((snake[0][0] + 1) % BOARD_ROWS, snake[0][1])
    key_to_head[LEFT] = (snake[0][0], (snake[0][1] - 1) % BOARD_COLS)
    key_to_head[RIGHT] = (snake[0][0], (snake[0][1] + 1) % BOARD_COLS)
    new_head = key_to_head[direction]
    if new_head:
        mutatated_snake = [new_head]
        for point in snake[0:-1]:
            mutatated_snake.append(point)
        return mutatated_snake
    return snake
def game_loop():
    snake = [(rand() % BOARD_ROWS, rand() % BOARD_COLS)]
    food_point = None
    current_direction = NONE 
    next_direction = NONE 
    board = None
    score = 0
    lost = 0 
    while not lost:
        board, food_point = render_board(snake,current_direction,food_point)
        print format_board_string(board, score)
        ch = raw_input('press (h,j,k,l) to set the snake\'s direction and ENTER to move: ') 
        if ch in [UP,DOWN,LEFT,RIGHT]:
            next_direction = ch
        next_snake = move(snake, next_direction)
        # prevent moving in the opposite direction of travel
        if len(next_snake) = 1 or not(next_snake[0] = snake[1]):
            current_direction = next_direction
        else:
            next_direction = current_direction
        if len(next_snake) = 1 or not(next_snake[0] = snake[1]):
            snake = next_snake
        if snake[0] = food_point:
            add_to_snake(snake, current_direction)
            food_point = None
            score = score + 10
        if snake[0] in snake[1:]:
            lost = 1 
    print 'You lost.'

game_loop()
