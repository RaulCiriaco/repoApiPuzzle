class Nodo:
    def __init__(self, datos, hijos=None):  # Corregido: `None` sin espacios innecesarios
        self.datos = datos
        self.hijos = None  # Error corregido: Antes se sobrescribía `self.datos` con `None`
        self.padre = None
        self.costo = None
        self.set_hijos(hijos)

    def set_hijos(self, hijos):
        self.hijos = hijos
        if self.hijos is not None:  # Error corregido: `!= None` ahora es `is not None` 
            for h in hijos:
                h.padre = self

    def get_hijos(self):
        return self.hijos  # Error corregido: Antes devolvía `self.padre` en lugar de `self.hijos`

    def get_datos(self):  # Agregado: Método faltante que se usa en `igual()`
        return self.datos

    def set_datos(self, datos):
        self.datos = datos

    def set_costo(self, costo):
        self.costo = costo

    def get_padre(self):  # Agregado: Método necesario para `puzzle.py`
        return self.padre

    def igual(self, nodo):
        if self.get_datos() == nodo.get_datos():  # Antes usaba `self.get_datos()` sin definirlo
            return True
        else:
            return False

    def en_lista(self, lista_nodos):
        en_la_lista = False
        for n in lista_nodos:
            if self.igual(n):
                en_la_lista = True
        return en_la_lista  # Error corregido: Antes retornaba solo `en_la_lista = True`, ahora retorna el valor

    def __str__(self):
        return str(self.get_datos())  # Error corregido: Se usa `get_datos()` ahora definido arriba
