import numpy as np
import copy
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

tarimas_data = []

def cargar_txt():
    global tarimas_data
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        try:
            with open(filepath, 'r') as file:
                lines = file.read().splitlines()
                tarimas_data.clear()
                for i in range(0, len(lines), 6):
                    tiempos = [float(lines[i].strip())]
                    tiempos.append(float(lines[i+1].strip()))
                    tiempos.append(float(lines[i+2].strip()) / 60)  # Convertir segundos a minutos
                    tiempos.append(float(lines[i+3].strip()) / 60)  # Convertir segundos a minutos
                    tiempos.append(float(lines[i+4].strip()))
                    tarimas_data.append({"id": len(tarimas_data) + 1, "T": np.array(tiempos)})
            messagebox.showinfo("Éxito", "Datos cargados exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

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

def generar_vecinos(secuencia):
    vecinos = []
    n = len(secuencia)
    for i in range(n):
        for j in range(i + 1, n):
            vecino = copy.deepcopy(secuencia)
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos

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

def graficar_secuencia(secuencia, tiempo_inicio, tiempo_final):
    n = len(secuencia)
    m = len(tiempo_inicio[0])
    colores = plt.cm.tab10.colors

    fig, ax = plt.subplots()

    for i in range(n):
        for j in range(m):
            ax.broken_barh([(tiempo_inicio[i][j], tiempo_final[i][j] - tiempo_inicio[i][j])],
                           (i - 0.4, 0.8), facecolors=colores[j % 10])

    ax.set_yticks(range(n))
    ax.set_yticklabels([f"Tarima {secuencia[i]}" for i in range(n)])
    ax.set_xlabel("Tiempo (minutos)")
    ax.set_title("Flowshop")

    plt.show()

def calcular_secuencia():
    try:
        cant_t1 = int(entry_t1.get())
        cant_t2 = int(entry_t2.get())
        cant_t3 = int(entry_t3.get())
        
        secuencia = [1]*cant_t1 + [2]*cant_t2 + [3]*cant_t3
        mejor_secuencia, mejor_makespan = busqueda_tabu([tarimas_data[s-1] for s in secuencia])

        makespan, tiempo_inicio, tiempo_final = calcular_makespan(mejor_secuencia, [tarimas_data[s-1] for s in secuencia])

        result_text.set(f"Mejor secuencia: {mejor_secuencia}\nMejor makespan: {mejor_makespan:.2f} minutos")

        graficar_secuencia(mejor_secuencia, tiempo_inicio, tiempo_final)
    except ValueError:
        messagebox.showerror("Entrada inválida", "Por favor ingrese números enteros válidos.")

root = tk.Tk()
root.title("Secuencia de Tarimas")

label_t1 = tk.Label(root, text="Cantidad de Tarima 1:")
label_t1.grid(row=0, column=0, padx=10, pady=10)
entry_t1 = tk.Entry(root)
entry_t1.grid(row=0, column=1, padx=10, pady=10)

label_t2 = tk.Label(root, text="Cantidad de Tarima 2:")
label_t2.grid(row=1, column=0, padx=10, pady=10)
entry_t2 = tk.Entry(root)
entry_t2.grid(row=1, column=1, padx=10, pady=10)

label_t3 = tk.Label(root, text="Cantidad de Tarima 3:")
label_t3.grid(row=2, column=0, padx=10, pady=10)
entry_t3 = tk.Entry(root)
entry_t3.grid(row=2, column=1, padx=10, pady=10)

button_cargar = tk.Button(root, text="Cargar Datos desde TXT", command=cargar_txt)
button_cargar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

button_calcular = tk.Button(root, text="Calcular Secuencia", command=calcular_secuencia)
button_calcular.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

result_text = tk.StringVar()
label_result = tk.Label(root, textvariable=result_text, justify=tk.LEFT)
label_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
