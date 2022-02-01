from sympy.matrices import Matrix
from sympy.physics.quantum.dagger import Dagger
from typing import List, Dict


class QFA:
    """
    Clase que representa un autómata finito cuántico
    """

    def __init__(self, dim: int = 3, estado_inicial: Matrix = None,
                 transformaciones: Dict[chr, Matrix] = None,
                 observable: List[Matrix] = None):
        if transformaciones is None:
            transformaciones = {}
        self.dim = dim
        self.estado_inicial = estado_inicial
        self.transformaciones = transformaciones
        self.observable = observable

    def anadir_transformacion(self, simbolo: chr, matriz: Matrix):
        self.transformaciones[simbolo] = matriz

    def get_alfabeto(self):
        return list(self.transformaciones.keys())

    def medir(self, estado: Matrix) -> list:
        """
        Proyecta el estado sobre cada uno de los subespacios del observable
        :param estado:
        :return: cada una de las proyecciones
        """
        proyecciones = []
        for subespacio in self.observable:
            proyecciones.append(subespacio * estado)

        return proyecciones

    def leer_palabra(self, palabra: str):
        pass

    def es_correcto(self):
        """
        Comprueba si las opciones del autómata configuran un autómata correcto
        :return:
        """
        for simbolo in self.transformaciones.keys():
            if not self.comprobar_unitaria(simbolo):
                return False

        return bool(self.transformaciones) and self.comprobar_observable()

    def evaluar_matrices(self):
        """
        Evalua las matrices del autómata. Necesario para un procesamiento de
        palabras más rápido
        :return:
        """
        self.estado_inicial = self.estado_inicial.evalf()
        self.transformaciones = {simbolo: transformacion.evalf() for
                                 simbolo, transformacion in
                                 self.transformaciones.items()}
        self.observable = [proyeccion.evalf() for proyeccion in
                           self.observable]

    def get_transformacion(self, simbolo: chr):
        return self.transformaciones[simbolo]

    def comprobar_unitaria(self, simbolo: chr) -> bool:
        """
        Comprueba que la matriz de la transformación asociada al símbolo sea
        unitaria
        :param simbolo:
        :return:
        """
        pass

    def comprobar_observable(self) -> bool:
        """
        Comprueba que el observable sea correcto
        :return:
        """
        pass

    def comprobar_proy(self) -> bool:
        """
        Comprueba si las matrices del observable son proyecciones ortogonales
        :return:
        """
        for matriz in self.observable:
            if not matriz.is_square or not matriz.equals(
                    Dagger(matriz)) or not matriz.equals(matriz ** 2):
                return False
        return True
