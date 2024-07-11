import numpy as np

# Definir el número de procesos
num_procesos = 5

# Datos para Tarima 1
T1 = np.array([5, 3, 7, 4, 2])
A1 = np.array([2, 1, 3, 2, 1])
B1 = np.array([3, 2, 4, 1, 2])
C1 = np.array([10, 15, 20, 25, 30])

# Datos para Tarima 2
T2 = np.array([6, 4, 6, 5, 3])
A2 = np.array([3, 2, 2, 4, 2])
B2 = np.array([2, 3, 1, 3, 2])
C2 = np.array([15, 20, 25, 30, 35])

# Inicializar variables de tiempo de inicio y finalización
start_time1 = np.zeros(num_procesos)
end_time1 = np.zeros(num_procesos)
total_cost1 = np.zeros(num_procesos)

start_time2 = np.zeros(num_procesos)
end_time2 = np.zeros(num_procesos)
total_cost2 = np.zeros(num_procesos)

# Calcular los tiempos de inicio y finalización, y los costos totales para Tarima 1
for j in range(num_procesos):
    if j == 0:
        start_time1[j] = 0
    else:
        start_time1[j] = end_time1[j-1]
    end_time1[j] = start_time1[j] + T1[j]
    total_cost1[j] = A1[j] + B1[j] + C1[j]

# Calcular los tiempos de inicio y finalización, y los costos totales para Tarima 2
for j in range(num_procesos):
    if j == 0:
        start_time2[j] = 0
    else:
        start_time2[j] = end_time2[j-1]
    end_time2[j] = start_time2[j] + T2[j]
    total_cost2[j] = A2[j] + B2[j] + C2[j]

# Imprimir los tiempos de finalización
print("Tiempos de finalización para Tarima 1:")
print(end_time1)

print("Tiempos de finalización para Tarima 2:")
print(end_time2)

# Imprimir los costos totales
print("Costos totales para Tarima 1:")
print(total_cost1)

print("Costos totales para Tarima 2:")
print(total_cost2)

# Tiempo total de finalización (makespan)
makespan1 = end_time1[-1]
makespan2 = end_time2[-1]
print(f"Tiempo total de finalización para Tarima 1 (makespan): {makespan1}")
print(f"Tiempo total de finalización para Tarima 2 (makespan): {makespan2}")

# Costo total acumulado
total_accumulated_cost1 = np.sum(total_cost1)
total_accumulated_cost2 = np.sum(total_cost2)
print(f"Costo total acumulado para Tarima 1: {total_accumulated_cost1}")
print(f"Costo total acumulado para Tarima 2: {total_accumulated_cost2}")

