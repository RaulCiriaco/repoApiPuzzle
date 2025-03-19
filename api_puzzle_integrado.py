from flask import Flask, render_template, request
from arbol import Nodo  # Asegúrate de que arbol.py esté en el mismo directorio

app = Flask(__name__)

# Clase Nodo (Se mantiene igual que antes)
class Nodo:
    def __init__(self, datos, hijos=None):
        self.datos = datos
        self.hijos = None
        self.padre = None
        self.costo = None
        self.set_hijos(hijos)

    def set_hijos(self, hijos):
        self.hijos = hijos
        if self.hijos is not None:
            for h in hijos:
                h.padre = self

    def get_hijos(self):
        return self.hijos

    def get_datos(self):
        return self.datos

    def set_datos(self, datos):
        self.datos = datos

    def set_costo(self, costo):
        self.costo = costo

    def get_padre(self):
        return self.padre

    def igual(self, nodo):
        return self.get_datos() == nodo.get_datos()

    def en_lista(self, lista_nodos):
        return any(self.igual(n) for n in lista_nodos)

    def __str__(self):
        return str(self.get_datos())

# Método BFS para el puzzle lineal
def buscar_solucion_BFS_puzzle(estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while (not solucionado) and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
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

# Método DFS Recursivo para el puzzle lineal
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

# Método BFS para vuelos
def buscar_solucion_BFS_vuelos(conexiones, estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while nodos_frontera:
        nodo = nodos_frontera.pop(0)  # Sacar el primer nodo (FIFO)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo 
        
        # Expandir los nodos hijos
        dato_nodo = nodo.get_datos()
        if dato_nodo in conexiones:  
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    hijo.padre = nodo 
                    nodos_frontera.append(hijo)

    return None 

# Ruta principal para el formulario
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        # Obtener datos del formulario
        metodo = request.form["metodo"]
        estado_inicial = request.form["estado_inicial"].strip()
        estado_final = request.form["estado_final"].strip()

        if metodo in ["BFS", "DFS_Rec"]:
            estado_inicial = list(map(int, estado_inicial.split(",")))
            estado_final = list(map(int, estado_final.split(",")))

        conexiones = {
            'CDMX': ['SLP', 'MEXICALI', 'CHIHUAHUA'],
            'SAPOPAN': ['ZACATECAS', 'MEXICALI'],
            'GUADALAJARA': ['CHIAPAS'],
            'CHIAPAS': ['CHIHUAHUA'],
            'MEXICALI': ['SLP', 'SAPOPAN', 'CDMX', 'CHIHUAHUA', 'SONORA'],
            'SLP': ['CDMX', 'MEXICALI'],
            'ZACATECAS': ['SAPOPAN', 'SONORA', 'CHIHUAHUA'],
            'SONORA': ['ZACATECAS', 'MEXICALI'],
            'MICHOACAN': ['CHIHUAHUA'],
            'CHIHUAHUA': ['MICHOACAN', 'ZACATECAS', 'MEXICALI', 'CDMX', 'CHIAPAS'],
        }

        # Resolver según el método elegido
        if metodo == "BFS":
            nodo_solucion = buscar_solucion_BFS_puzzle(estado_inicial, estado_final)
        elif metodo == "DFS_Rec":
            nodo_inicial = Nodo(estado_inicial)
            visitados = []
            nodo_solucion = buscar_solucion_DFS_Recursivo(nodo_inicial, estado_final, visitados)
        elif metodo == "BFS_Vuelos":
            nodo_solucion = buscar_solucion_BFS_vuelos(conexiones, estado_inicial, estado_final)
        else:
            nodo_solucion = None

        # Obtener la solución en forma de lista
        if nodo_solucion:
            resultado = []
            nodo = nodo_solucion
            while nodo is not None:
                resultado.append(nodo.get_datos())
                nodo = nodo.get_padre()
            resultado.reverse()
        else:
            resultado = "No se encontró una solución"

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(port=5000)
