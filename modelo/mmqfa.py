from sympy.physics.quantum.dagger import Dagger
from sympy.matrices import eye, Matrix, zeros

from .qfa import QFA


class MMQFA(QFA):
    """
    Clase que representa un autómata finito cuántico measure many
    """

    def __init__(self, dim=3, estado_inicial=None, transformaciones=None,
                 observable=None, t_dolar: Matrix = None):
        if observable is None:
            observable = [eye(dim), eye(dim), eye(dim)]
        super().__init__(dim, estado_inicial, transformaciones, observable)
        if t_dolar is None:
            t_dolar = eye(dim)
        self.transformacion_dolar = t_dolar

    def leer_palabra(self, palabra: str):
        """
        Lee una palabra del modo en que lo hacen los autómatas measure many:
        tras la aplicación de una transformación unitaria se hace una medición
        :param palabra: compuesta por símbolos del autómata (menos $)
        :return: probabilidad de aceptación de la palabra
        """
        estado = self.estado_inicial
        aceptacion = 0
        for simbolo in palabra:
            estado = self.transformaciones[simbolo].evalf() * estado
            proyecciones = self.medir(estado)
            estado = proyecciones[-1]
            aceptacion += Dagger(proyecciones[0]).dot(proyecciones[0])

        proyecciones = self.medir(self.transformacion_dolar * estado)
        aceptacion += Dagger(proyecciones[0]).dot(proyecciones[0])

        return float(aceptacion)

    def evaluar_matrices(self):
        self.transformacion_dolar = self.transformacion_dolar.evalf()
        super().evaluar_matrices()

    def anadir_transformacion(self, simbolo, matriz):
        if simbolo == '$':
            self.transformacion_dolar = matriz
        else:
            self.transformaciones[simbolo] = matriz

    def get_transformacion(self, simbolo):
        if simbolo == '$':
            return self.transformacion_dolar
        else:
            return self.transformaciones[simbolo]

    def comprobar_unitaria(self, simbolo) -> bool:
        if simbolo == '$':
            matriz = self.transformacion_dolar
        else:
            matriz = self.transformaciones[simbolo]
        if matriz.is_square:
            producto = matriz * Dagger(matriz)
            resultado = producto.equals(eye(self.dim))
            return resultado
        else:
            return False

    def comprobar_observable(self) -> bool:
        mismo_tam = all(
            [self.observable[i].shape == self.observable[i + 1].shape for i in
             range(len(self.observable) - 1)])
        if mismo_tam:
            son_proyecciones = self.comprobar_proy()
            # Se comprueba si las matrices representan subespacios
            # complementarios y suman el total
            dim = self.observable[0].shape[0]
            zero = zeros(dim)
            complementarias = True
            for i in range(len(self.observable)):
                for j in range(i + 1, len(self.observable)):
                    complementarias = complementarias and self.observable[i] * \
                                      self.observable[j] == zero
            suma = self.observable[0] + self.observable[1] + self.observable[2]
            return son_proyecciones and complementarias and suma == eye(dim)
        else:
            return False
