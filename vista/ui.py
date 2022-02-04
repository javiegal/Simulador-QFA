import tkinter as tk

from .vista_inicio import VistaInicio
from .vista_simular import VistaSimular
from .vista_comparar import VistaComparar


class UI(tk.Tk):
    """
    Interfaz de la aplicación con tres frames: el inicial de creación de
    autómatas, el de simulación de un autómata y el de comparación de dos
    autómatas
    """

    def __init__(self, num_automatas, controlador=None):
        super().__init__()

        self.controlador = controlador
        self.title('Simulador QFA')
        self.geometry('750x650')
        self.resizable(False, False)

        self.frame_inicio = VistaInicio(self, self.controlador, num_automatas)
        self.frame_simular = VistaSimular(self, self.controlador)
        self.frame_comparar = VistaComparar(self, self.controlador)

        self.frame_inicio.grid(row=1, column=0, sticky="nsew")
        self.actual = self.frame_inicio

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def set_controlador(self, controlador):
        self.controlador = controlador
        self.frame_inicio.set_controlador(controlador)
        self.frame_comparar.set_controlador(controlador)
        self.frame_simular.set_controlador(controlador)

    def mostrar_simular(self, alfabeto, id_qfa):
        """
        Cambia el frame actual por el de simular un autómata
        :return:
        """
        self.actual.grid_forget()
        self.frame_simular.set_alfabeto(alfabeto)
        self.frame_simular.set_id_qfa(id_qfa)
        self.frame_simular.borrar_info()
        self.frame_simular.grid(row=1, column=0, sticky="nsew")
        self.actual = self.frame_simular

    def mostrar_comparar(self):
        """
        Cambia el frame actual por el de comparar dos autómatas
        :return:
        """
        self.actual.grid_forget()
        self.frame_comparar.borrar_informacion()
        self.frame_comparar.grid(row=1, column=0, sticky="nsew")
        self.actual = self.frame_comparar

    def mostrar_inicio(self):
        """
        Cambia el frame actual por el inicial
        :return:
        """
        self.actual.grid_forget()
        self.frame_inicio.grid(row=1, column=0, sticky="nsew")
        self.actual = self.frame_inicio

    def actualizar_automata(self, id_qfa, dim=None, tipo=None, s_init=None,
                            simbolo=None, transformacion=None,
                            observable=None, alfabeto=None):
        self.frame_inicio.actualizar_automata(id_qfa, dim, tipo, s_init,
                                              simbolo, transformacion,
                                              observable, alfabeto)
