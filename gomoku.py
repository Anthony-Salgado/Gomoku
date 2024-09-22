
from importlib.resources import open_binary


def is_sq_in_board(board, y, x):
    return y < 8 and x < 8 and x >= 0 and y >= 0

def is_empty(board):
    for i in range (8):
        for j in range (8):
            if board[i][j] != " ":
                return False
    return True

def is_full(board):
    for y in range (8):
        for x in range(8):
            if board[y][x] == " ":
                return False
    return True

def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):

    y_prior_start = y_start - d_y
    x_prior_start = x_start - d_x
    y_after_end = y_start + length * d_y
    x_after_end = x_start + length * d_x

    if board[y_start][x_start] == " ":
        return False
    if is_sq_in_board(board, y_prior_start, x_prior_start):
        if board[y_prior_start][x_prior_start] == col:
            return False
    if is_sq_in_board(board, y_after_end, x_after_end):
        if board[y_after_end][x_after_end] == col:
            return False
    for i in range (length):
        if board[y_start + d_y * i][x_start + d_x * i] != col:
            return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):

    #location of the square prior to the starting index of the sequence
    x_prior_start = x_end - length * d_x
    y_prior_start = y_end - length * d_y

    #check if the square is still in board and idle
    sq_prior_start = is_sq_in_board(board, y_prior_start, x_prior_start) and board[y_prior_start][x_prior_start] == " "
    sq_after_end = is_sq_in_board(board, y_end + d_y, x_end + d_x) and board[y_end + d_y][x_end + d_x] == " "
    if sq_prior_start and sq_after_end:
        return "OPEN"
    elif not sq_after_end and not sq_prior_start:
        return "CLOSED"
    else:
        return "SEMIOPEN"
    


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0

    #difference between the last and the first of the sequence = length - 1
    y_end = y_start + (length - 1) * d_y 
    x_end = x_start + (length - 1) * d_x

    while is_sq_in_board(board, y_end, x_end):
        #check if the sequence is complete and matches the colour 
        if is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
            match is_bounded(board, y_end, x_end, length, d_y, d_x):
                case "OPEN":
                    open_seq_count += 1
                case "SEMIOPEN":
                    semi_open_seq_count += 1
                case _:
                    open_seq_count = 0
                    semi_open_seq_count = 0
        y_end += d_y
        x_end += d_x
        y_start += d_y
        x_start += d_x
    return open_seq_count, semi_open_seq_count


def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    seq_count = [open_seq_count, semi_open_seq_count]

    #Horizontal check
    hor_start = 0
    while hor_start < 8:
        seq_count[0] += detect_row(board, col, hor_start, 0, length, 0, 1)[0]
        seq_count[1] += detect_row(board, col, hor_start, 0, length, 0, 1)[1]
        hor_start += 1

    #Vertical check
    vert_start = 0
    while vert_start < 8:
        seq_count[0] += detect_row(board, col, 0, vert_start, length, 1, 0)[0]
        seq_count[1] += detect_row(board, col, 0, vert_start, length, 1, 0)[1]
        vert_start += 1

    #Upper Diagonal check Top down (middle diagonal line included)
    upper_diag_start = 0
    while upper_diag_start < 8:
        seq_count[0] += detect_row(board, col, 0, upper_diag_start, length, 1, 1)[0]
        seq_count[1] += detect_row(board, col, 0, upper_diag_start, length, 1, 1)[1]
        upper_diag_start += 1

    #Lower Diagonal check Top down
    lower_diag_start = 1
    while lower_diag_start < 8:
        seq_count[0] += detect_row(board, col, lower_diag_start, 0, length, 1, 1)[0]
        seq_count[1] += detect_row(board, col, lower_diag_start, 0, length, 1, 1)[1]
        lower_diag_start += 1

    #Upper Diagonal check Bottom up (middle diagonal line included)
    upper_diag_start = 7
    while upper_diag_start >= 0:
        seq_count[0] += detect_row(board, col, upper_diag_start, 0, length, -1, 1)[0]
        seq_count[1] += detect_row(board, col, upper_diag_start, 0, length, -1, 1)[1]
        upper_diag_start -= 1
        
    #Lower Diagonal check Bottom up 
    lower_diag_start = 1
    while lower_diag_start < 8:
        seq_count[0] += detect_row(board, col, 7, lower_diag_start, length, -1, 1)[0]
        seq_count[1] += detect_row(board, col, 7, lower_diag_start, length, -1, 1)[1]
        lower_diag_start += 1
    
    tup = tuple(seq_count)

    return tup

def search_max(board):
    max_score = None
    move_y, move_x = None, None
    for y in range(8):
        for x in range(8):
            if board[y][x] == " ":
                board[y][x] = "b"
                if max_score == None or score(board) > max_score:
                    max_score = score(board)
                    move_y = y
                    move_x = x
                board[y][x] = " "
    return move_y, move_x


def is_win(board):
    if detect_rows(board, "b", 5) > (0, 0):
        return "Black won"
    elif detect_rows(board, "w", 5) > (0, 0):
        return "White won"
    elif is_full(board):
        return "Draw"
    else:
        return "Continue playing"
    



def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])



def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x





def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    some_tests()
