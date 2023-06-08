

class TrieTree:
    def __init__(self, char: str = '', is_last_char: bool = False) -> None:
        self.char = char
        self.is_last_char = is_last_char 
        self.nodes = [] 
        # value: any
    
    def __setitem__(self, key, value):
        self.insert(key, value)

    def __getitem__(self, item: str):
        return self.retrieve(item)

    def __contains__(self, char):
        return any(char == node.char for node in self.nodes)

    def __str__(self) -> str:
        return f"({self.char}{'*' if self.is_last_char else ''} [{len(self.nodes)}])"

    @property
    def is_empty(self) -> bool:
        return not bool(self.nodes)

    def _get_char(self, char: str) -> "TrieTree|None":
        return next(
            (node for node in self.nodes if char == node.char),
            None
        )

    def _recursive_delete(self, sub_key: str) -> bool:
        if sub_key == "":
            # self.value = None
            self.is_last_char = False
            print(f"Node {self} deixou de ser fim de palavra")

        elif next_node := self._get_char(sub_key[0]):
            if next_node._recursive_delete(sub_key[1:]) and not next_node.is_last_char:
                # remove node from list and delete
                self.nodes.remove(next_node)
                print(f"Node {next_node} deletado")
        else:
            raise ValueError(f"sequência '{sub_key}' não encontrada")
        return self.is_empty or self.is_last_char

    def insert(self, key: str, value: any):
        current = self
        for char in key:
            if (node := current._get_char(char)) is None:
                node = TrieTree(char)
                current.nodes.append(node)
                print(f'Node {node} adicionado')
            current = node
        node.is_last_char = True
        # current.value = value

    def retrieve(self, key: str) -> any:
        try:
            current = self
            chain = ''
            for char in key:
                if (node := current._get_char(char)) is None:
                    raise ValueError(f"palvavra {key} não encontrada")
                chain += f'{current}->'
                current = node
        except ValueError as e:
            print(chain, e)
        else:
            print(current.is_last_char)
            # return current.value

    def delete(self, key):
        try:
            if current := self._get_char(key[0]):
                if current._recursive_delete(key[1:]):
                    self.nodes.remove(current)
            else:
                raise ValueError
        except ValueError as e:
            print(f"chave '{key}' não encontrada")
            raise e

    def count_nodes(self) -> int:
        return sum(node.count_nodes() for node in self.nodes) + 1


if __name__ == "__main__":
    t = TrieTree()
    print(f'qtd: {t.count_nodes()}')
    t['camada'] = 2
    print(f'qtd: {t.count_nodes()}')
    t['cama'] = 42
    # print(f'qtd: {t.count_nodes()}')
    # t['nakama'] = 10
    # print(f'qtd: {t.count_nodes()}')
    # t.delete('nakama')
    print(f'qtd: {t.count_nodes()}')
    t.delete('camada')
