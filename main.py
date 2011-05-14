#!/usr/bin/python

"""
-------------
| x | o | x |
-------------
| o | o | x |
-------------
| x | x | o |
-------------
"""

board = [[" "," "," "],[" "," "," "],[" "," "," "],]
player = "x"
winner = None
computer_players = []

def setup_players():
	global computer_players
	valid_setup = False
	while (not valid_setup):
		try:
			nop = int(raw_input("Number of human players: "))
			if (nop > 2 or nop < 0): raise Exception("Invalid number of players!")
			if (nop == 0):
				computer_players = ["x", "o"]
			elif (nop == 1):
				h_player = raw_input("Enter player type (x or o): ")
				if (h_player != "x" and h_player != "o"): raise Exception("Invalid player type!")
				if (h_player == "x"): computer_players = ["o"]
				if (h_player == "o"): computer_players = ["x"]
		except ValueError as e:
			print "Invalid Answer!"
			continue
		except Exception as e:
			print e
			continue
		valid_setup = True
		
def check_for_win(b):
	"""
	check_for_win
	
	checks to see what state the board is in as far as whether or not
	there is a winner
	
	returns x,o for a winner, - for a a tie, or none if no win
	"""
	# Horizontals
	if (b[0][0] == b[0][1] == b[0][2] != " "): return b[0][0]
	if (b[1][0] == b[1][1] == b[1][2] != " "): return b[1][0]
	if (b[2][0] == b[2][1] == b[2][2] != " "): return b[2][0]
	
	# Verticals
	if (b[0][0] == b[1][0] == b[2][0] != " "): return b[0][0]
	if (b[0][1] == b[1][1] == b[2][1] != " "): return b[0][1]
	if (b[0][2] == b[1][2] == b[2][2] != " "): return b[0][2]
	
	# Diagonals
	if (b[0][0] == b[1][1] == b[2][2] != " "): return b[0][0]
	if (b[0][2] == b[1][1] == b[2][0] != " "): return b[0][2]
	
	for row in b:
		for col in row:
			# if any square is blank, there is no tie
			if col == " ": return None
	
	# Catch All for tie
	return "-"
def get_open_spaces(board):
	spaces = []
	for i in range(0, len(board)):
		for j in range(0, len(board[i])):
			if (board[i][j] == " "):
				spaces.append([i,j])
	return spaces
		
	
def find_best_move(b, player):
	spaces = get_open_spaces(b)
	move = []
	score = -100000
	i_move = imminent_win(b, switch_player(player))
	if (i_move):
		return i_move
	for space in spaces:
		e_score = get_move_score(space[0], space[1], list(b[:]) ,player, player, 1)
		if (e_score > score):
			score = e_score
			move = [space[0], space[1]]
	return move
	
def imminent_win(b, player):
	spaces = get_open_spaces(b)
	move = None
	for space in spaces:
		b[space[0]][space[1]] = player
		if (check_for_win(b) == player):
			move = [space[0],space[1]]
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
	if (was_win):
		if (was_win == eval_player):
			score = 1 / move_count
		elif(was_win == "-"):
			score = 0
		else:
			score = -1 / move_count
	else:
		spaces = get_open_spaces(board)
		for space in spaces:
			score += get_move_score(space[0], space[1], list(b[:]) ,curr_player, eval_player, move_count + 1)
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
			row = int(raw_input("Enter row: ")) - 1
			if (row < 0 or row > 2): raise Exception("Invalid row given!")
			col = int(raw_input("Enter col: ")) - 1
			if (col < 0 or col > 2): raise Exception("Invalid col given!")
		except ValueError as e:
			print "Must be a numeric value"
			continue
		except Exception as e:
			print e
			continue
		if (b[row][col] == " "):
			valid_move = True
		else:
			print "Invalid move!"
	return (row, col)
	
def print_board(b):
	print " ", " ", "1", " ", "2", " ", "3"
	print " ", "-" * 13
	print "1 |", b[0][0], "|", b[0][1], "|", b[0][2], "|"
	print " ", "-" * 13
	print "2 |", b[1][0], "|", b[1][1], "|", b[1][2], "|"
	print " ", "-" * 13
	print "3 |", b[2][0], "|", b[2][1], "|", b[2][2], "|"
	print " ","-" * 13
	
def switch_player(p):
	if (p == "x"): return "o"
	else: return "x"

setup_players()
while not winner:
	print_board(board)
	if (player in computer_players):
		print "Computer is THINKING!"
		p_move = find_best_move(board, player)
	else:
		p_move = request_move(board)
	move(p_move[0], p_move[1], player, board)
	winner = check_for_win(board)
	player = switch_player(player)


print_board(board)
if (winner == "-"):
	print "Players tied!"
else:
	print "Player %s wins!" % winner