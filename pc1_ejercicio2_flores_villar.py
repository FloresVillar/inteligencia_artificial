import sys
from collections import deque;
#librerias necesariasa
class Problema:
	def __init__(self,inicial,final=None):
                self.inicial = inicial
                self.final = final
	def goal_test(self,estado):
        	if isinstance(self.final,list):
                        return is_in(estado,self.final)
        	else:
                        return estado==self.final
	def accciones(self,estado):
        	raise NotImplementedError 	#las acciones para el problema particular
	def resultado(self,estado,accion):
        	raise NotImplementedError 	#los resultados al ejecutar la accion
	def costo_accion(self,c_hasta1,estado1,accion,estado2):
        	return c_hasta1 + 1
	def valor(self,estado):
        	raise NotImplementedError

class Reconfiguracion(Problema):
	def __init__(self,estado_inicial,objetivo_base,capacidades,restricciones):
		super().__init__(estado_inicial)
		self.objetivo_base = objetivo_base #{servicio:servidor}
		self.capacidades = capacidades # {servidor:capacidad}
		self.restricciones = restricciones #[('separados','A','B'),('juntos','C','D')]
	def capacidad_disponible(self,estado,servidor):
		ocupados = 0
		for s in estado.values():
			if s == servidor:
				ocupados+=1
		return self.capacidades[servidor]-ocupados

	def acciones(self,estado): #accion "mover a" = (servicio,servidor_destino)
		acciones = []
		for servicio,servidor_actual in estado.items(): #s=servicio, S=servidor
			for servidor_destino in self.capacidades:
				if servidor_destino != servidor_actual:
					valido = True
					for restriccion in self.restricciones:
						tipo, s1, s2 = restriccion
						if tipo =='no_juntos' and s1==servicio and s2 in estado and estado[s2]==servidor_destino:
							valido = False
						elif tipo=='juntos' and s1 == servicio and s2 in estado and estado[s2] != servidor_destino:
							valido = False
					if valido and self.capacidad_disponible(estado,servidor_destino)>0:
						acciones.append((servicio,servidor_destino))
		return acciones
	def resultado(self,estado,accion): 
		"""	estado = {'A': 'S1', 'B': 'S1', 'C': 'S2'}
			accion = ('A', 'S2'),
			resultado = {'A': 'S2', 'B': 'S1', 'C': 'S2'} """
		servicio, servidor_destino = accion
		nuevo_estado = estado.copy()
		nuevo_estado[servicio] = servidor_destino
		return nuevo_estado
	def conteo_servidor(self,estado,servidor):
		cuenta = 0
		for s in estado.values():
			if s == servidor:
				cuenta+=1
		return cuenta
	def goal_test(self,estado):
		"""	capacidade={'s1':2,'s2':3,'s3':2...}
			objetivo_base={'A':'s1','B':'s2','C':'s3'...} 
			restricciones =[('no_juntos','D','E'),('juntos','F','G')] 
			estado = {'A':'s1','B':'s2','C':'s3','D','s1','E','s2','F':'s3','G','s3'}"""
		for servicio, servidor_destino in self.objetivo_base.items():
			if estado.get(servicio)!=servidor_destino:
				return False
		for restriccion in self.restricciones:
			tipo, s1, s2 = restriccion
			if tipo == 'no juntos':
				if estado[s1] == estado[s2]:
					return False
			elif tipo == 'juntos':
				if estado[s1]!=estado[s2]:
					return False
		for servidor, capacidad in self.capacidades.items():
			if self.conteo_servidor(estado,servidor)>capacidad:
				return False
	def es_valido(self,estado):
		for restriccion in self.restricciones:
			tipo, s1, s2 = restriccion
			if tipo == 'no juntos':
				if estado.get(s1)==estado.get(s2):
					return False
				elif tipo == 'juntos':
					if estado.get(s1)!=estado.get(s2):
						return False
		for servidor, capacidad in self.capacidades.items():
			if self.conteo_servidor(estado,servidor)>capacidad:
				return False
		return self.goal_test(estado)

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
                siguiente_estado = problema.resultado(self.estado,accion)
			    if not problema.es_valido(siguiente_estado):
				    continue
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

def breadth_first_graph_search(problema):
	nodo_inicial =Nodo(problema.inicial)
	if problema.goal_test(nodo_inicial.estado):
		return nodo_inicial
	frontera = deque([nodo_inicial])
	explorados = set()
	while frontera:
		nodo = frontera.popleft()
		print(f"estado: {nodo.estado}")
		explorados.add(frozenset(nodo.estado.items()))
		for hijo in nodo.expandir(problema):
			print(f"hijos: {hijo.estado}")
			if frozenset(hijo.estado.items()) not in explorados and hijo not in frontera:
				if problema.goal_test(hijo.estado):
					return hijo
				frontera.append(hijo)
	return None

if __name__=='__main__':
	estado_inicial = {'A':'s1','B':'s1','C':'s2','D':'s1','E':'s3','F':'s3','G':'s2'}
	objetivo_base = {'A':'s1','B':'s2'}
	capacidades = {'s1':3,'s2':3,'s3':3}
	restricciones = [('no_juntos','D','E'),('juntos','F','G')]
	problema = Reconfiguracion(estado_inicial,objetivo_base,capacidades,restricciones)
	objetivo = breadth_first_graph_search(problema)
	if objetivo:
		print("solucion")
		for accion in objetivo.solucion():
			print(accion)
	else:
		print("no hay solucion") 
