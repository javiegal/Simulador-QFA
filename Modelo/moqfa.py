from Modelo.qfa import QFA
from sympy.physics.quantum.dagger import Dagger
from sympy.matrices import eye


class MOQFA(QFA):
    """
    Clase que representa un autómata finito cuántico measure once
    """

    def __init__(self, dim=3, estado_inicial=None, transformaciones=None, observable=None):
        if observable is None:
            observable = [eye(dim)]
        super().__init__(dim, estado_inicial, transformaciones, observable)

    def leer_palabra(self, palabra: str):
        """
        Lee una palabra del modo en que lo hacen los autómatas measure once: aplica las transformaciones unitarias y
        luego realiza una medición
        :param palabra: ha de estar en el alfabeto
        :return: probabilidad de aceptación de la palabra
        """
        estado = self.estado_inicial
        for simbolo in palabra:
            estado = self.transformaciones[simbolo] * estado
        proyecciones = self.medir(estado)
        aceptacion = Dagger(proyecciones[0]).dot(proyecciones[0])
        return aceptacion

    def comprobar_unitaria(self, simbolo: chr) -> bool:
        matriz = self.transformaciones[simbolo]
        if matriz.is_square:
            producto = matriz * Dagger(matriz)
            resultado = producto.equals(eye(self.dim))
            return resultado
        else:
            return False

    def comprobar_observable(self) -> bool:
        return self.comprobar_proy()
