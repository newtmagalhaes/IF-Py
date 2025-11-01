# 2025.2 Introdução à Ciência de Dados


## Orange

```bash
# run Orange canvas
python -m Orange.canvas
```

## Notebooks

Adicione a raiz do repositório aos paths dos notebooks para poder importar de arquivos python.

> Altere a quantidade de 'parent' até chegar do notebook à raiz do repositório.

```python
import sys
from os import getcwd
from pathlib import Path

sys.path.append(str(Path(getcwd()).parent.parent.absolute()))
```
