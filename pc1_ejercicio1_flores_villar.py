#librerias necesarias
class Problem:
	def __init__(self,inicial,final=None):
		self.inicial = inicial
		self.final = final
	def is_goal(self,estado):
		if estado==self.final:
			return estado
	def accciones(self,estado):
		raise NotImplementedError #las acciones para el problema particular
	def resultado(self,estado,accion):
		raise NotImplementedError #los resultados al ejecutar la accion a ese estado
	def costo_accion(self,estado1,accion,estado2):
		return 1

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
			hijo = self.nodo_hijo(problema,acion)
			lista.append(hijo)
		return lista
