from ctypes import *
from ctypes.util import *

lib_file = find_library('csearch')
lib      = CDLL( lib_file )


state_hash_fxn       = CFUNCTYPE( c_size_t, py_object )
compare_fxn          = CFUNCTYPE( c_int, py_object, py_object )
heuristic_fxn        = CFUNCTYPE( c_int, py_object, py_object )
cost_fxn             = CFUNCTYPE( c_int, py_object, py_object )
nonnegative_cost_fxn = CFUNCTYPE( c_uint, py_object, py_object )
successors_fxn       = CFUNCTYPE( None, py_object, c_void_p )

class Successors:
	handle = None

	def __init__( self, handle ):
		self.handle = handle

	def push( self, state ):
		lib.successors_push.restype  = c_bool
		lib.successors_push.argtypes = [c_void_p, py_object]
		return lib.successors_push( self.handle, py_object(state) )

	def pop( self ):
		lib.successors_pop.restype  = c_bool
		lib.successors_pop.argtypes = [c_void_p]
		return lib.successors_pop( self.handle )

	def resize( self, new_size ):
		lib.successors_resize.restype  = c_bool
		lib.successors_resize.argtypes = [c_void_p, c_uint]
		return lib.successors_resize( self.handle, new_size )

	def clear( self ):
		lib.successors_clear.restype  = None
		lib.successors_clear.argtypes = [c_void_p]
		return lib.successors_clear( self.handle )

class AStarSearch:
	handle = None
	node = None
	compare = None
	state_hasher = None
	heuristic = None
	cost = None
	successors_of = None

	def __init__( self, compare, state_hasher, heuristic, cost, successors_of ):
		self.compare       = compare_fxn(compare)
		self.state_hasher  = state_hash_fxn(state_hasher)
		self.heuristic     = heuristic_fxn(heuristic)
		self.cost          = cost_fxn(cost)
		self.successors_of = successors_fxn(successors_of)

		lib.astar_create.restype  = c_void_p
		lib.astar_create.argtypes = [compare_fxn, state_hash_fxn, heuristic_fxn, cost_fxn, successors_fxn]
		self.handle = lib.astar_create( self.compare, self.state_hasher, self.heuristic, self.cost, self.successors_of )

	def __deinit__( self ):
		lib.astar_destroy.restype  = None
		lib.astar_destroy.argtypes = [c_void_p]
		lib.astar_destroy( self.handle )

	def setCompareFunction( self, fxn ):
		self.compare = compare_fxn(fxn)
		lib.astar_set_compare_fxn.restype = None
		lib.astar_set_compare_fxn.argtypes = [c_void_p, compare_fxn]
		lib.astar_set_compare_fxn( self.handle, self.compare )

	def setHeuristicFunction( self, fxn ):
		self.state_hasher = state_hash_fxn(fxn)
		lib.astar_set_heuristic_fxn.restype = None
		lib.astar_set_heuristic_fxn.argtypes = [c_void_p, heuristic_fxn]
		lib.astar_set_heuristic_fxn( self.handle, self.state_hasher )

	def setCostFunction( self, fxn ):
		self.cost = cost_fxn(fxn)
		lib.astar_set_cost_fxn.restype = None
		lib.astar_set_cost_fxn.argtypes = [c_void_p, compare_fxn]
		lib.astar_set_cost_fxn( self.handle, self.cost )

	def setSuccessorsFunction( self, fxn ):
		self.successors_of = successors_fxn(fxn)
		lib.astar_set_successors_fxn.restype = None
		lib.astar_set_successors_fxn.argtypes = [c_void_p, successors_fxn]
		lib.astar_set_successors_fxn( self.handle, self.successors_of )

	def cleanup( self ):
		lib.astar_cleanup.restype  = None
		lib.astar_cleanup.argtypes = [c_void_p]
		lib.astar_cleanup( self.handle )

	def find( self, start, end ):
		lib.astar_find.restype  = c_bool
		lib.astar_find.argtypes = [c_void_p, py_object, py_object]
		return lib.astar_find( self.handle, py_object(start), py_object(end) )

	def firstState( self ):
		lib.astar_first_node.restype  = c_void_p
		lib.astar_first_node.argtypes = [c_void_p]
		self.node = lib.astar_first_node( self.handle )
		state = None
		if self.node != None:
			lib.astar_state.restype  = py_object
			lib.astar_state.argtypes = [c_void_p]
			state = lib.astar_state( self.node )
		return state

	def nextState( self ):
		lib.astar_next_node.restype  = c_void_p
		lib.astar_next_node.argtypes = [c_void_p]
		self.node = lib.astar_next_node( self.node )
		state = None
		if self.node != None:
			lib.astar_state.restype  = py_object
			lib.astar_state.argtypes = [c_void_p]
			state = lib.astar_state( self.node )
		return state

	def iterativeInit( self, start, end, found ):
		lib.astar_iterative_init.restype  = None
		lib.astar_iterative_init.argtypes = [c_void_p, py_object, py_object, py_object]
		return lib.astar_iterative_init( self.handle, py_object(start), py_object(end), py_object(found) )

	def iterativeFind( self, start, end, found ):
		lib.astar_iterative_find.restype  = None
		lib.astar_iterative_find.argtypes = [c_void_p, py_object, py_object, py_object]
		return lib.astar_iterative_find( self.handle, py_object(start), py_object(end), py_object(found) )

	def iterativeIsDone( self, found ):
		lib.astar_iterative_is_done.restype  = c_bool
		lib.astar_iterative_is_done.argtypes = [c_void_p, py_object]
		return lib.astar_iterative_is_done( self.handle, py_object(found) )


