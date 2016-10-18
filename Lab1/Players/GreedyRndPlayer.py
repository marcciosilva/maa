# -*- coding:utf-8 -*-

from Player import Player
import random

class GreedyRndPlayer(Player):
	"""Jugador que siempre elige la jugada que más fichas come."""

	name = 'GreedyRnd'	
	def __init__(self, color):
		self.movs = 0
		self.randomMovs=5
		super(GreedyRndPlayer, self).__init__(self.name, color)

	def random_move(self, board):
		possible_moves = board.get_possible_moves(self.color)
		i = random.randint(0, len(possible_moves) - 1)
		return possible_moves[i]
		
	def move(self, board, opponent_move):
		"""
		:param board: Board
		:param opponent_move: Move
		:return: Move
		"""
		
		if (self.movs < self.randomMovs):
			self.movs+=1
			return self.random_move(board)
			
		max_squares = 0
		chosen_move = None
		for move in board.get_possible_moves(self.color):
			tmp = len(board.get_squares_to_mark(move=move, color=self.color))
			if max_squares < tmp:
				chosen_move = move
				max_squares = tmp
		return chosen_move
		
	def on_win(self, board):
		print 'Gané y soy el color:' + self.color.name

	def on_defeat(self, board):
		print 'Perdí y soy el color:' + self.color.name

	def on_draw(self, board):
		print 'Empaté y soy el color:' + self.color.name

	def on_error(self, board):
		raise Exception('Hubo un error.')
