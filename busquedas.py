import sys
from collections import deque;
import math
import heapq

#clase Problema-------------------------------------------------------------------
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
	def costo_accion(self,costo1,estado1,accion,estado2):
		return costo1+1
	def valor(self,estado):
		raise NotImplementedError
	def h(self,nodo):
		return 0
#Clase Descrifrado----------------------------------------------------------------------------
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
	def aplicar_mapeo(self,estado): #estado => mapeo(asignacion)			#estado = {'J': 'H', 'V': 'O', 'Q': 'A'}
		resultado = ""    #estado = {'J': 'H', 'V': 'O', 'Q': 'A'}
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
		coincidencias = 0
		for i,l in enumerate(texto_descifrado):
			if i<len(fragmento_conocido):
				if l ==self.fragmento_conocido[i]:
					coincidencias+=1
			else:break
		return coincidencias
#clase Nodo----------------------------------------------------------------------------
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
		return self.costo_camino < nodo.costo_camino
	def expandir_0(self, problema):
		lista = []
		for accion in problema.acciones(self.estado):
			hijo = self.nodo_hijo(problema,accion)
			lista.append(hijo)
		return lista
	def expandir(self,problema):
		lista = []
		for accion in problema.acciones(self.estado):
			r = problema.resultado(self.estado,accion)
			hijo = Nodo(r,self,accion,problema.costo_accion(self.costo_camino,self.estado,accion,r))
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
#metodo IDS para dfs limitado----------------
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

falla =Nodo('falla',costo_camino = math.inf)
corte =Nodo('corte',costo_camino =math.inf)
#--------------------------------------------------------------
def bfs_arbol(problema):
	frontera = deque([Nodo(problema.inicial)])
	while frontera:
		nodo = frontera.popleft()
		if problema.is_goal(nodo.estado):
			return nodo
		frontera.extend(nodo.expandir(problema)) #anadir
	return falla
#------------------------------------------------------------
def dfs_arbol(problema):
	frontera = [Nodo(problema.inicial)]
	while frontera:
		nodo =frontera.pop()
		if problema.is_goal(nodo.estado):
			return nodo
		frontera.extend(nodo.expandir(problema))
	return falla
#----------------------------#comentrios si estado es dict---------------------------------
def dfs_grafo(problema):
	frontera = [(Nodo(problema.inicial))]
	visitados = set()
	while frontera:
		nodo = frontera.pop()
		if problema.is_goal(nodo.estado):
			return nodo
		visitados.add(nodo.estado) #visitados.add(frozenset(nodo.estado.items()))
		for hijo in nodo.expandir(problema):
			if hijo.estado not in visitados and hijo not in frontera:
				frontera.append(hijo)
	return falla
#-------------------------------------------------------------
def bfs_grafo(poblema):
	frontera = deque([Nodo(problema.inicial)])
	visitados = set()
	while frontera:
		nodo = frontera.popleft()
		if problema.is_goal(nodo.estado):
			return nodo
		visitados.add(frozenset(nodo.estado.items()))
		for hijo in nodo.expandir(problema):
			if frozenset(hijo.estado.items()) not in visitados and hijo not in frontera:
	 			frontera.append(hijo)
	return falla
#------------------------------------------------------------
def expandir(problema,nodo):
	s = nodo.estado
	for accion in problema.acciones(s):
		r = problema.resultado(s,accion)
		costo =problema.costo_accion(nodo.costo_camino,s,accion,r) #costo = nodo.costo_camino+problema.costo_accion(0,s,accion,r)
		yield Nodo(r,nodo,accion,costo)
#--------------------------------------------------------------
def acciones_camino(nodo):
	if nodo.padre ==None:
		return []
	return acciones_camino(nodo.padre)+[nodo.accion]
#-------------------------------------------------------------
def estados_camino(nodo):
	if nodo in (falla,corte,None):
		return []
	return estados_camino(nodo.padre)+[nodo.estado]

FIFOQueue = deque
LIFOQueu = list

#Clase ColaPrioridad-----------------------------------------------------------------
class ColaPrioridad:
	def __init__(self,items=(),prioridad=lambda x:x):
		self.items =[]
		self.prioridad = prioridad
		for item in items:
			self.agregar(item)
	def agregar(self,item):
		par = (self.prioridad(item),item)
		heapq.heappush(self.items,par)
	def quitar(self):
		return heapq.heappop(self.items)[1] #devuelve una tupla (prioridad,item)
	def cima(self):
		return self.items[0][1]
	def __len__(self):
		return len(self.items)

#--------------------------------------------------------
def primero_mejor(problema, f):
	nodo = Nodo(problema.inicial)
	frontera = ColaPrioridad([nodo],f)
	#visitados = {frozenset(problema.inicial.items()):nodo} #{estado:nodo}, visitados[estado].costo_camino
	visitados = {problema.inicial:nodo}
	while frontera:
		nodo = frontera.quitar()
		if nodo.estado == problema.final:
			return nodo
		for hijo in expandir(problema,nodo):
			s = hijo.estado
			#s_clave = frozenset(s.items())
			if s not in visitados or hijo.costo_camino<visitados[s].costo_camino:
				frontera.agregar(hijo)
				visitados[s] = hijo
	return falla
#-----------------------------------------------------------
def es_ciclo(nodo):
	ac = nodo.padre
	while ac is not None:
		if ac.estado == nodo.estado:
			return True
		ac = ac.padre
	return False
#------------------------------------------------------------
def primero_mejor_arbol(problema,f):
	frontera = ColaPrioridad(problema.inicial,f)
	while frontera:
		nodo = frontera.extraer()
		if problema.is_goal(nodo):
			return nodo
		for hijo in expandir(problema,nodo):
			if not es_ciclo(hijo):
				frontera.agregar(nodo)
	return falla
#-----------------------------------------------------------
def g(nodo):
	return nodo.costo_camino
#-----------------------------------------------------------
def a_estrella(problema,h=None):
	h = h or problema.h
	return primero_mejor(problema,f=lambda nodo:g(nodo)+h(nodo))
#------------------------------------------------------------
def a_estrella_arbol(problema):
	h = h or problema.h
	return primero_mejor_arbol(problema, f=lambda nodo:g(nodo)+h(nodo))
#----------------------------------------------------------
def costo_uniforme(problema):
	return primero_mejor(problema,f = g)
#-----------------------------------#los comentarios si los estdos son dict---------------------------
def bfs_aima(problema):
	nodo = Nodo(problema.inicial)
	if problema.is_goal(nodo.estado):
		return nodo
	frontera = FIFOQueue([nodo])
	visitados = {problema.inicial} #visitados = {frozenset(problema.inicial.items())}
	while frontera:
		nodo = frontera.popleft()
		if  problema.is_goal(nodo.estado):
			return nodo
		for hijo in expandir(problema,nodo):
			s = hijo.estado
			s_clave = s #s_clave = frozenset(s.items())
			if problema.is_goal(s):
				return hijo
			if s_clave not in visitados:
				visitados.add(s_clave)
				frontera.append(hijo)
	return falla
#clase OchoPuzzles----------------------------------------------------------------
class OchoPuzzles(Problema):
	def __init__(self,inicial,final=(1,2,3,4,5,6,7,8,0)):
		self.inicial = inicial 
		self.final = final
	def is_goal(self,estado):
		if estado ==self.final:
			return True
		return False
	def posicion_vacio(self,estado):
		return estado.index(0)
	def acciones(self,estado):
		acciones_base =['ARRIBA','ABAJO','DERECHA','IZQUIERDA']
		p_vacio = self.posicion_vacio(estado)
		if p_vacio%3 == 0:
			acciones_base.remove('IZQUIERDA')
		if p_vacio < 3:
			acciones_base.remove('ARRIBA')
		if p_vacio%3 ==2:
			acciones_base.remove('DERECHA')
		if p_vacio > 5:
			acciones_base.remove('ABAJO')
		return acciones_base
	def resultado(self,estado,accion):
		nuevo_estado = list(estado)
		r = {'ARRIBA':-3,'ABAJO':+3,'IZQUIERDA':-1,'DERECHA':+1}
		p_vacio = self.posicion_vacio(estado)
		p = p_vacio + r[accion]
		print(f'p_vacio:{p_vacio}, r[accion]:{r[accion]} , p : {p}')
		aux = nuevo_estado[p_vacio]
		nuevo_estado[p_vacio]= nuevo_estado[p]
		nuevo_estado[p] = aux
		return tuple(nuevo_estado)
	def es_soluble(self,estado):
		intercambios = 0
		for i in range		(len(estado)):
			for j in range(i+1,len(estado)):
				if (estado[i] > estado[j]) and estado[i]!=0 and estado[j]!=0:
					intercambios +=1
		return intercambios%2==0
	def h_0(self,nodo): #h posicion fuera de posicion en final
		cuenta = 0
		estado = nodo.estado
		for i in range(len(estado)):
			if estado[i]!=self.final[i]:
				cuenta +=1
		return cuenta
	def h(self,nodo): #manhattan
		estado = nodo.estado
		distancia = 0
		for e in range(1,9):
			ind_e = estado.index(e)
			fila_e = ind_e//3
			col_e = ind_e%3
			ind_f = self.final.index(e)
			fila_f = ind_f//3
			col_f = ind_f%3
			distancia += abs(fila_f -fila_e) + abs(col_f-col_e)
		return distancia
	def valor(self,nodo):
		return -self.h(nodo)
#Clase panqueques--------------------------------------------------------------------
class Panqueques(Problema):
	def __init__(self,inicial):
		self.inicial = tuple(inicial)
		self.final = tuple(sorted(inicial))
	def acciones(self,estado):
		n_volteo = range(2,len(estado)+1)
		return n_volteo
	def resultado(self,estado,accion):
		n = accion
		tmp_estado = estado[0:n]
		tmp_estado = tuple(reversed(tmp_estado))
		nuevo_estado = tmp_estado + estado[n:]
		return nuevo_estado
	def h(self,nodo):
		cuenta = 0
		estado = nodo.estado
		for i in range(1,len(estado)):
			if (estado[i-1] - estado[i])> 1:
				cuenta=+1
		return cuenta
import random
#clase laberinto------------------------------------------------------
class Laberinto(Problema):
	def __init__(self,inicial,final,m,n):
		self.inicial = inicial
		self.final = final
		self.m = m
		self.n = n
		self.mapa = [[random.randint(0,1) for _ in range(n)]for _ in range(m)]
		self.mapa[inicial[0]][inicial[1]] =0
		self.mapa[final[0]][final[1]] = 0
		for i in range(self.m):
			for j in range(self.n):
				if self.mapa[i][j] == 1:
					print('*',end=' ')
				else:
					print(' ',end=' ')
			print('\n')
		print('\n')
	def acciones(self,estado):
		acciones_base = ['ARRIBA','ABAJO','DERECHA','IZQUIERDA']
		fila,columna = estado  #estado es una [fila,columna]
		mapa = self.mapa
		m = self.m
		n = self.n
		if fila==0 or mapa[fila-1][columna]==1:
			acciones_base.remove('ARRIBA')
		if fila==m-1 or mapa[fila+1][columna]==1:
			acciones_base.remove('ABAJO')
		if columna==0 or mapa[fila][columna-1]==1:
			acciones_base.remove('IZQUIERDA')
		if columna==n-1 or mapa[fila][columna+1]==1:
			acciones_base.remove('DERECHA')
		return acciones_base
	def resultado(self,estado,accion):
		nuevo_estado = ()
		match accion:
			case 'ARRIBA':nuevo_estado = estado[0]-1,estado[1]
			case 'ABAJO':nuevo_estado = estado[0]+1,estado[1]
			case 'DERECHA':nuevo_estado =estado[0],estado[1]+1
			case 'IZQUIERDA':nuevo_estado = estado[0],estado[1]-1;
		return nuevo_estado
	def h(self,nodo): #manhatan
		estado = nodo.estado
		distancia = abs(self.final[0]-estado[0])+abs(self.final[1]-estado[1])
		return distancia
	def is_goal(self,estado):
		return estado == self.final
#-----clase mapa--------------------------------------------------------------------
from collections import defaultdict
class Mapa:
	def __init__(self,conexiones,localizaciones,dirigido =False):
		if not dirigido:
			copia = dict(conexiones)
			for (c1,c2),distancia in conexiones.items():
				copia[(c2,c1)] = distancia	
		conexiones = copia
		self.conexiones = conexiones
		self.vecinos = defaultdict(list)
		for (c1,c2) in self.conexiones:
			self.vecinos[c1].append(c2)
		self.localizaciones = localizaciones or defaultdict(lambda:(0,0))
#----clase ProblemaMapa--------------------------------------------------------------
class ProblemaMapa(Problema):
	def __init__(self,inicial,final,mapa=None):
		self.inicial = inicial
		self.final = final
		self.mapa = mapa or Mapa()
	def acciones(self,estado):
		return self.mapa.vecinos[estado] # {estado: ['B','C','etc']}
	def resultado(self,estado,accion):
		if accion in self.mapa.vecinos[estado]:
			return accion
		else:
			return estado
	def costo_accion(self,costo1,estado1,accion,estado2):
		return costo1 + self.mapa.conexiones[estado1,estado2] #{(a,b):123}
	def h(self,nodo):
		locs = self.mapa.localizaciones
		A = locs[nodo.estado]
		B = locs[self.final]
		distancia = (A[0]-B[0])**2 + (A[1]-B[1])**2
		return distancia**.5

#-----------------------------------------------------------------------
def hill_climbing(problema):
	nodo = Nodo(problema.inicial)
	if problema.is_goal(nodo.estado):
		return nodo
	actual_val = problema.h(nodo)
	while True:
		vecinos = nodo.expandir(problema)
		if not vecinos:
			break
		mejor_vec = vecinos[0]
		mejor_val = problema.h(mejor_vec)
		for vec in vecinos[1:]:
			val = problema.h(vec)
			if val < mejor_val:
				mejor_vec = vec
				mejor_val = val
		if mejor_val >= actual_val:
			break
		else:
			nodo = mejor_vec
			actual_val = mejor_val
	return nodo
#-------------------------------------------------
def hill_climbing_aima(problema):
	actual = Nodo(problema.inicial)
	while True:
		vecinos = actual.expandir(problema)
		if not vecinos:
			break
		vecino = vecmax_random_tie(vecinos,key =lambda nodo:-problema.h(nodo))
		if problema.h(vecino) >= problema.h(actual):
			break
		actual = vecino
	return actual
def vecmax_random_tie(vecinos,key=None):
	nodo = max(vecinos,key = key)
	mejor = [item for item in vecinos if key(item)==key(nodo)]
	return random.choice(mejor)


#-----------------------------------------------
import numpy as np
def enfriamiento_simulado(problema, estrategia):
	nodo = Nodo(problema.inicial)
	for t in range(sys.maxsize):
		T = estrategia(t)
		if T==0:
			return nodo
		vecinos = nodo.expandir(problema)
		if not vecinos:
			return nodo
		vec = random.choice(vecinos)
		delta = problema.valor(vec)-problema.valor(nodo)
		if delta > 0 or random.random() < np.exp(delta/T):
			nodo = vec

def estrategia(k=20,lam = 0.05,lim = 100):
	return lambda t:(k*np.exp(-lam*t) if  t<lim else 0)
#MAIN
#----
if __name__=='__main__':
	#hill_climbing
	
	problema = OchoPuzzles((5,7,0,1,4,3,8,2,6),(1,2,3,4,5,6,7,8,0))
	if problema.es_soluble(problema.inicial):
                resultado = enfriamiento_simulado(problema,estrategia())
	if resultado!=falla:
				print(problema.final)
				print(problema.inicial)
				print(resultado.estado)
	
	#problema mapa
	"""
	romania = Mapa({('O', 'Z'):  71, ('O', 'S'): 151, ('A', 'Z'): 75, ('A', 'S'): 140, ('A', 'T'): 118,('L', 'T'): 111, ('L', 'M'):  70, ('D', 'M'): 75, ('C', 'D'): 120, ('C', 'R'): 146,('C', 'P'): 138, ('R', 'S'):  80, ('F', 'S'): 99, ('B', 'F'): 211, ('B', 'P'): 101,('B', 'G'):  90, ('B', 'U'):  85, ('H', 'U'): 98, ('E', 'H'):  86, ('U', 'V'): 142,('I', 'V'):  92, ('I', 'N'):  87, ('P', 'R'): 97},{'A': ( 76, 497), 'B': (400, 327), 'C': (246, 285), 'D': (160, 296), 'E': (558, 294),'F': (285, 460), 'G': (368, 257), 'H': (548, 355), 'I': (488, 535), 'L': (162, 379),'M': (160, 343), 'N': (407, 561), 'O': (117, 580), 'P': (311, 372), 'R': (227, 412),'S': (187, 463), 'T': ( 83, 414), 'U': (471, 363), 'V': (535, 473), 'Z': (92, 539)})
	problema  = ProblemaMapa('A','B',mapa=romania)
	resultado = a_estrella(problema)
	print(resultado)
	print(resultado.solucion())"""
	#Laberinto
	"""
	problema = Laberinto((0,0),(0,5),6,6)
	resultado = a_estrella(problema)
	print(resultado)
	print(resultado.solucion())"""
	#panqueques
	"""problema = Panqueques((1, 3, 5, 7, 9, 2, 4, 6, 8))
	print(problema.inicial)
	resultado = a_estrella(problema)
	print(resultado)"""
	#ochopuzzles
	"""
	problema = OchoPuzzles((5,7,0,1,4,3,8,2,6),(1,2,3,4,5,6,7,8,0))
	if problema.es_soluble(problema.inicial):
		resultado = a_estrella(problema)
	if resultado!=falla:
		print(problema.inicial)
		print(resultado.estado) """
	#sustitucion monoalfabetica
	"""texto_cifrado= "XMZV"
	fragmento_conocido = "HOLA"
	diccionario= ["DOLAR","MIA","TOLUCA","CIFRA"]
	problema = Descifrado(texto_cifrado=texto_cifrado,fragmento_conocido=fragmento_conocido,diccionario=diccionario,inicial = {})
	def f(nodo):
		return -problema.valor(nodo.estado)
	solucion = bfs_aima(problema)
	if solucion:
		print("solucion:")
		print("texto descifrado:",problema.aplicar_mapeo(solucion.estado))
		print("camino de acciones",solucion.solucion())
	else:
		print("no hay solucion") """
