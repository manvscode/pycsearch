# Copyright (C) 2010 by Joseph A. Marrero
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import math
import random
import ctypes
import sys
from csearch import AStarSearch
from csearch import Successors

class Board:
	WIDTH  = 3
	HEIGHT = 3
	GOAL_STATE = [
		1, 2, 3,
		4, 5, 6,
		7, 8, 0
	]
	state = []
	# A collection of all of the game board
	# states that are possibilities.
	# This is used to ensure that the GC
	# doesn't take our references away from us.
	states = []

	def __init__( self, board = None ):
		if board == None:
			self.state = list(self.GOAL_STATE)
		else:
			self.state = list(board)

		Board.states.append( self ) # this is needed to avoid self getting garbage collected

	@staticmethod
	def goal():
		goal_state = Board( Board.GOAL_STATE )
		return goal_state

	# Generate a random game board.
	def randomize( self, only_solvable ):
		if not(only_solvable):
			# This may or may not produce a board with a solution.
			length = self.WIDTH * self.HEIGHT

			numbers = [ i for x in xrange(0, length) ]

			for i in xrange(length - 1, 0, -1):
				random_index = random.randint( 0, i + 1)
				chosen = numbers[ random_index ]
				numbers[ random_index ] = numbers[ i ]
				self.state[ i ] = chosen
		else:
			# Start with the goal
			current_board = Board.goal()

			potential_moves = [
				( -1,  0 ),
				(  1,  0 ),
				(  0, -1 ),
				(  0,  1 )
			]

			# Attempt to make 14 moves to scramble the goal state.
			# This new state will be the start state.
			moves = 14
			while moves > 0:
				moves -= 1

				for y in xrange(0, self.HEIGHT):
					for x in xrange(0, self.WIDTH):
						index = self.WIDTH * y + x

						# loop until you find the empty space to make moves
						if current_board[ index ] == 0:
							moved = False

							while not(moved):
								m = random.randint(0, 3)
								move_x = x + potential_moves[ m ][ 0 ]
								move_y = y + potential_moves[ m ][ 1 ]

								if 0 <= move_x < Board.WIDTH and 0 <= move_y < Board.HEIGHT:
									# make the move
									move_index = self.WIDTH * move_y + move_x

									tmp = current_board[ index ]
									current_board[ index ] = current_board[ move_index ]
									current_board[ move_index ] = tmp

									moved = True

			# copy randomized board to the game board
			length = self.WIDTH * self.HEIGHT
			for i in xrange(0, length):
				self.state[ i ] = current_board[ i ]

	def __getitem__( self, key ):
		return self.state[ key ]

	def __setitem__( self, key, value ):
		self.state[ key ] = value

	def hash( self ):
		return hash(tuple(self.state))


	# Draw a game board state. Step 0 implies no moves have
	# occurred and is our initial board.
	def draw( self, step ):
		tile = lambda x, y: " " if self.state[Board.WIDTH * y + x] == 0 else self.state[Board.WIDTH * y + x]

		if self.state == None or len(self.state) == 0:
			print "self.state is BAD. {}".format( self.state )

		for y in xrange(0, Board.HEIGHT):
			if y == 1:
				if step == 0:
					print ' {0:>10} {1:<3} |{2}|{3}|{4}|'.format( "Initial", "", tile(0, y), tile(1, y), tile(2, y) );
				else:
					print ' {0:>10} {1:<3} |{2}|{3}|{4}|'.format( "Step", step,  tile(0, y), tile(1, y), tile(2, y) );
			else:
					print ' {0:>10} {1:<3} |{2}|{3}|{4}|'.format( "", "",        tile(0, y), tile(1, y), tile(2, y) );
		print ""

	def debug( self ):
		print ' |{0:1d}|{1:1d}|{2:1d}|'.format( self.state[ 0 ],  self.state[ 1 ],  self.state[ 2 ] );
		print ' |{0:1d}|{1:1d}|{2:1d}|'.format( self.state[ 3 ],  self.state[ 4 ],  self.state[ 5 ] );
		print ' |{0:1d}|{1:1d}|{2:1d}|'.format( self.state[ 6 ],  self.state[ 7 ],  self.state[ 8 ] );
		print ""

	# Create a new game board by transposing two titles
	def transpose( self, index, move_index ):
		assert( index != move_index )
		assert( 0 <= index < Board.WIDTH * Board.HEIGHT )
		assert( 0 <= move_index < Board.WIDTH * Board.HEIGHT )
		new_board = Board( self.state )
		tmp = new_board[ index ]
		new_board[ index ] = new_board[ move_index ]
		new_board[ move_index ] = tmp
		assert( isinstance(new_board, Board) )
		return new_board

def find_empty_space( board ):
	for x in xrange(0, Board.WIDTH):
		for y in xrange(0, Board.HEIGHT):
			index = Board.WIDTH * y + x

			# loop until you find the empty space to make moves
			if board[ index ] == 0:
				assert( 0 <= x < Board.WIDTH )
				assert( 0 <= y < Board.HEIGHT )
				return (x, y)
	return None

# Given a game board, what are all of the possible
# game boards that can result from all of the potential
# moves.
def get_possible_moves( current_board, successors_handle ):
	successors = Successors(successors_handle)
	potential_moves = [
		( -1,  0 ),
		(  1,  0 ),
		(  0, -1 ),
		(  0,  1 )
	]
	index = None
	found = False
	empty_space = find_empty_space( current_board )

	for move in potential_moves:
		move_x = empty_space[0] + move[0]
		move_y = empty_space[1] + move[1]

		if 0 <= move_x < Board.WIDTH and 0 <= move_y < Board.HEIGHT:
			move_index = Board.WIDTH * move_y + move_x
			index = Board.WIDTH * empty_space[1] + empty_space[0]
			# make the move
			new_board = current_board.transpose( index, move_index )
			assert( isinstance(new_board, Board) )
			successors.push( new_board )

# The sum of the manhattan distance of each number between
# game boards.
def heuristic( board1, board2 ):
	sum = 0
	for y1 in xrange(0, Board.HEIGHT):
		for x1 in xrange(0, Board.WIDTH):
			index1 = Board.WIDTH * y1 + x1
			for y2 in xrange(0, Board.HEIGHT):
				for x2 in xrange(0, Board.WIDTH):
					index2 = Board.WIDTH * y2 + x2

					if board1[ index1 ] == board2[ index2 ]:
						sum += int( math.fabs( x2 - x1 ) + math.fabs( y2 - y1 ))
	return sum

# The cost of making a move is 1.
def cost( board1, board2 ):
	return 1

# Two game boards are equal if every number is in the same
# position in both.
def board_compare( board1, board2 ):
	for i in xrange(0, Board.WIDTH * Board.HEIGHT):
		if board1[ i ] != board2[ i ]:
			return 1
	return 0

def state_hash(board):
	return board.hash()

def main():
	random.seed( None )

	astar = AStarSearch( board_compare, state_hash, heuristic, cost, get_possible_moves )

	# Produce a solvable random board
	initial_state = Board()
	initial_state.randomize( True )

	if astar.find( Board.goal(), initial_state ):
		step = 0

		for board in astar:
			board.draw( step )
			step += 1

		astar.cleanup( )
	else:
		# No solution found.
		print "No solution found for:\n\n"
		initial_state.draw( 0 );

main()

