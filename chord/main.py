import os
from typing import Dict, List

TOTAL_NODES = 16

DATA = [None] * TOTAL_NODES

for i in range(TOTAL_NODES):
    DATA[i] = f"Vinicius{i}"


class Hasher:
    def hash(value: str) -> int:
        hash_code = 0
        for char in value:
            hash_code = (hash_code * 31 + ord(char)) % TOTAL_NODES
        return hash_code


class Node:
    def __init__(self, key: int = -1):
        self.key: int = key
        self.value: List[str] = []
        self.conjunct: Dict[int, List[str]] = dict()
        self.active: bool = False
        self.next: int = -1


class Chord:
    def __init__(self):
        self.actives: List[int] = [1, 3, 6, 7]
        self.ring: List[Node] = []

    def add_node(self, node: Node):
        self.ring.append(node)

    def add_value(self, v: str):
        hash_key = Hasher.hash(v)
        self.ring[hash_key].value.append(v)
        return hash_key

    def active_node(self, node: int):
        if node >= 0 and node < TOTAL_NODES and node not in self.actives:
            self.actives.append(node)
            self.actives.sort()
            self.ring[node].active = True
            index = self.actives.index(node)
            ## head
            if index == 0:
                tail = self.actives[len(self.actives) - 1]
                self.ring[node].next = self.actives[index + 1]
                self.ring[tail].next = node

                it_node = [*self.ring[tail + 1 : len(self.ring)], *self.ring[: self.ring[node].key + 1]]
                conjunct_node = {}
                for it in it_node:
                    conjunct_node.update({it.key: it.value})

                it_next = self.ring[self.actives[index + 1] : self.ring[node].next + 1]
                conjunct_next = {}
                for it in it_next:
                    conjunct_next.update({it.key: it.value})

                self.ring[node].conjunct = conjunct_node
                self.ring[self.ring[node].next].conjunct = conjunct_next

            # tail
            elif index == len(self.actives) - 1:
                prev = self.actives[index - 1]
                self.ring[node].next = self.ring[prev].next
                self.ring[prev].next = node

                it_node = self.ring[self.actives[index - 1] + 1 : self.ring[node].key + 1]
                conjunct_node = {}
                for it in it_node:
                    conjunct_node.update({it.key: it.value})

                it_next = [*self.ring[self.ring[node].key + 1 : len(self.ring)], *self.ring[: self.ring[node].next + 1]]
                conjunct_next = {}
                for it in it_next:
                    conjunct_next.update({it.key: it.value})

                self.ring[node].conjunct = conjunct_node
                self.ring[self.ring[node].next].conjunct = conjunct_next

            else:
                prev = self.actives[index - 1]
                self.ring[node].next = self.ring[prev].next
                self.ring[prev].next = node

                it_node = self.ring[self.actives[index - 1] + 1 : self.ring[node].key + 1]
                conjunct_node = {}
                for it in it_node:
                    conjunct_node.update({it.key: it.value})

                it_next = self.ring[self.ring[node].key + 1 : self.ring[node].next + 1]
                conjunct_next = {}
                for it in it_next:
                    conjunct_next.update({it.key: it.value})

                self.ring[node].conjunct = conjunct_node
                self.ring[self.ring[node].next].conjunct = conjunct_next
            return 1
        return -1

    def inactive_node(self, node: int):
        if len(self.actives) == 1:
            self.ring[node].active = False
            self.ring[node].value = []
            return 1
        if node >= 0 and node < TOTAL_NODES and node in self.actives:
            index = self.actives.index(node)
            # head
            if index == 0:
                next_node = self.ring[self.ring[node].next]
                next_node.conjunct = {**self.ring[node].conjunct, **next_node.conjunct}
                tail = self.actives[len(self.actives) - 1]
                self.ring[tail].next = next_node.key
            # tail
            elif index == index == len(self.actives) - 1:
                head_node = self.ring[self.actives[0]]
                head_node.conjunct = {**self.ring[node].conjunct, **head_node.conjunct}
                prev = self.ring[self.actives[index - 1]]
                prev.next = self.ring[node].next
            else:
                next_node = self.ring[self.ring[node].next]
                next_node.conjunct = {**self.ring[node].conjunct, **next_node.conjunct}
                prev = self.ring[self.actives[index - 1]]
                prev.next = self.ring[node].next
            self.actives.remove(node)
            self.actives.sort()
            self.ring[node].next = -1
            self.ring[node].active = False
            return 1
        return -1

    def start_nodes(self):
        for ring in self.ring:
            if ring.key in self.actives:
                idx = self.actives.index(ring.key)
                last_active = self.actives[len(self.actives) - 1]
                ring.active = True

                if idx == len(self.actives) - 1:
                    ring.next = self.actives[0]
                else:
                    ring.next = self.actives[idx + 1]

                # é head
                if ring.key == self.actives[0]:
                    conjunct1 = self.ring[last_active + 1 : len(self.ring)]
                    conjunct2 = self.ring[: ring.key + 1]
                    iterable: List[Node] = [*conjunct1, *conjunct2]

                    conjunct = {}

                    for it in iterable:
                        conjunct.update({it.key: it.value})

                    ring.conjunct = conjunct

                else:
                    iterable = self.ring[self.actives[idx - 1] + 1 : ring.key + 1]
                    conjunct = {}
                    for it in iterable:
                        conjunct.update({it.key: it.value})

                    ring.conjunct = conjunct

    def search(self, start_key: int, value: str):
        if start_key not in self.actives:
            return -1

        current_key = start_key
        steps = 0
        while steps < len(self.actives):
            node = self.ring[current_key]
            iterable = sum([node.conjunct[i] for i in node.conjunct], [])
            if value in iterable:
                return current_key
            else:
                current_key = node.next

            steps += 1

        return -1

    def display(self):
        for ring in self.ring:
            if ring.active:
                print(f"key: {ring.key}")
                print(f"next: {ring.key}->{ring.next}")
                print(f"conjunct: {ring.key}->{ring.conjunct}\n")


if __name__ == "__main__":
    chord = Chord()
    message = ""
    while True:
        if message:
            print(message)
        print("1 - Exit")
        print("2 - Cria nova rede")
        print("3 - Display")
        print("4 - Buscar")
        print("5 - Inserir um novo valor")
        print("6 - Ativar nó")
        print("7 - Inativa nó")
        code = int(input("Digite o número o código: "))
        match code:
            case 1:
                exit()
            case 2:
                chord = Chord()
                for i in range(TOTAL_NODES):
                    chord.add_node(Node(i))
                chord.start_nodes()

                for data in DATA:
                    chord.add_value(data)
                message = "Criado com sucesso"
            case 3:
                chord.display()
                message = ""
            case 4:
                start_key = int(input("Digite o nó inicial de busca: "))
                value = str(input("Digite o valor a ser buscado: "))
                node = chord.search(start_key, value)
                if node == -1:
                    message = "Valor não encontrado"
                else:
                    message = f"Valor encontrado no nó {node}"
            case 5:
                value = str(input("Digite o novo valor a ser inserido: "))
                node = chord.add_value(value)
                message = f"Inserido com sucesso no nó {node}"
            case 6:
                value = int(input("Digite o nó que deseja ativar: "))
                result = chord.active_node(value)
                if result == -1:
                    message = f"Esse nó é inválido"
                else:
                    message = f"Nó ativado com  sucesso"
            case 7:
                value = int(input("Digite o nó que deseja inativar: "))
                result = chord.inactive_node(value)
                if result == -1:
                    message = f"Esse nó é inválido"
                else:
                    message = f"Nó inativado com  sucesso"

            case _:
                message = "Opção inválida"
