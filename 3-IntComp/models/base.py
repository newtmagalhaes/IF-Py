from dataclasses import dataclass


class Ambiente:
    pass


@dataclass
class Sensor:
    ambiente: Ambiente


class Atuador:
    pass


@dataclass
class Agente:
    ambiente: Ambiente
    sensores: list[Sensor]
    atuadores: list[Atuador]
