from vista.ui import UI
from modelo.modelo import Modelo


class Controlador:
    def __init__(self, modelo: Modelo, ui: UI):
        self.modelo = modelo
        self.ui = ui

    def simular_palabra(self, palabra, id_qfa):
        """
        Solicita al modelo la lectura de una palabra por parte del autómata que
        indique el identificador
        :param palabra:
        :param id_qfa:
        :return:
        """
        return self.modelo.leer_palabra(palabra, id_qfa)

    def simular_combinaciones(self, maximo, id_qfa):
        """
        Solicita al modelo la lectura de todas las palabras hasta una longitud
        máxima por parte del autómata que
        indique el identificador
        :param maximo:
        :param id_qfa:
        :return:
        """
        return self.modelo.simular_combinaciones(maximo, id_qfa)

    def ejecutar_comparacion(self, maximo):
        """
        Solicita al modelo la comparación de dos autómatas con secuencias de
        inputs de hasta una longitud máxima
        :param maximo:
        :return:
        """
        return self.modelo.comparar_automatas(maximo)

    def simular_automata(self, estado_inicial, observable, simbolo, matriz,
                         id_qfa):
        """
        Actualiza el autómata que indique el identificador con las opciones
        recibidas como parámetros y, en caso de poder, pasa a simular el
        autómata. La evaluación previa a la simulación se debe a que así los
        productos de matrices se ejecutarán más rápido
        :param estado_inicial:
        :param observable:
        :param simbolo:
        :param matriz:
        :param id_qfa:
        :return:
        """
        self.modelo.set_s_init(estado_inicial, id_qfa)
        if simbolo is not None:
            self.modelo.anadir_transformacion(simbolo, matriz, id_qfa)
        self.modelo.set_observable(observable, id_qfa)
        if self.modelo.es_correcto(id_qfa):
            self.modelo.evaluar_matrices(id_qfa)
            self.ui.mostrar_simular(self.modelo.get_alfabeto(id_qfa), id_qfa)
            return True
        else:
            return False

    def comparar_automatas(self, s_init, simbolo, matriz, observable, s_init_2,
                           simbolo_2, matriz_2, observable_2):
        """
        Actualiza los autómatas con las opciones recibidas como parámetros y,
        en caso de poder, pasa a compararlos.
        :param s_init:
        :param simbolo:
        :param matriz:
        :param observable:
        :param s_init_2:
        :param simbolo_2:
        :param matriz_2:
        :param observable_2:
        :return:
        """
        self.modelo.set_s_init(s_init, 0)
        if simbolo is not None:
            self.modelo.anadir_transformacion(simbolo, matriz, 0)
        self.modelo.set_observable(observable, 0)

        self.modelo.set_s_init(s_init_2, 1)
        if simbolo_2 is not None:
            self.modelo.anadir_transformacion(simbolo_2, matriz_2, 1)
        self.modelo.set_observable(observable_2, 1)

        if self.modelo.son_moqfa() and self.modelo.es_correcto(
            0) and self.modelo.es_correcto(
            1) and self.modelo.get_alfabeto(
                0) == self.modelo.get_alfabeto(1):
            self.modelo.evaluar_matrices(0)
            self.modelo.evaluar_matrices(1)
            self.ui.mostrar_comparar()
            return True
        else:
            return False

    def anadir_transformacion(self, simbolo, matriz, id_qfa):
        self.modelo.anadir_transformacion(simbolo, matriz, id_qfa)

    def get_transformacion(self, simbolo, id_qfa):
        return self.modelo.get_transformacion(simbolo, id_qfa)

    def eliminar_transformacion(self, simbolo, id_qfa):
        self.modelo.eliminar_transformacion(simbolo, id_qfa)

    def comprobar_unitaria(self, simbolo, id_qfa):
        return self.modelo.comprobar_unitaria(simbolo, id_qfa)

    def comprobar_observable(self, observable, id_qfa):
        self.modelo.set_observable(observable, id_qfa)
        return self.modelo.comprobar_observable(id_qfa)

    def actualizar_dim(self, dim, id_qfa):
        self.modelo.cambiar_dim(dim, id_qfa)

    def actualizar_tipo(self, tipo, id_qfa):
        self.modelo.cambiar_tipo(tipo, id_qfa)

    def seleccionar_ejemplo(self, ejemplo, id_qfa):
        """
        Actualiza el modelo seleccionando el autómata indicado y después lo
        muestra
        :param ejemplo:
        :param id_qfa:
        :return:
        """
        self.modelo.set_ejemplo(ejemplo, id_qfa)
        dim, tipo, s_init, transformaciones, observable = self.modelo.get_automata(
            id_qfa)
        alfabeto = list(transformaciones.keys())
        simbolo = alfabeto[0]
        self.ui.actualizar_automata(id_qfa, dim, tipo, s_init, simbolo,
                                    transformaciones[simbolo], observable,
                                    alfabeto)
