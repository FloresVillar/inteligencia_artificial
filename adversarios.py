import numpy as np
import random
import math
from collections import namedtuple, Counter, defaultdict
import functools
cache = functools.lru_cache(10**6)

class Juego:
	def acciones(self,estado):
		raise NotImplementedError
	def resultado(self,estado,accion):
		raise NotImplementedError
	def es_terminal(self,estado):
		return not self.acciones(estado)
	def utilidad(self,estado,jugador):
		raise NotImplementedError
def jugar_juego(juego,estrategias:dict,verbose = False):
	estado = juego.inicial
	while not juego.es_terminal(estado):
		jugador = estado.turno
		movimiento = estrategias[jugador](juego,estado)
		estado = juego.resultado(estado,movimiento)
		if verbose:
			print(f'Jugador {jugador} movimiento:{movimiento}')
			print(estado)
	return estado
infinito = math.inf
def minimax(juego,estado):
	jugador = estado.turno
	def maxx(estado):
		if juego.es_terminal(estado):
			return juego.utilidad(estado,jugador),None
		valor,movimiento = -infinito,None
		for accion in juego.acciones(estado):
			valor2, _ = minx(juego.resultado(estado,accion))
			if valor2 > valor:
				valor, movimiento = valor2,accion
		return valor,movimiento
	def minx(estado):
		if juego.es_terminal(estado):
			return juego.utilidad(estado,jugador),None
		valor, movimiento = infinito,None
		for accion in juego.acciones(estado):
			valor2, _ = maxx(juego.resultado(estado,accion))
			if valor2 < valor:
				valor, movimiento = valor2,accion
		return valor,movimiento

	return maxx(estado)
def poda_alfabeta(juego,estado): #pag188, ejemplo perfecto 
	jugador = estado.turno
	def maxx(estado,alfa,beta):
		if juego.es_terminal(estado):
			return juego.utilidad(estado,jugador),None
		valor, movimiento = -infinito,None
		for accion in juego.acciones(estado):
			valor2, _ = minx(juego.resultado(estado,accion),alfa,beta)
			if valor2 > valor:
				valor,movimiento = valor2, accion
				alfa = max(alfa,valor)
			if valor >=beta:
				return valor,movimiento
		return valor,movimiento
	def minx(estado,alfa,beta):
		if juego.es_terminal(estado):
			return juego.utilidad(estado,jugador),None
		valor,movimiento = infinito,None
		for accion in juego.acciones(estado):
			valor2, _ = maxx(juego.resultado(estado,accion),alfa,beta)
			if valor2 < valor:
				valor, movimiento = valor2,accion
				beta = min(beta,valor)
			if valor<=alfa:
				return valor,movimiento
		return valor,movimiento
	return maxx(estado,-infinito,infinito)
#------juego Tres en raya
class TresEnRaya(Juego):
	def __init__(self,alto=3,ancho=3,k=3):
		self.k = k
		self.coordenadas =set()
		for i in range(ancho):
			for j in range(alto):
				self.coordenadas.add((i,j))
		self.inicial = Tablero(alto = alto,ancho=ancho,turno ='X',utilidad= 0)
	def acciones(self,tablero):
		return self.coordenadas - set(tablero)
	def resultado(self,tablero,coordenada):
		jugador = tablero.turno
		nuevo_tablero = tablero.nuevo({coordenada:jugador},turno=('O' if jugador == 'X' else 'X'))
		result = logro_raya(nuevo_tablero,jugador,coordenada,self.k)
		nuevo_tablero.utilidad = (0 if not result else +1 if jugador =='X' else -1)
		return nuevo_tablero
	def utilidad(self,tablero,jugador):
		return tablero.utilidad if jugador=='X' else -tablero.utilidad
	def es_terminal(self,tablero):
		return tablero.utilidad !=0 or len(self.coordenadas)==len(tablero)
	def mostrar(self,tablero):
		print(tablero)

def logro_raya(tablero,jugador,coordenada,k):
	def raya(x,y,dx,dy):
		if tablero[x,y]!=jugador:
			return 0
		else:
			return 1+raya(x+dx,y+dy,dx,dy)
	for (dx,dy) in ((0,1),(1,0),(1,1),(1,-1)):
		cantidad = raya(*coordenada,dx,dy)+raya(*coordenada,-dx,-dy)-1
		if cantidad>=k:
			return True
	return False
#------------clase Tablero---------------------
class Tablero(defaultdict):
	vacio = '.'
	fuera = '#'
	def __init__(self,ancho=8,alto=8,turno=None,**kwds):
		super().__init__(lambda:Tablero.vacio)
		self.ancho = ancho
		self.alto = alto
		self.turno = turno
		for clave, valor in kwds.items():
			setattr(self,clave,valor)
	def nuevo(self,cambios:dict,**kwds)->'Tablero':
		tablero = Tablero(ancho=self.ancho,alto=self.alto,**kwds)
		tablero.update(self)
		tablero.update(cambios)
		return tablero
	def __missing__(self,loc):
		x,y = loc
		if 0<=x<self.ancho and 0<=y<self.alto:
			return self.vacio
		else:
			return self.fuera
	def __hash__(self):
		return hash(tuple(sorted(self.items())))+hash(self.turno)
	def __repr__(self):
		filas = []
		for y in range(self.alto):
			fila = []
			for x in range(self.ancho):
				celda = self[x,y]
				fila.append(celda)
			fila_str = ' '.join(fila)
			filas.append(fila_str)
		tablero_str = '\n'.join(filas)
		return tablero_str + '\n'
#---------jugador--------
def jugador_aleatorio(juego,estado):
	return random.choice(list(juego.acciones(estado)))
def jugador(algoritmo_busqueda):
	return lambda juego,estado:algoritmo_busqueda(juego,estado)[1]

#--------MAIN------------------------------------
if __name__ =='__main__':
	jugar_juego(TresEnRaya(),dict(X=jugador_aleatorio,O=jugador(poda_alfabeta)),verbose=True).utilidad
