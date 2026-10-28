class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class RouteList:
    """
    Lista doblemente enlazada para gestionar las paradas de una ruta.
    Permite inserciones y eliminaciones eficientes.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def insert_after(self, target_data, new_data):
        curr = self.head
        while curr:
            if curr.data == target_data:
                new_node = Node(new_data)
                new_node.next = curr.next
                new_node.prev = curr
                if curr.next:
                    curr.next.prev = new_node
                else:
                    self.tail = new_node
                curr.next = new_node
                return True
            curr = curr.next
        return False

    def remove(self, data):
        curr = self.head
        while curr:
            if curr.data == data:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev
                return True
            curr = curr.next
        return False

    def to_list(self, reverse=False):
        res = []
        curr = self.tail if reverse else self.head
        while curr:
            res.append(curr.data)
            curr = curr.prev if reverse else curr.next
        return res
