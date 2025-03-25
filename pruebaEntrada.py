#import numpy
"""busqueda binaria
valorEsperado
matrizPorTranspuesta """

def busqueda_binaria(lista,limite_inferior,limite_superior,elemento):
	while (limite_superior-limite_inferior)>1:
		medio =(limite_inferior + limite_superior)//2
		if lista[medio] == elemento:
			return 1
		else:
			if elemento < lista[medio]:
				limite_superior = medio
			else:
				limite_inferior = medio
	return 0

def valor_esperado(costo,probabilidad,premio):
	return probabilidad*premio/100 - costo

def producto_matriz_transpuesta(matriz):
	producto[][]
	for i in range(len(matriz)):
		for j in range(len(matriz[0])):
			producto[i,j] = matriz[i,j]*matriz[j,i]


if __name__=='__main__':
	lista = [1,3,5,7,10,15,25,28,32,40]
	print("busqueda_binaria: ",busqueda_binaria(lista,0,len(lista),26))
	print("valor_esperado: ",valor_esperado(5,10,50))
	print("producto_matriz_transpuesta: ")
	print(producto_matriz_transpuesta())
