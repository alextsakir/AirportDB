from typing import NoReturn, Optional


class Vertex:

    def __init__(self, name: str = "unnamed vertex") -> NoReturn:
        self.name: str = name
        self.input: tuple[Edge] = tuple()
        self.output: Optional[Edge] = None
        return

    @staticmethod
    def function(argument: float) -> float:
        return 2 * argument

    @property
    def display(self) -> str:
        return self.name


class Edge:

    def __init__(self, weight: float) -> NoReturn:
        self._weight: float = weight
        self._vertices: tuple[Vertex] = tuple()
        return

    @property
    def weight(self) -> str:
        return str(self._weight)

    @property
    def vertices(self) -> str:
        return self._vertices[0].name + "-" + self._vertices[1].name


class Graph:

    def __init__(self) -> NoReturn:
        self.vertices: list[Vertex] = []
        self.edges: list[Edge] = []
        return
