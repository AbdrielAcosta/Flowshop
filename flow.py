import numpy as np
import copy

# Definir el número de procesos
num_procesos = 5

# Datos para Tarima 1
T1 = np.array([5, 3, 7, 4, 2])
# Datos para Tarima 2
T2 = np.array([6, 4, 6, 5, 3])

# Datos combinados para simplificación
tarimas = [
    {"id": 1, "T": T1},
    {"id": 2, "T": T2}
]

# Función para calcular makespan para una secuencia dada
def calcular_makespan(secuencia, tarimas):
    n = len(secuencia)
    m = num_procesos
    tiempo_inicio = np.zeros((n, m))
    tiempo_final = np.zeros((n, m))

    for i in range(n):
        idx = secuencia[i] - 1
        for j in range(m):
            if i == 0 and j == 0:
                tiempo_inicio[i][j] = 0
            elif i == 0:
                tiempo_inicio[i][j] = tiempo_final[i][j - 1]
            elif j == 0:
                tiempo_inicio[i][j] = tiempo_final[i - 1][j]
            else:
                tiempo_inicio[i][j] = max(tiempo_final[i - 1][j], tiempo_final[i][j - 1])
            tiempo_final[i][j] = tiempo_inicio[i][j] + tarimas[idx]["T"][j]

    return tiempo_final[-1][-1], tiempo_final

# Función para generar vecinos de una solución dada
def generar_vecinos(secuencia):
    vecinos = []
    n = len(secuencia)
    for i in range(n):
        for j in range(i + 1, n):
            vecino = copy.deepcopy(secuencia)
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos

# Algoritmo NEH
def algoritmo_neh(tarimas):
    # Ordenar trabajos en orden decreciente de la suma de sus tiempos de procesamiento
    suma_tiempos = [(tarima["id"], np.sum(tarima["T"])) for tarima in tarimas]
    suma_tiempos.sort(key=lambda x: x[1], reverse=True)
    secuencia_ordenada = [item[0] for item in suma_tiempos]

    # Construir secuencia inicial
    mejor_secuencia = [secuencia_ordenada[0]]
    mejor_makespan, _ = calcular_makespan(mejor_secuencia, tarimas)

    # Iterar sobre el resto de los trabajos
    for i in range(1, len(secuencia_ordenada)):
        mejor_makespan_iter = float('inf')
        mejor_secuencia_iter = None

        # Probar insertar el trabajo en cada posición de la secuencia actual
        for j in range(len(mejor_secuencia) + 1):
            nueva_secuencia = mejor_secuencia[:j] + [secuencia_ordenada[i]] + mejor_secuencia[j:]
            makespan, _ = calcular_makespan(nueva_secuencia, tarimas)
            if makespan < mejor_makespan_iter:
                mejor_makespan_iter = makespan
                mejor_secuencia_iter = nueva_secuencia

        mejor_secuencia = mejor_secuencia_iter
        mejor_makespan = mejor_makespan_iter

    return mejor_secuencia, mejor_makespan

# Función de búsqueda tabú
def busqueda_tabu(tarimas, max_iter=1000):
    # Inicialización de la solución inicial (puede ser con NEH u otra heurística)
    mejor_secuencia, _ = algoritmo_neh(tarimas)
    mejor_makespan, _ = calcular_makespan(mejor_secuencia, tarimas)

    # Inicialización de la lista tabú y otros parámetros
    lista_tabu = []
    iteracion = 0

    while iteracion < max_iter:
        # Generar vecinos de la mejor solución actual
        vecinos = generar_vecinos(mejor_secuencia)

        # Evaluar y seleccionar el mejor vecino no tabú
        mejor_vecino = None
        mejor_makespan_vecino = float('inf')

        for vecino in vecinos:
            if vecino not in lista_tabu:
                makespan_vecino, _ = calcular_makespan(vecino, tarimas)
                if makespan_vecino < mejor_makespan_vecino:
                    mejor_vecino = vecino
                    mejor_makespan_vecino = makespan_vecino

        # Actualizar la mejor solución encontrada
        if mejor_vecino is not None:
            mejor_secuencia = mejor_vecino
            mejor_makespan = mejor_makespan_vecino

        # Actualizar lista tabú y otros parámetros según criterios de actualización tabú

        iteracion += 1

    return mejor_secuencia, mejor_makespan

# Ejecutar la búsqueda tabú
mejor_secuencia, mejor_makespan = busqueda_tabu(tarimas)

# Resultados
print(f"Mejor secuencia encontrada: {mejor_secuencia}")
print(f"Mejor makespan encontrado: {mejor_makespan}")
