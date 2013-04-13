import math
import random
import ctypes
import sys
from csearch import AStarSearch
from csearch import Successors

BOARD_WIDTH  = 3
BOARD_HEIGHT = 3

GOAL_STATE = [
	1, 2, 3,
	4, 5, 6,
	7, 8, 0
]

# A collection of all of the game board
# states that was a possibility.
# This is used to ensure that the GC
# doesn't take our references away from us.
states = []

# Generate a random game board.
def randomize_board( board, width, height, only_solvable ):
	if not(only_solvable):
		# This may or may not produce a board with a solution.
		length = width * height

		numbers = [ i for x in range(0, length) ]

		for i in range(length - 1, 0, -1):
			random_index = random.randint( 0, i + 1)
			chosen = numbers[ random_index ]

			numbers[ random_index ] = numbers[ i ]
			board[ i ] = chosen
	else:
		# Start with the goal
		current_board = list(GOAL_STATE)

		potential_moves = [
			( -1,  0 ),
			(  1,  0 ),
			(  0, -1 ),
			(  0,  1 )
		]

		# Attempt to make 14 moves to scramble the goal state.
		# This new state will be the start state.
		moves = 2
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

# Create a new game board.
def create_board( board, index, move_index ):
	new_board = list(board)

	tmp = new_board[ index ]
	new_board[ index ] = new_board[ move_index ]
	new_board[ move_index ] = tmp

	states.append( new_board )
	return new_board

# Given a game board, what are all of the possible
# game boards that can result from all of the potential
# moves.
def get_possible_moves( current_board, successors_handle ):
	successors = Successors(successors_handle)

	print "Finding successors of:"
	debug_board( current_board )

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

	assert( found_empty )

	if found_empty:
		for m in range(0, 4):
			move_x = emptyX + potential_moves[ m ][ 0 ]
			move_y = emptyY + potential_moves[ m ][ 1 ]

			if move_x >= 0 and move_x < BOARD_WIDTH and move_y >= 0 and move_y < BOARD_HEIGHT:
				# make the move
				move_index = BOARD_WIDTH * move_y + move_x
				print "empty = ({},{}), index = {}".format(emptyX, emptyY, BOARD_WIDTH * emptyY + emptyX)
				print "move = ({},{}),  index = {}".format( move_x, move_y, move_index )
				new_board = create_board( current_board, index, move_index )

				print "Successor"
				debug_board( new_board )
				successors.push( new_board )

	sys.stdin.read(1)

# Draw a game board board. Step 0 implies no moves have
# occurred and is our initial board.
def draw_board( step, board ):
	for y in range(0, BOARD_HEIGHT):
		if y == 1:
			if step == 0:
				print ' {0:10} {1:3} |{2:1d}|{3:1d}|{4:1d}|'.format( "Initial", "",board[ BOARD_WIDTH * y + 0 ],  board[ BOARD_WIDTH * y + 1 ],  board[ BOARD_WIDTH * y + 2 ] );
			else:
				print ' {0:10} {1:3} |{2:1d}|{3:1d}|{4:1d}|'.format( "Step", step, board[ BOARD_WIDTH * y + 0 ],  board[ BOARD_WIDTH * y + 1 ],  board[ BOARD_WIDTH * y + 2 ] );
		else:
				print ' {0:10} {1:3} |{2:1d}|{3:1d}|{4:1d}|'.format( "", "",       board[ BOARD_WIDTH * y + 0 ],  board[ BOARD_WIDTH * y + 1 ],  board[ BOARD_WIDTH * y + 2 ] );

	print ""

def debug_board( board ):
	print ' |{0:1d}|{1:1d}|{2:1d}|'.format( board[ 0 ],  board[ 1 ],  board[ 2 ] );
	print ' |{0:1d}|{1:1d}|{2:1d}|'.format( board[ 3 ],  board[ 4 ],  board[ 5 ] );
	print ' |{0:1d}|{1:1d}|{2:1d}|'.format( board[ 6 ],  board[ 7 ],  board[ 8 ] );

	print ""


# The sum of the manhattan distance of each number between
# game boards.
def heuristic( board1, board2 ):
	sum = 0

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
def cost( board1, board2 ):
	return 1

# Two game board states are equal if every number is in the same
# position in both.
def board_compare( board1, board2 ):
	for i in range(0, BOARD_WIDTH * BOARD_HEIGHT):
		if board1[ i ] != board2[ i ]:
			return 1

	return 0


def state_hash(board):
	return hash(tuple(board))

def main():
	random.seed( None )

	astar = AStarSearch( board_compare, state_hash, heuristic, cost, get_possible_moves )

	# Produce a solvable random board
	initial_state = list(GOAL_STATE)
	randomize_board( initial_state, BOARD_WIDTH, BOARD_HEIGHT, True )

	states.append( initial_state )

	if astar.find( GOAL_STATE, initial_state ):
		step = 0;
		board = astar.firstState()
		while board != None:

			draw_board( step, board )
			print "\n"

			step += 1
			board = astar.nextState()

		astar.cleanup( )
	else:
		# No solution found.
		print "No solution found for:\n\n"
		draw_board( 0, initial_state );

main()

