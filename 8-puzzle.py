import math
import random
import ctypes
from csearch import AStarSearch

BOARD_WIDTH  = 3
BOARD_HEIGHT = 3

puzzle_state = ctypes.c_int * (BOARD_HEIGHT * BOARD_WIDTH)

GOAL_STATE = puzzle_state(
	1, 2, 3,
	4, 5, 6,
	7, 8, 0
)

# A collection of all of the game board
# states that was a possibility.
states = []

# Generate a random game board.
def randomize_board( board, width, height, only_solvable ):
	if not(only_solvable):
		# This may or may not produce a board with a solution.
		length = width * height

		numbers = puzzle_state([ i for x in range(0, length) ])

		for i in range(len - 1, 0, -1):
			random_index = random.randint( 0, i + 1)
			chosen = numbers[ random_index ]

			numbers[ random_index ] = numbers[ i ]
			board[ i ] = chosen
	else:
		# Start with the goal
		current_board = (GOAL_STATE)

		potential_moves = [
			( -1,  0 ),
			(  1,  0 ),
			(  0, -1 ),
			(  0,  1 )
		]

		# Attempt to make 14 moves to scramble the goal state.
		# This new state will be the start state.
		moves = 14;
		while moves > 0:
			moves -= 1

			for y in range(0, height):
				for x in range(0, width):
					index = width * y + x

					# loop until you find the empty space to make moves 
					if current_board[ index ] == 0:
						moved = False

						while not(moved):
							m = random.randint(0, 3)
							move_x = x + potential_moves[ m ][ 0 ]
							move_y = y + potential_moves[ m ][ 1 ]

							if move_x >= 0 and move_x < width and move_y >= 0 and move_y < height:
								# make the move
								move_index = width * move_y + move_x

								tmp = current_board[ index ]
								current_board[ index ] = current_board[ move_index ]
								current_board[ move_index ] = tmp

								moved = True

		# copy randomized board to the game board
		length = width * height
		for i in range(0, length): 
			board[ i ] = current_board[ i ]

# Create a new game board state.
def create_state( board, size, index, move_index ):
	new_board = puzzle_state(board)

	tmp = new_board[ index ]
	new_board[ index ] = new_board[ move_index ]
	new_board[ move_index ] = tmp

	states.append( new_board )
	return new_board

# Given a game board state, what are all of the possible
# game boards that can result from all of the potential
# moves. 
def get_possible_moves( state, successors ):
	current_board = puzzle_state( ctypes.cast( state, ctypes.c_long_p ).contents )
	print current_board

	potential_moves = [
		( -1,  0 ),
		(  1,  0 ),
		(  0, -1 ),
		(  0,  1 )
	]

	emptyX = None
	emptyY = None
	index = 0
	found_empty = False

	for y in range(0, BOARD_HEIGHT):
		for x in range(0, BOARD_WIDTH):
			index = BOARD_WIDTH * y + x

			# loop until you find the empty space to make moves
			if current_board[ index ] == 0:
				found_empty = True
				emptyX = x
				emptyY = y

	if found_empty:
		for m in range(0, 3):
			move_x = emptyX + potential_moves[ m ][ 0 ]
			move_y = emptyY + potential_moves[ m ][ 1 ]

			if move_x >= 0 and move_x < BOARD_WIDTH and move_y >= 0 and move_y < BOARD_HEIGHT:
				# make the move
				move_index = BOARD_WIDTH * move_y + move_x

				new_state = create_state( current_board, BOARD_WIDTH * BOARD_HEIGHT, index, move_index )

				successorsPush( successors, new_state )

# Draw a game board state. Step 0 implies no moves have
# occurred and is our initial state.
def draw_board( step, board ):
	for y in range(0, BOARD_HEIGHT - 1):
		if y == 1:
			if step == 0:
				print ' {0:10}     '.format("Initial")
			else:
				print ' {0:10} {1:3d} '.format("Step", step)
		else:
			print '                '

		for x in range(0, BOARD_WIDTH - 1):
			index = BOARD_WIDTH * y + x
			num   = board[ index ]

			if num:
				print '|{0:1d}'.format(num)
			else:
				print '| ' 

		print '|\n'

# The sum of the manhattan distance of each number between
# game boards.
def heuristic( state1, state2 ):
	board1 = puzzle_state(state1)

	draw_board( 0,  state1 )

	board2 = puzzle_state(state2)
	#board1 = state1[0]
	#board2 = state2[0]

	sum = 0;

	for y1 in range(0, BOARD_HEIGHT):
		for x1 in range(0, BOARD_WIDTH):
			index1 = BOARD_WIDTH * y1 + x1
			for y2 in range(0, BOARD_HEIGHT):
				for x2 in range(0, BOARD_WIDTH):
					index2 = BOARD_WIDTH * y2 + x2

					if board1[ index1 ] == board2[ index2 ]:
						sum += int( math.fabs( x2 - x1 ) + math.fabs( y2 - y1 ))

	return sum

# The cost of making a move is 1.
def cost( state1, state2 ):
	return 1

# Two game board states are equal if every number is in the same 
# position in both.
def board_compare( state1, state2 ):
	if state1 == state2:
		return 0
	elif state1 < state2:
		return -1
	else:
		return 1

def state_hash(state):
	return hash(state)

def main():
	random.seed( None )

	astar = AStarSearch( board_compare, state_hash, heuristic, cost, get_possible_moves )

	# Produce a solvable random board
	initial_state = puzzle_state()
	randomize_board( initial_state, BOARD_WIDTH, BOARD_HEIGHT, True )
	states.append( initial_state )

	if astar.find( GOAL_STATE, initial_state ):
		step = 0;
		state = astar.firstState()
		while state != None:
			board = puzzle_state(state)

			draw_board( step, board )
			print "\n"
			
			step += 1
			state = astar.nextState()

		astar.cleanup( )
	else:
		# No solution found. 
		print "No solution found for:\n\n"
		draw_board( 0, initial_state );


main()
	
