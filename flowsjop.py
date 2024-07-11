import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt

tarimas_data = []

# Función para cargar CSV
def cargar_csv():
    global tarimas_data
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        try:
            df = pd.read_csv(filepath)
            tarimas_data = [
                {"id": int(row["Tarima"]), "T": [row["Filtrado"], row["Selección"], row["Armado 1era"], row["Armado 2da"], row["Empaquetado"]]}
                for index, row in df.iterrows()
            ]
            messagebox.showinfo("Éxito", "CSV cargado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo CSV: {e}")

# Función para calcular el makespan de una secuencia
def calcular_makespan(secuencia, tarimas):
    n = len(secuencia)
    m = len(tarimas[0]["T"])
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

    return tiempo_final[-1][-1], tiempo_inicio, tiempo_final

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

# Algoritmo NEH para solución inicial
def algoritmo_neh(tarimas):
    suma_tiempos = [(tarima["id"], np.sum(tarima["T"])) for tarima in tarimas]
    suma_tiempos.sort(key=lambda x: x[1], reverse=True)
    secuencia_ordenada = [item[0] for item in suma_tiempos]

    mejor_secuencia = [secuencia_ordenada[0]]
    mejor_makespan, _, _ = calcular_makespan(mejor_secuencia, tarimas)

    for i in range(1, len(secuencia_ordenada)):
        mejor_makespan_iter = float('inf')
        mejor_secuencia_iter = None

        for j in range(len(mejor_secuencia) + 1):
            nueva_secuencia = mejor_secuencia[:j] + [secuencia_ordenada[i]] + mejor_secuencia[j:]
            makespan, _, _ = calcular_makespan(nueva_secuencia, tarimas)
            if makespan < mejor_makespan_iter:
                mejor_makespan_iter = makespan
                mejor_secuencia_iter = nueva_secuencia

        mejor_secuencia = mejor_secuencia_iter
        mejor_makespan = mejor_makespan_iter

    return mejor_secuencia, mejor_makespan

# Función de búsqueda tabú
def busqueda_tabu(tarimas, max_iter=100):
    mejor_secuencia, _ = algoritmo_neh(tarimas)
    mejor_makespan, _, _ = calcular_makespan(mejor_secuencia, tarimas)

    lista_tabu = []
    iteracion = 0

    while iteracion < max_iter:
        vecinos = generar_vecinos(mejor_secuencia)

        mejor_vecino = None
        mejor_makespan_vecino = float('inf')

        for vecino in vecinos:
            if vecino not in lista_tabu:
                makespan_vecino, _, _ = calcular_makespan(vecino, tarimas)
                if makespan_vecino < mejor_makespan_vecino:
                    mejor_vecino = vecino
                    mejor_makespan_vecino = makespan_vecino

        if mejor_vecino is not None:
            mejor_secuencia = mejor_vecino
            mejor_makespan = mejor_makespan_vecino

        lista_tabu.append(mejor_secuencia)
        if len(lista_tabu) > 10:
            lista_tabu.pop(0)

        iteracion += 1

    return mejor_secuencia, mejor_makespan

# Función para calcular la secuencia óptima
def calcular_secuencia():
    global tarimas_data
    if not tarimas_data:
        messagebox.showerror("Error", "Por favor, cargue el archivo CSV primero")
        return

    mejor_secuencia, mejor_makespan = busqueda_tabu(tarimas_data)
    resultado_label.config(text=f"Mejor Secuencia: {mejor_secuencia}\nMakespan: {mejor_makespan} minutos")

    # Graficar resultados
    plot_gantt(mejor_secuencia, tarimas_data)

# Función para graficar el diagrama de Gantt
def plot_gantt(secuencia, tarimas):
    _, tiempo_inicio, tiempo_final = calcular_makespan(secuencia, tarimas)
    colors = ["red", "green", "blue", "cyan", "magenta", "yellow", "black", "orange", "purple", "brown"]

    fig, gnt = plt.subplots()
    gnt.set_xlabel('Tiempo')
    gnt.set_ylabel('Tarima')

    gnt.set_yticks([10, 20, 30])
    gnt.set_yticklabels([f'Tarima {secuencia[i]}' for i in range(len(secuencia))])

    for i in range(len(secuencia)):
        for j in range(len(tarimas[0]["T"])):
            gnt.broken_barh([(tiempo_inicio[i][j], tarimas[secuencia[i] - 1]["T"][j])], 
                            (10 * (i+1), 9), facecolors=(colors[j % len(colors)]))

    plt.show()

# Crear interfaz gráfica
root = tk.Tk()
root.title("Optimización Flowshop")
root.geometry("400x300")

cargar_button = tk.Button(root, text="Cargar CSV", command=cargar_csv)
cargar_button.pack(pady=10)

calcular_button = tk.Button(root, text="Calcular Secuencia", command=calcular_secuencia)
calcular_button.pack(pady=10)

resultado_label = tk.Label(root, text="")
resultado_label.pack(pady=10)

root.mainloop()
