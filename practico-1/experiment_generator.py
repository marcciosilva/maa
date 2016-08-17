import random
import math
#B for black
#W for white
#O for empty

'''
La idea de este modulo es ofrecer un tablero inicial nuevo.
'''

def getNewBoard():
	# 	#tablero inicial
	board = [
	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	    ["W", "O", "W", "O", "W", "O", "W", "O"],
	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	    ["B", "O", "B", "O", "B", "O", "B", "O"],
	    ["O", "B", "O", "B", "O", "B", "O", "B"],
	    ["B", "O", "B", "O", "B", "O", "B", "O"]
	    ]


	# amountOfBoards = 4
	# boardChoice = math.floor(random.random() * amountOfBoards)
	# if (boardChoice == 0):
	# 	#tablero inicial
	# 	board = [
	# 	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	# 	    ["W", "O", "W", "O", "W", "O", "W", "O"],
	# 	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["B", "O", "B", "O", "B", "O", "B", "O"],
	# 	    ["O", "B", "O", "B", "O", "B", "O", "B"],
	# 	    ["B", "O", "B", "O", "B", "O", "B", "O"]
	# 	    ]
	# elif (boardChoice == 1):
	# 	#comida doble
	# 	board = [
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "W", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "W", "O", "W", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "W", "O", "O", "O"],
	# 	    ["O", "O", "O", "B", "O", "O", "O", "O"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"]
	# 	    ]
	# elif (boardChoice == 2):
	# 	#tablero en donde las negras pueden comer una blanca
	# 	board = [
	# 	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	# 	    ["W", "O", "W", "O", "W", "O", "W", "O"],
	# 	    ["O", "W", "O", "O", "O", "O", "O", "W"],
	# 	    ["O", "O", "O", "O", "W", "O", "W", "O"],
	# 	    ["O", "B", "O", "B", "O", "O", "O", "O"],
	# 	    ["O", "O", "B", "O", "O", "O", "B", "O"],
	# 	    ["O", "B", "O", "B", "O", "B", "O", "B"],
	# 	    ["B", "O", "B", "O", "B", "O", "B", "O"]
	# 	    ]
	# elif (boardChoice == 3):
	# 	board = [
	# 	    ["O", "W", "O", "W", "O", "W", "O", "W"],
	# 	    ["W", "O", "W", "O", "W", "O", "W", "O"],
	# 	    ["O", "W", "O", "O", "O", "W", "O", "W"],
	# 	    ["O", "O", "O", "O", "O", "O", "O", "O"],
	# 	    ["O", "B", "O", "B", "O", "O", "O", "O"],
	# 	    ["O", "O", "B", "O", "O", "O", "W", "O"],
	# 	    ["O", "B", "O", "B", "O", "B", "O", "B"],
	# 	    ["B", "O", "B", "O", "B", "O", "B", "O"]
	# 	    ]	    
	return board

#juego corto
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],    
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "B", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "W", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]	

#tablero inicial
# board = [
#     ["O", "W", "O", "W", "O", "W", "O", "W"],
#     ["W", "O", "W", "O", "W", "O", "W", "O"],
#     ["O", "W", "O", "W", "O", "W", "O", "W"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["B", "O", "B", "O", "B", "O", "B", "O"],
#     ["O", "B", "O", "B", "O", "B", "O", "B"],
#     ["B", "O", "B", "O", "B", "O", "B", "O"]
#     ]



#tablero en donde las negras pueden comer una blanca
# board = [
#     ["O", "W", "O", "W", "O", "W", "O", "W"],
#     ["W", "O", "W", "O", "W", "O", "W", "O"],
#     ["O", "W", "O", "O", "O", "O", "O", "W"],
#     ["O", "O", "O", "O", "W", "O", "W", "O"],
#     ["O", "B", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "B", "O", "O", "O", "B", "O"],
#     ["O", "B", "O", "B", "O", "B", "O", "B"],
#     ["B", "O", "B", "O", "B", "O", "B", "O"]
#     ]

#comida simple
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]

#comida doble
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "W", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "W", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]

#white action
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]

#white double
# board = [
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "W", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "B", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"],
#     ["O", "O", "O", "B", "O", "O", "O", "O"],
#     ["O", "O", "O", "O", "O", "O", "O", "O"]
#     ]