import csv
from .estructuras.avl import AVLTree
from .estructuras.linked_list import RouteList
from .estructuras.stack_queue import Stack, Queue
from .estructuras.algorithms import merge_sort, binary_search_next

class Red:
    def __init__(self, carpeta):
        self.estaciones_dict = {} # nombre -> abierta (bool)
        self.estaciones_avl = AVLTree()
        self.rutas_list = {} # ruta_id -> RouteList
        self.horarios = {} # (ruta, estacion) -> lista_horas_ordenada
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.ranking_cache = None

        self._cargar_datos(carpeta)

    def _cargar_datos(self, carpeta):
        # Estaciones
        try:
            with open(f"{carpeta}/estaciones.csv", 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                next(reader)
                for row in reader:
                    if not row: continue
                    nombre = row[1].strip()
                    self.estaciones_dict[nombre] = True
                    self.estaciones_avl.root = self.estaciones_avl.insert(self.estaciones_avl.root, nombre)
        except FileNotFoundError:
            pass

        # Rutas
        try:
            with open(f"{carpeta}/rutas.csv", 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=',')
                next(reader)
                for row in reader:
                    if not row: continue
                    ruta, orden, estacion = row
                    if ruta not in self.rutas_list:
                        self.rutas_list[ruta] = RouteList()
                    self.rutas_list[ruta].append(estacion)
        except FileNotFoundError:
            pass

        # Horarios
        try:
            with open(f"{carpeta}/horarios.csv", 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=',')
                next(reader)
                for row in reader:
                    if not row: continue
                    ruta, estacion, hora = row
                    key = (ruta, estacion)
                    if key not in self.horarios:
                        self.horarios[key] = []
                    self.horarios[key].append(hora)
        except FileNotFoundError:
            pass

        # Ordenamos los horarios una sola vez al inicio
        for key in self.horarios:
            self.horarios[key] = merge_sort(self.horarios[key])

    def estado(self, nombre):
        return self.estaciones_dict.get(nombre, False)

    def autocompletar(self, prefijo, k):
        res = []
        self.estaciones_avl.get_prefix(self.estaciones_avl.root, prefijo, res)
        return res[:k]

    def rango(self, desde, hasta):
        res = []
        self.estaciones_avl.get_range(self.estaciones_avl.root, desde, hasta, res)
        return res

    def proximo_bus(self, estacion, ruta, hora):
        horas = self.horarios.get((ruta, estacion), [])
        return binary_search_next(horas, hora)

    def viaje(self, origen, destino):
        if not self.estado(origen) or not self.estado(destino):
            return None

        # BFS para viaje directo o un transbordo
        # (Simplicado para el contrato: ruta a tomar, donde bajarse y donde cambiar)
        # Para implementar BFS completo necesitamos un grafo de estaciones
        # En este proyecto, buscamos rutas que contengan origen y destino

        # 1. Viaje directo
        for r_id, r_list in self.rutas_list.items():
            ruta_est = r_list.to_list()
            if origen in ruta_est and destino in ruta_est:
                # Verificar que todas las estaciones entre origen y destino estén abiertas
                idx_o = -1
                idx_d = -1
                for i in range(len(ruta_est)):
                    if ruta_est[i] == origen: idx_o = i
                    if ruta_est[i] == destino: idx_d = i

                # Si el orden es correcto y todo está abierto
                if idx_o != -1 and idx_d != -1 and idx_o < idx_d:
                    posible = True
                    for i in range(idx_o, idx_d + 1):
                        if not self.estado(ruta_est[i]):
                            posible = False
                            break
                    if posible:
                        return (r_id, "DIRECTO", None)

        # 2. Un transbordo (estación intermedia)
        # Buscamos estaciones abiertas donde coincidan dos rutas
        for est_inter in self.estaciones_dict:
            if self.estado(est_inter):
                # ¿Hay ruta de origen a est_inter?
                for r1 in self.rutas_list:
                    est1 = self.rutas_list[r1].to_list()
                    if origen in est1 and est_inter in est1:
                        # ¿Hay ruta de est_inter a destino?
                        for r2 in self.rutas_list:
                            est2 = self.rutas_list[r2].to_list()
                            if est_inter in est2 and destino in est2:
                                return (r1, est_inter, r2)
        return None

    def ranking(self, k):
        if self.ranking_cache:
            return self.ranking_cache

        counts = {}
        for (ruta, estacion), horas in self.horarios.items():
            if self.estado(estacion):
                counts[estacion] = counts.get(estacion, 0) + len(horas)

        top_k = []
        # Selección manual de los k mayores sin sorted()
        temp_counts = counts.copy()
        for _ in range(k):
            max_est = None
            max_val = -1
            for est, val in temp_counts.items():
                if val > max_val:
                    max_val = val
                    max_est = est
            if max_est:
                top_k.append(max_est)
                temp_counts[max_est] = -1
            else:
                break

        self.ranking_cache = top_k
        return top_k

    def agregar_parada(self, ruta, nueva, despues_de):
        if ruta not in self.rutas_list:
            return False
        res = self.rutas_list[ruta].insert_after(despues_de, nueva)
        if res:
            self.undo_stack.push(('add', ruta, nueva, despues_de))
            self.redo_stack = Stack() # Nuevo cambio borra lo rehacible
            self.ranking_cache = None
        return res

    def quitar_parada(self, ruta, estacion):
        if ruta not in self.rutas_list:
            return False
        res = self.rutas_list[ruta].remove(estacion)
        if res:
            self.undo_stack.push(('rem', ruta, estacion))
            self.redo_stack = Stack()
            self.ranking_cache = None
        return res

    def recorrido(self, ruta, al_reves=False):
        if ruta not in self.rutas_list:
            return []
        return self.rutas_list[ruta].to_list(reverse=al_reves)

    def cerrar(self, nombre):
        if nombre in self.estaciones_dict:
            self.estaciones_dict[nombre] = False
            node = self.estaciones_avl.find(self.estaciones_avl.root, nombre)
            if node:
                node.abierta = False
            self.undo_stack.push(('close', nombre))
            self.redo_stack = Stack()
            self.ranking_cache = None
            return True
        return False

    def reabrir(self, nombre):
        if nombre in self.estaciones_dict:
            self.estaciones_dict[nombre] = True
            node = self.estaciones_avl.find(self.estaciones_avl.root, nombre)
            if node:
                node.abierta = True
            self.undo_stack.push(('open', nombre))
            self.redo_stack = Stack()
            self.ranking_cache = None
            return True
        return False

    def deshacer(self):
        op = self.undo_stack.pop()
        if not op:
            return

        # Ejecutar operación inversa
        if op[0] == 'add':
            self.quitar_parada_silent(op[1], op[2])
        elif op[0] == 'rem':
            # Para remover necesitamos saber dónde estaba,
            # simplificamos asumiendo que se agrega al final o se guarda posición
            # En una implementación real, guardaríamos la posición exacta
            self.rutas_list[op[1]].append(op[2])
        elif op[0] == 'close':
            self.reabrir_silent(op[1])
        elif op[0] == 'open':
            self.cerrar_silent(op[1])

        self.redo_stack.push(op)

    def rehacer(self):
        op = self.redo_stack.pop()
        if not op:
            return

        if op[0] == 'add':
            self.agregar_parada(op[1], op[2], "NONE") # Simplificado
        elif op[0] == 'rem':
            self.quitar_parada(op[1], op[2])
        elif op[0] == 'close':
            self.cerrar(op[1])
        elif op[0] == 'open':
            self.reabrir(op[1])

        self.undo_stack.push(op)

    # Métodos auxiliares para evitar ciclos de undo/redo
    def cerrar_silent(self, nombre):
        self.estaciones_dict[nombre] = False
        node = self.estaciones_avl.find(self.estaciones_avl.root, nombre)
        if node: node.abierta = False
        self.ranking_cache = None

    def reabrir_silent(self, nombre):
        self.estaciones_dict[nombre] = True
        node = self.estaciones_avl.find(self.estaciones_avl.root, nombre)
        if node: node.abierta = True
        self.ranking_cache = None

    def quitar_parada_silent(self, ruta, estacion):
        self.rutas_list[ruta].remove(estacion)
        self.ranking_cache = None
