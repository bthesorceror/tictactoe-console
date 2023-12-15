from math import pow

board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
player = "x"
winner = None
computer_players = []


def setup_players():
    global computer_players
    valid_setup = False
    while not valid_setup:
        try:
            nop = int(input("Number of human players: "))
            if not (0 <= nop <= 2):
                raise ValueError("Invalid number of players!")

            if nop == 0:
                computer_players = ["x", "o"]
            elif nop == 1:
                h_player = input("Enter player type (x or o): ")
                if h_player not in ["x", "o"]:
                    raise ValueError("Invalid player type!")
                computer_players = ["o"] if h_player == "x" else ["x"]
        except ValueError as e:
            print('Invalid Answer!')
            continue
        except Exception as e:
            print(e)
            continue
        valid_setup = True


def check_for_win(b):
    # Horizontals, Verticals, and Diagonals
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != " " or \
                b[0][i] == b[1][i] == b[2][i] != " ":
            return b[i][i]

    if b[0][0] == b[1][1] == b[2][2] != " " or \
            b[0][2] == b[1][1] == b[2][0] != " ":
        return b[1][1]

    for row in b:
        for col in row:
            if col == " ":
                return None

    return "-"


def get_open_spaces(board):
    spaces = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                spaces.append([i, j])
    return spaces


def find_best_move(b, player):
    spaces = get_open_spaces(b)
    move = []
    score = -100000
    i_move = imminent_win(b, switch_player(player))
    if i_move:
        return i_move
    for space in spaces:
        e_score = get_move_score(space[0], space[1], list(map(list, b)), player, player, 1)
        if e_score > score:
            score = e_score
            move = [space[0], space[1]]
    return move


def imminent_win(b, player):
    spaces = get_open_spaces(b)
    move = None
    for space in spaces:
        b[space[0]][space[1]] = player
        if check_for_win(b) == player:
            move = [space[0], space[1]]
            b[space[0]][space[1]] = " "
            break
        b[space[0]][space[1]] = " "
    return move


def get_move_score(row, col, b, curr_player, eval_player, move_count):
    orig = b[row][col]
    b[row][col] = curr_player
    curr_player = switch_player(curr_player)
    was_win = check_for_win(b)
    score = 0
    if was_win:
        if was_win == eval_player:
            score = 1 / pow(move_count, move_count)
        elif was_win == "-":
            score = 0
        else:
            score = -1 / pow(move_count, move_count)
    else:
        spaces = get_open_spaces(b)
        for space in spaces:
            score += get_move_score(space[0], space[1], list(map(list, b)), curr_player, eval_player, move_count + 1)
    b[row][col] = orig
    return score


def move(row, col, p, b):
    b[row][col] = p


def request_move(b):
    row = None
    col = None
    valid_move = False
    while not valid_move:
        try:
            row = int(input("Enter row: ")) - 1
            if not (0 <= row <= 2):
                raise ValueError("Invalid row given!")
            col = int(input("Enter col: ")) - 1
            if not (0 <= col <= 2):
                raise ValueError("Invalid col given!")
        except ValueError as e:
            print("Must be a numeric value")
            continue
        if b[row][col] == " ":
            valid_move = True
        else:
            print("Invalid move!")
    return row, col


def print_board(b):
    print(" ", " ", "1", " ", "2", " ", "3")
    print(" ", "-" * 13)
    for i in range(3):
        print(f"{i + 1} |", b[i][0], "|", b[i][1], "|", b[i][2], "|")
        print(" ", "-" * 13)


def switch_player(p):
    return "o" if p == "x" else "x"


setup_players()
while not winner:
    print_board(board)
    if player in computer_players:
        print("Computer is THINKING!")
        p_move = find_best_move(board, player)
    else:
        p_move = request_move(board)
    move(p_move[0], p_move[1], player, board)
    winner = check_for_win(board)
    player = switch_player(player)

print_board(board)
if winner == "-":
    print("Players tied!")
else:
    print(f"Player {winner} wins!")
