"""
	Busqueda de adversarios:
	Aproximacion heuristica:definir una funcion que nos indique lo cerca que estamos de una jugada ganadora
	creamos el arbol de busqueda: evaluar de abajo hacia arriba.
	el algoritmo busca con profundidad limitada, y solo decide la siguiente jugada  partir del nodo raiz.
	 | |   |    |
	|| || || ||
	expandir hasta cierta profundidad,  de acuerdo a la f_utilidad= heuristica
	juego e 3 en raya
	e(funcion de utilidad)  = [numero de filas columnas diagonales disponibles para MAX]  - 
	[numero de filas columnas doagonales completas disponibles para MIN ]
	un puzzle de 15(parcial)

 """
