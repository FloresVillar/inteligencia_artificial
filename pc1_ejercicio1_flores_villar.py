import sys
from collections import deque;
from utils import *
#librerias necesariasa
class Problem:
	def __init__(self,inicial,final=None):
		self.inicial = inicial
		self.final = final
	def is_goal(self,estado):
		if isinstance(self.final,list):
			return is_in(estado,self.fin)
		else:
			return estado==self.final
	def accciones(self,estado):
		raise NotImplementedError #las acciones para el problema particular
	def resultado(self,estado,accion):
		raise NotImplementedError #los resultados al ejecutar la accion a ese estado
	def costo_camino(self,c_hasta1,estado1,accion,estado2):
		return c_hasta1 + 1
	def valor(self,estado):
		raise NotImplementedError
class Nodo:
	def __init__(self,estado,padre =None,accion =None,costo_camino =0):
		self.estado = estado
		self.padre = padre
		self.accion = accion
		self.costo_camino = costo_camino
		self.profundidad = 0
		if padre:
			self.profundidad = padre.profundidad + 1
	def __repr__(self):
		return f"<nodo {self.estado}"
	def __lt__(self,nodo):
		return self.estado < nodo.estado
	def expandir(self, problema)
		lista = []
		for accion in problema.acciones(self.estado):
			hijo = self.nodo_hijo(problema,accion)
			lista.append(hijo)
		return lista
	def nodo_hijo(self,problema,accion):
		siguiente_estado = problema.resultado(self.estado,accion):
		siguiente_nodo = Nodo(siguiente_estado,self,accion,problema.costo_camino(self.costo_camino,self.estado,accion,siguiente_estado))
		return siguiente_nodo
	def solucion(self):
		acciones = []
		camino = self.camino()[1:]
		for nodo in camino:
			acciones.append(node.accion)
		return acciones
	def camino():
		nodo, camino_atras = self, []
		while nodo:
			camino_atras.append(nodo)
			nodo = nodo.padre
		return list(reversed(camino_atras))
	def __eq__(self,otro):
		return isinstance() and self.estado == otro.estado
	def __hash__(self):
		
