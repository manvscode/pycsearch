from ctypes import *
from ctypes.util import *

libcsearch_file = find_library('csearch')
libcsearch      = CDLL( libcsearch_file )

#typedef void         (*successors_fxn)         ( const void* __restrict state, successors_t* __restrict p_successors )


to_state_hash_fxn       = CFUNCTYPE( c_size_t, c_void_p )
to_compare_fxn          = CFUNCTYPE( c_int, c_void_p, c_void_p )
to_heuristic_fxn        = CFUNCTYPE( c_int, c_void_p, c_void_p )
to_cost_fxn             = CFUNCTYPE( c_int, c_void_p, c_void_p )
to_nonnegative_cost_fxn = CFUNCTYPE( c_uint, c_void_p, c_void_p )
to_successors_fxn       = CFUNCTYPE( None, c_void_p, c_void_p ) 

#print dir( )

def successorsPush( successors, state ):
	return libcsearch.successors_push( successors, byref(state) )

def successorsPop( successors ):
	return libcsearch.successors_pop( successors )

def successorsResize( successors, new_size ):
	return libcsearch.successors_resize( successors, new_size )

def successorsClear( successors ):
	return libcsearch.successors_clear( successors )


class BestFirstSearch:
	bfs = None
	node = None

	def __init__( self, compare_fxn, state_hasher, heuristic, successors_of ):
		self.bfs = libcsearch.bestfs_create( to_compare_fxn(compare_fxn), to_state_hash_fxn(state_hasher), to_heuristic_fxn(heuristic), to_successors_of(successors_of) )

	def __deinit__( self ):
		libcsearch.bestfs_destroy( self.bfs )

	def setCompareFxn( self, compare_fxn ):
		libcsearch.bestfs_set_compare_fxn( self.bfs, to_compare_fxn(compare_fxn) )

	def setHeuristicFxn( self, heuristic_fxn ):
		libcsearch.bestfs_set_heuristic_fxn( self.bfs, to_heuristic_fxn(heuristic_fxn) )

	def setSuccessorsFxn( self, successors_fxn ):
		libcsearch.bestfs_set_successors_fxn( self.bfs, to_successors_fxn(successors_fxn) )

	def cleanup( self ):
		libcsearch.bestfs_cleanup( self.bfs )

	def find( self, start, end ):
		return libcsearch.bestfs_find( self.bfs, byref(start), byref(end) )

	def firstState( self ):
		node = libcsearch.bestfs_first_node( self.bfs )
		return libcsearch.bestfs_state( self.node )

	def nextState( self ):
		node = libcsearch.bestfs_next_node( self.node )
		return libcsearch.bestfs_state( self.node )

	def iterativeInit( self, start, end, found ):
		return libcsearch.bestfs_iterative_init( self.bfs, byref(start), byref(end), byref(found) )	

	def iterativeFind( self, start, end, found ):
		return libcsearch.bestfs_iterative_find( self.bfs, byref(start), byref(end), byref(found) )	

	def iterativeIsDone( self, found ):
		return libcsearch.bestfs_iterative_is_done( self.bfs, byref(found) )

class AStarSearch:
	astar = None
	node = None

	def __init__( self, compare_fxn, state_hasher, heuristic, cost, successors_of ):
		self.astar = libcsearch.astar_create( to_compare_fxn(compare_fxn), to_state_hash_fxn(state_hasher), to_heuristic_fxn(heuristic), to_cost_fxn(cost), to_successors_fxn(successors_of) )

	def __deinit__( self ):
		libcsearch.astar_destroy( self.astar )

	def setCompareFxn( self, compare_fxn ):
		libcsearch.astar_set_compare_fxn( self.astar, to_compare_fxn(compare_fxn) )

	def setHeuristicFxn( self, heuristic_fxn ):
		libcsearch.astar_set_heuristic_fxn( self.astar, to_heuristic_fxn(heuristic_fxn) )

	def setCostFxn( self, cost_fxn ):
		libcsearch.astar_set_cost_fxn( self.astar, to_cost_fxn(cost_fxn) )

	def setSuccessorsFxn( self, successors_fxn ):
		libcsearch.astar_set_successors_fxn( self.astar, to_successors_fxn(successors_fxn) )

	def cleanup( self ):
		libcsearch.astar_cleanup( self.astar )

	def find( self, start, end ):
		return libcsearch.astar_find( self.astar, byref(start), byref(end) )

	def firstState( self ):
		node = libcsearch.astar_first_node( self.astar )
		return libcsearch.astar_state( self.node )

	def nextState( self ):
		node = libcsearch.astar_next_node( self.node )
		return libcsearch.astar_state( self.node )

	def iterativeInit( self, start, end, found ):
		return libcsearch.astar_iterative_init( self.astar, byref(start), byref(end), byref(found) )	

	def iterativeFind( self, start, end, found ):
		return libcsearch.astar_iterative_find( self.astar, byref(start), byref(end), byref(found) )	

	def iterativeIsDone( self, found ):
		return libcsearch.astar_iterative_is_done( self.astar, byref(found) )


