from flask import Flask, render_template, request
from arbol import Nodo  # Importamos la clase Nodo desde arbol.py

app = Flask(__name__)

# Método DFS Recursivo (DFS_rec)
def buscar_solucion_DFS_Recursivo(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())

    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial

    dato_nodo = nodo_inicial.get_datos()
    hijo_izquierdo = Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]])
    hijo_central = Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]])
    hijo_derecho = Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])

    nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

    for nodo_hijo in nodo_inicial.get_hijos():
        if nodo_hijo.get_datos() not in visitados:
            sol = buscar_solucion_DFS_Recursivo(nodo_hijo, solucion, visitados)
            if sol is not None:
                return sol

    return None

# Método BFS estándar (iterativo)
def buscar_solucion_BFS(estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while not solucionado and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)  # FIFO
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo

        dato_nodo = nodo.get_datos()
        movimientos = [(0, 1), (1, 2), (2, 3)]

        for i, j in movimientos:
            hijo = dato_nodo[:]
            hijo[i], hijo[j] = hijo[j], hijo[i]
            nuevo_nodo = Nodo(hijo)
            nuevo_nodo.padre = nodo

            if not nuevo_nodo.en_lista(nodos_visitados) and not nuevo_nodo.en_lista(nodos_frontera):
                nodos_frontera.append(nuevo_nodo)

    return None

# Método DFS (No Recursivo)
def buscar_solucion_DFS(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())

    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial

    dato_nodo = nodo_inicial.get_datos()
    hijo_izquierdo = Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]])
    hijo_central = Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]])
    hijo_derecho = Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])

    nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

    for nodo_hijo in nodo_inicial.get_hijos():
        if nodo_hijo.get_datos() not in visitados:
            sol = buscar_solucion_DFS(nodo_hijo, solucion, visitados)
            if sol is not None:
                return sol

    return None

# Ruta principal para el formulario
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        metodo = request.form["metodo"]
        estado_inicial = list(map(int, request.form["estado_inicial"].strip().split(",")))
        solucion = list(map(int, request.form["estado_final"].strip().split(",")))

        nodo_inicial = Nodo(estado_inicial)
        visitados = []

        if metodo == "DFS_Rec":
            nodo_solucion = buscar_solucion_DFS_Recursivo(nodo_inicial, solucion, visitados)
        elif metodo == "BFS":
            nodo_solucion = buscar_solucion_BFS(estado_inicial, solucion)
        elif metodo == "DFS":
            nodo_solucion = buscar_solucion_DFS(nodo_inicial, solucion, visitados)
        else:
            nodo_solucion = None

        # Obtener la solución si se encuentra
        if nodo_solucion:
            resultado = []
            nodo = nodo_solucion
            while nodo is not None:
                resultado.append(nodo.get_datos())
                nodo = nodo.get_padre()
            resultado.reverse()
        else:
            resultado = "No se encontró solución"

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(port=5000)
