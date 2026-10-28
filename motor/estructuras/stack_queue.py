class Stack:
    """Pila implementada sobre una lista para deshacer/rehacer."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            return None
        return self.items.pop()

    def peek(self):
        return self.items[-1] if self.items else None

    def is_empty(self):
        return len(self.items) == 0

class Queue:
    """Cola implementada para BFS y simulación."""
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.items:
            return None
        # En BFS el volumen es manejable, usamos pop(0).
        # En simular_fila usaremos punteros para evitar O(n).
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0
