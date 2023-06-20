

def _removeprefix(string: str, prefix: str) -> str:
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string[:]


def _match_prefix(s1: str, s2: str) -> str:
    roof = min(len(s1), len(s2))
    i = 0
    while i < roof and s1[i] == s2[i]:
        i += 1
    return s1[:i]


class PatrieciaTree:
    def __init__(self, substr: str = '', is_last_substr: bool = False) -> None:
        self.substr = substr
        self.is_last_substr = is_last_substr 
        self.nodes = [] 
        # value: any
    
    def __setitem__(self, key, value):
        self.insert(key, value)

    def __getitem__(self, item: str):
        return self.retrieve(item)

    def __contains__(self, substr):
        return any(substr == node.substr for node in self.nodes)

    def __str__(self) -> str:
        return f"({self.substr}{'*' if self.is_last_substr else ''} [{len(self.nodes)}])"

    @property
    def is_empty(self) -> bool:
        return not bool(self.nodes)

    def _get_substr(self, substr: str) -> "PatrieciaTree|None":
        return next(
            (node for node in self.nodes if substr[0] == node.substr[0]),
            None
        )

    def _recursive_delete(self, sub_key: str) -> bool:
        if sub_key == "":
            # self.value = None
            self.is_last_substr = False
            print(f"Node {self} deixou de ser fim de palavra")

        elif next_node := self._get_substr(sub_key[0]):
            if next_node._recursive_delete(sub_key[1:]) and not next_node.is_last_substr:
                # remove node from list and delete
                self.nodes.remove(next_node)
                print(f"Node {next_node} deletado")
        else:
            raise ValueError(f"sequência '{sub_key}' não encontrada")
        return self.is_empty or self.is_last_substr

    def insert(self, key: str, value: any):
        prefix = _match_prefix(self.substr, key)
        if key := _removeprefix(key, prefix):
            # end is ahead
            if next_node := self._get_substr(key):
                next_node.insert(key, value)
            else:
                self.nodes.append(
                    PatrieciaTree(key, True)
                )
        elif len(prefix) == len(self.substr):
            self.is_last_substr = True
        elif len(prefix) < len(self.substr):
            new_node = PatrieciaTree(
                _removeprefix(self.substr, prefix),
                self.is_last_substr,
            )
            new_node.nodes = self.nodes
            self.nodes = [new_node]
            self.substr = prefix
            self.is_last_substr = True

    def retrieve(self, key: str, _chain: str = '*') -> any:
        if prefix := _match_prefix(self.substr, key):
            _chain += f'->{prefix}'
        try:
            if (key := _removeprefix(key, prefix)) and (next_node := self._get_substr(key)):
                next_node.retrieve(key, _chain)
            elif len(prefix) == len(self.substr) and self.is_last_substr:
                # palavra encontrada
                print(f"palvavra '{_chain}|{key}' encontrada")
                # return current.value
            else:
                raise ValueError(f"palvavra '{_chain}[{key}]' não encontrada")
        except ValueError as e:
            print(e)
            # raise e

    def delete(self, key, _chain: str = '*') -> any:
        if prefix := _match_prefix(self.substr, key):
            _chain += f'->{prefix}'
        try:
            if (key := _removeprefix(key, prefix)) and (child_node := self._get_substr(key)):
                if child_node.delete(key, _chain):
                    self.nodes.remove(child_node)
            elif len(prefix) == len(self.substr) and self.is_last_substr:
                # palavra encontrada
                self.is_last_substr = False
                print(f"palvavra '{_chain}|{key}' deletada")
                if len(self.nodes) == 1:
                    # absorver nó caso tenha apenas 1 filho
                    node = self.nodes[0]
                    print(f'Nó "{self.substr}" absorveu "{node.substr}"')
                    self.substr += node.substr
                    self.nodes = node.nodes
                    self.is_last_substr = node.is_last_substr
                # nó deve ser removido do pai se:
                # - estiver vazio;
                # - não for fim de palavra
                return self.is_empty and not self.is_last_substr
            else:
                raise ValueError(f"palvavra '{_chain}[{key}]' não encontrada")
        except ValueError as e:
            print(e)
            # raise e

    def count_nodes(self) -> int:
        return sum(node.count_nodes() for node in self.nodes) + 1


if __name__ == "__main__":
    t = PatrieciaTree()
    t["cama"] = 24
    # t["camada"] = 42
    t["camarada"] = 2
    t['camaradagem'] = 8
    t.count_nodes()
