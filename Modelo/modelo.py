from Modelo.moqfa import MOQFA
from Modelo.mmqfa import MMQFA
from Modelo.qfa import QFA
from sympy.matrices import eye, Matrix, zeros
from sympy import real_roots, sqrt
from sympy.abc import x
import math
from itertools import product
from typing import List


class Modelo:
    """
    Modelo que posee varios autómatas cuánticos y permite gestionar cada uno de ellos
    """

    def __init__(self, num_automatas: int):
        self.qfas: List[QFA] = []
        for i in range(num_automatas):
            self.qfas.append(MOQFA())
        self.ejemplos = ['MOD3', 'MOD7', 'a*b*', 'i', 's1', 's2', 'NEQ']

    def set_s_init(self, estado_inicial: Matrix, id_qfa: int):
        self.qfas[id_qfa].estado_inicial = estado_inicial

    def set_observable(self, observable: List[Matrix], id_qfa: int):
        self.qfas[id_qfa].observable = observable

    def get_transformacion(self, simbolo: chr, id_qfa: int) -> Matrix:
        # Añadir caso $
        return self.qfas[id_qfa].get_transformacion(simbolo)

    def anadir_transformacion(self, simbolo: chr, matriz: Matrix, id_qfa: int):
        self.qfas[id_qfa].anadir_transformacion(simbolo, matriz)

    def eliminar_transformacion(self, simbolo: chr, id_qfa: int):
        del self.qfas[id_qfa].transformaciones[simbolo]

    def cambiar_tipo(self, tipo: str, id_qfa: int):
        """
        Crea de nuevo el autómata que indique el identificador siguiendo el tipo indicado y manteniendo el resto de
        opciones como estaban
        :param tipo:
        :param id_qfa:
        :return:
        """
        dim = self.qfas[id_qfa].dim
        transformaciones = self.qfas[id_qfa].transformaciones
        observable = self.qfas[id_qfa].observable
        s_init = self.qfas[id_qfa].estado_inicial
        if tipo == 'MOQFA':
            self.qfas[id_qfa] = MOQFA(dim, s_init, transformaciones, [observable[0]])
        elif tipo == 'MMQFA':
            if len(observable) == 1:
                observable += [eye(dim), eye(dim)]
            self.qfas[id_qfa] = MMQFA(dim, s_init, transformaciones, observable)

    def cambiar_dim(self, dim: int, id_qfa: int):
        """
        Cambia la dimensión del autómata que indique el identificador modificando la dimensión de las matrices de las
        transformaciones y del observable e inicializándolas a la identidad
        :param dim:
        :param id_qfa:
        :return:
        """
        es_moqfa = isinstance(self.qfas[id_qfa], MOQFA)
        alfabeto = self.qfas[id_qfa].get_alfabeto()
        identidad = eye(dim)
        transformaciones = {simbolo: identidad for simbolo in alfabeto}
        if es_moqfa:
            observable = [eye(dim)]
            self.qfas[id_qfa] = MOQFA(dim=dim, transformaciones=transformaciones, observable=observable)
        else:
            observable = [eye(dim), eye(dim), eye(dim)]
            self.qfas[id_qfa] = MMQFA(dim=dim, transformaciones=transformaciones, observable=observable)

    def comparar_automatas(self, maximo: int):
        """
        Realiza la comparación de las secuencias de inputs hasta un tamaño máximo entre dos autómatas
        :param maximo:
        :return:
        """
        comb1 = self.simular_combinaciones(maximo, 0)
        comb2 = self.simular_combinaciones(maximo, 1)

        comparacion = {}
        for palabra, prob1 in comb1.items():
            prob2 = comb2[palabra]
            comparacion[palabra] = (prob1, prob2, math.isclose(prob1, prob2))

        return comparacion

    def comprobar_observable(self, id_qfa: int) -> bool:
        return self.qfas[id_qfa].comprobar_observable()

    def comprobar_unitaria(self, simbolo: chr, id_qfa: int) -> bool:
        return self.qfas[id_qfa].comprobar_unitaria(simbolo)

    def simular_combinaciones(self, maximo: int, id_qfa: int) -> dict:
        """
        Simula todas las combinaciones de palabras el autómata indicado por el identificador puede procesar hasta un
        tamaño máximo
        :param maximo:
        :param id_qfa:
        :return:
        """
        alfabeto = self.qfas[id_qfa].get_alfabeto()

        probabilidades = {}
        for n in range(maximo):
            palabras = [''.join(p) for p in product(alfabeto, repeat=n + 1)]
            for palabra in palabras:
                probabilidades[palabra] = self.qfas[id_qfa].leer_palabra(palabra)
        return probabilidades

    def leer_palabra(self, palabra: str, id_qfa: int):
        return self.qfas[id_qfa].leer_palabra(palabra)

    def get_automata(self, id_qfa: int):
        if isinstance(self.qfas[id_qfa], MOQFA):
            tipo = 'MOQFA'
        else:
            tipo = 'MMQFA'
        return self.qfas[id_qfa].dim, tipo, self.qfas[id_qfa].estado_inicial, self.qfas[id_qfa].transformaciones, \
            self.qfas[id_qfa].observable

    def es_correcto(self, id_qfa: int) -> bool:
        return self.qfas[id_qfa].es_correcto()

    def get_alfabeto(self, id_qfa: int) -> list:
        return list(self.qfas[id_qfa].transformaciones.keys())

    def evaluar_matrices(self, id_qfa: int):
        self.qfas[id_qfa].evaluar_matrices()

    def son_moqfa(self) -> bool:
        return isinstance(self.qfas[0], MOQFA) and isinstance(self.qfas[0], MOQFA)

    def set_ejemplo(self, nombre: str, id_qfa: int):
        """
        Establece las opciones que marque el ejemplo sobre el autómata que indique el identificador
        :param nombre:
        :param id_qfa:
        :return:
        """
        if nombre[:-1] == 'MOD':
            angulo = '2*pi/' + nombre[-1]
            transformacion = Matrix(
                [['cos(' + angulo + ')', '-sin(' + angulo + ')'], ['sin(' + angulo + ')', 'cos(' + angulo + ')']])

            aceptacion = zeros(2, 2)
            aceptacion[0, 0] = 1

            estado_inicial = Matrix([1, 0])

            self.qfas[id_qfa] = MOQFA(2, estado_inicial, {'a': transformacion}, [aceptacion])

        elif nombre == 'a*b*':
            dim = 4
            p = real_roots(x ** 3 + x - 1)[0]
            a_transf = Matrix(
                [[1 - p, sqrt(p * (1 - p)), 0, sqrt(p)], [sqrt(p * (1 - p)), p, 0, -sqrt(1 - p)], [0, 0, 1, 0],
                 [sqrt(p), -sqrt(1 - p), 0, 0]])
            b_transf = Matrix([[0, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0]])
            end_transf = Matrix([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])

            transformaciones = {'a': a_transf, 'b': b_transf}

            acc = zeros(dim)
            acc[2, 2] = 1
            rej = zeros(dim)
            rej[3, 3] = 1
            non = zeros(dim)
            non[0, 0] = 1
            non[1, 1] = 1

            lista = [sqrt(1 - p), sqrt(p), 0, 0]
            estado_inicial = Matrix(lista)

            self.qfas[id_qfa] = MMQFA(4, estado_inicial, transformaciones, [acc, rej, non], end_transf)

        elif nombre == 'i':
            dim = 3

            transformaciones = {'a': Matrix(
                [[-1 / 2, 1 / 2, 1 / sqrt(2)], [1 / 2, -1 / 2, 1 / sqrt(2)], [1 / sqrt(2), 1 / sqrt(2), 0]])}
            estado_inicial = Matrix([1 / sqrt(2), 1 / sqrt(2), 0])

            aceptacion = eye(dim)
            aceptacion[2, 2] = 0

            self.qfas[id_qfa] = MOQFA(dim, estado_inicial, transformaciones, [aceptacion])

        elif nombre == 's1':
            dim = 2

            transformaciones = {'a': Matrix([[0, 1], [1, 0]])}
            estado_inicial = Matrix([1, 0])

            aceptacion = eye(dim)
            aceptacion[1, 1] = 0

            self.qfas[id_qfa] = MOQFA(dim, estado_inicial, transformaciones, [aceptacion])

        elif nombre == 's2':
            dim = 2

            transformaciones = {'a': Matrix([[1 / sqrt(2), 1 / sqrt(2)], [1 / sqrt(2), -1 / sqrt(2)]])}
            estado_inicial = Matrix([1, 0])

            aceptacion = eye(dim)
            aceptacion[1, 1] = 0

            self.qfas[id_qfa] = MOQFA(dim, estado_inicial, transformaciones, [aceptacion])

        elif nombre == 'NEQ':
            dim = 2

            transformaciones = {
                'a': Matrix([['cos(sqrt(2)*pi)', '-sin(sqrt(2)*pi)'], ['sin(sqrt(2)*pi)', 'cos(sqrt(2)*pi)']]),
                'b': Matrix([['cos(-sqrt(2)*pi)', '-sin(-sqrt(2)*pi)'], ['sin(-sqrt(2)*pi)', 'cos(-sqrt(2)*pi)']])}
            estado_inicial = Matrix([1, 0])

            aceptacion = eye(dim)
            aceptacion[0, 0] = 0

            self.qfas[id_qfa] = MOQFA(dim, estado_inicial, transformaciones, [aceptacion])

        elif nombre == 'Ej. MMQFA':
            dim = 4

            transformaciones = {
                'a': Matrix([['1/2', '1/2', '0', '1/sqrt(2)'], ['1/2', '1/2', '0', '-1/sqrt(2)'], ['0', '0', '1', '0'],
                             ['1/sqrt(2)', '-1/sqrt(2)', '0', '0']])}

            end_transf = Matrix([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
            estado_inicial = Matrix([1, 0, 0, 0])
            acc = zeros(dim)
            acc[2, 2] = 1
            non = zeros(dim)
            non[0, 0] = 1
            non[1, 1] = 1
            rej = zeros(dim)
            rej[3, 3] = 1

            self.qfas[id_qfa] = MMQFA(dim, estado_inicial, transformaciones, [acc, rej, non], end_transf)
