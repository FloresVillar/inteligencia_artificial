import sys
from collections import deque;

#librerias necesariasa
class Problema:
	def __init__(self,inicial,final=None):
		self.inicial = inicial
		self.final = final
	def is_goal(self,estado):
		if isinstance(self.final,list):
			return is_in(estado,self.final)
		else:
			return estado==self.final
	def accciones(self,estado):
		raise NotImplementedError #las acciones para el problema particular
	def resultado(self,estado,accion):
		raise NotImplementedError #los resultados al ejecutar la accion a ese estado
	def costo_accion(self,c_hasta1,estado1,accion,estado2):
		return c_hasta1 + 1
	def valor(self,estado):
		raise NotImplementedError

class Descifrado(Problema):
	def __init__(self,texto_cifrado,fragmento_conocido,diccionario,inicial = None):
		super().__init__(inicial)
		self.texto_cifrado = texto_cifrado #Jvsq, Mti, Xlmz.
		self.fragmento_conocido = fragmento_conocido # 'hola' aparece en el texto
		self.diccionario = diccionario #['Hola', 'Mundo', 'Cifrado', 'Texto']
	def is_goal(self,estado):
		texto_descifrado = self.aplicar_mapeo(estado)
		if self.fragmento_conocido in texto_descifrado:
			return True
		return False
	def aplicar_mapeo(self,estado): #estado => mapeo(asignacion)estado = {'J': 'H', 'V': 'O', 'Q': 'A'}
		resultado = ""
		for l in self.texto_cifrado:
			if l in estado:
				resultado+=estado[l]
			else:
				resultado+="_"
		return resultado
	def acciones(self,estado):
		alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		letras_asignadas = set(estado.values())
		letras_no_asignadas = set(alfabeto) - letras_asignadas
		acciones = []
		for l_cifrada in set(self.texto_cifrado)-set(estado.keys()):
			for l_plana in letras_no_asignadas:
				acciones.append((l_cifrada,l_plana))
		return acciones
	def resultado(self,estado,accion):
		nuevo_estado = estado.copy()
		l_cifrada, l_plana = accion
		nuevo_estado [l_cifrada] = l_plana
		return nuevo_estado
	def valor(self,estado):
		texto_descifrado = self.aplicar_mapeo(estado)
		concidencias = 0
		for i,l in enumerate(texto_descifrado):
			if l ==self.fragmento_conocido[i]:
				coincidencias+=1
		return coincidencias
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
	def expandir(self, problema):
		lista = []
		for accion in problema.acciones(self.estado):
			hijo = self.nodo_hijo(problema,accion)
			lista.append(hijo)
		return lista
	def nodo_hijo(self,problema,accion):
		siguiente_estado = problema.resultado(self.estado,accion)
		siguiente_nodo = Nodo(siguiente_estado,self,accion,problema.costo_accion(self.costo_camino,self.estado,accion,siguiente_estado))
		return siguiente_nodo
	def solucion(self):
		acciones = []
		camino = self.camino()[1:]
		for nodo in camino:
			acciones.append(nodo.accion)
		return acciones
	def camino(self):
		nodo, camino_atras = self, []
		while nodo:
			camino_atras.append(nodo)
			nodo = nodo.padre
		return list(reversed(camino_atras))
	def __eq__(self,otro):
		return isinstance(otro,Nodo) and self.estado == otro.estado
	def __hash__(self):
		return hash(self.estado) #n1=Nodo("A") n2=Nodo("A") conjunto=set() conjunto.add(n1) n2 in conjunto ===> true

def IDS(problema):
	limite = 0
	while True:
		resultado = busqueda_profundidad_limitada(Nodo(problema.inicial),problema,limite)
		if resultado is not None:
			return resultado
		limite+=1

def busqueda_profundidad_limitada(nodo,problema,limite):
	if problema.is_goal(nodo.estado):
		return nodo
	elif nodo.profundidad == limite:
		return None
	else:
		for hijo in nodo.expandir(problema):
			resultado = busqueda_profundidad_limitada(hijo,problema,limite)
			if resultado is not None:
				return resultado
	return None

def bfs_arbol(problema):
	frontera = deque([Nodo(problema.inicial)])
	while frontera:
		nodo = frontera.popleft()
		if problema.is_goal(nodo.estado):
			return nodo
		frontera.extend(nodo.expandir(problema)) #anadir
	return None

def dfs_arbol(problema):
	frontera = [Nodo(problema.inicial)]
	while frontera:
		nodo =frontera.pop()
		if problema.is_goal(nodo.estado):
			return nodo
		frontera.extend(nodo.expandir(problema))
	return None

def dfs_grafo(problema):
	frontera = [(Nodo(problema.inicial))]
	visitados = set()
	while frontera:
		nodo = frontera.pop()
		if problema.is_goal(nodo.estado):
			return nodo
		visitados.add(frozenset(nodo.estado.items()))
		for hijo in nodo.expandir(problema):
			if frozenset(hijo.estado.items()) not in visitados and hijo not in frontera:
				frontera.extend([hijo])
	return None

def bfs_grafo(poblema):
	frontera = deque([Nodo(problema.inicial)])
	visitados = set()
	while frontera:
		nodo = frontera.popleft()
		if problema.is_goal(nodo.estado):
			return nodo
		visitados.add(nodo.estado)
		for hijo in nodo.expandir(problema):
			if hijo.estado not in visitados and hijo not in frontera:
				frontera.extend(hijo)


if __name__=='__main__':
	texto_cifrado= "XLMZ"
	fragmento_conocido = "HOLA"
	diccionario= ["DOLAR","MIA","TOLUCA","CIFRA"]
	problema = Descifrado(texto_cifrado=texto_cifrado,fragmento_conocido=fragmento_conocido,diccionario=diccionario,inicial = {})
	solucion = dfs_grafo(problema)
	if solucion:
		print("solucion:")
		print("texto descifrado:",problema.aplicar_mapeo(solucion.estado))
		print("camino de acciones",solucion.solucion())
	else:
		print("no hay solucion")
