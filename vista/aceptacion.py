import tkinter as tk
from tkinter import messagebox
from sympy.matrices import eye

from .matriz_entrada import MatrizEntrada


class Aceptacion(tk.LabelFrame):
    """
    Frame para introducir la regla de aceptación, es decir, los subespacios
    necesarios del observable
    """

    def __init__(self, parent, dim, tipo, controlador, id_qfa):
        super().__init__(parent, text='Regla de aceptación')
        self.dim = dim
        self.tipo = tipo
        self.controlador = controlador
        self.id_qfa = id_qfa

        identidad = eye(self.dim)

        # Matrices de los subespacios
        label_acc = tk.Label(self, text='Subespacio de aceptación')
        self.label_rej = tk.Label(self, text='Subespacio de no aceptación')
        self.label_non = tk.Label(self, text='Subespacio de no parada')

        label_acc.grid(row=1, column=0)
        self.label_rej.grid(row=1, column=1)
        self.label_non.grid(row=1, column=2)

        self.matriz_acc = MatrizEntrada(self, self.dim, self.dim, identidad)
        self.matriz_rej = MatrizEntrada(self, self.dim, self.dim, identidad)
        self.matriz_non = MatrizEntrada(self, self.dim, self.dim, identidad)

        self.matriz_acc.grid(row=2, column=0, padx=5, sticky='nsew')
        self.matriz_rej.grid(row=2, column=1, padx=5, sticky='nsew')
        self.matriz_non.grid(row=2, column=2, padx=5, sticky='nsew')

        state = 'disabled'
        if self.tipo == 'MMQFA':
            state = 'normal'
        self.set_estado_subs(state)

        # Botón para comprobar que el observable es correcto
        check_button = tk.Button(self, text='Comprobar observable',
                                 command=self.comprobar_observable)
        check_button.grid(row=3, column=1, pady=5)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def set_controlador(self, controlador):
        self.controlador = controlador

    def set_dim(self, dim):
        self.dim = dim

    def set_tipo(self, tipo):
        """
        Establece el tipo de autómata y habilita o deshabilita las opciones
        según el caso
        :param tipo:
        :return:
        """
        self.tipo = tipo
        state = 'normal'
        if self.tipo == 'MOQFA':
            state = 'disabled'

        self.set_estado_subs(state)

    def set_estado_subs(self, state):
        self.matriz_rej.set_state(state=state)
        self.matriz_non.set_state(state=state)
        self.label_rej.configure(state=state)
        self.label_non.configure(state=state)

    def get_observable(self):
        try:
            if self.tipo == 'MOQFA':
                return [self.matriz_acc.get_matriz_ev()]
            else:
                return [self.matriz_acc.get_matriz_ev(),
                        self.matriz_rej.get_matriz_ev(),
                        self.matriz_non.get_matriz_ev()]
        except SyntaxError as e:
            raise e

    def comprobar_observable(self):
        """
        Muestra la ventana correspondiente en función de si el observable es
        correcto o no
        :return:
        """
        try:
            observable = self.get_observable()
            if self.controlador.comprobar_observable(observable, self.id_qfa):
                messagebox.showinfo(message='Observable correcto')
            else:
                messagebox.showerror(message='Observable incorrecto')
        except SyntaxError:
            messagebox.showerror(
                message='Error: las matrices introducidas no son correctas')

    def refrescar_matrices(self):
        self.matriz_acc.grid_forget()
        self.matriz_rej.grid_forget()
        self.matriz_non.grid_forget()

        self.matriz_acc.grid(row=2, column=0, padx=5, sticky='nsew')
        self.matriz_rej.grid(row=2, column=1, padx=5, sticky='nsew')
        self.matriz_non.grid(row=2, column=2, padx=5, sticky='nsew')

    def set_subespacios(self, observable, cambiar_dim):
        """
        Establece las matrices correspondientes a las proyecciones sobre los
        subespacios, creando de nuevo los frames en caso de que haya que
        cambiar la dimensión
        :param observable:
        :param cambiar_dim:
        :return:
        """
        state = 'normal'
        acc = observable[0]
        if self.tipo == 'MOQFA':
            state = 'disabled'
            rej = eye(self.dim)
            non = eye(self.dim)
        else:
            rej = observable[1]
            non = observable[2]

        if cambiar_dim:
            self.matriz_acc = MatrizEntrada(self, self.dim, self.dim, acc)
            self.matriz_rej = MatrizEntrada(self, self.dim, self.dim, rej,
                                            state=state)
            self.matriz_non = MatrizEntrada(self, self.dim, self.dim, non,
                                            state=state)

        else:
            self.matriz_acc.set_matriz(acc)
            self.matriz_rej.set_matriz(rej)
            self.matriz_non.set_matriz(non)

            self.matriz_rej.set_state(state)
            self.matriz_non.set_state(state)

    def mostrar_observable(self, observable, cambiar_dim):
        """
        Establece la regla de aceptación según las opciones recibidas
        :param cambiar_dim:
        :param observable:
        :return:
        """
        self.set_subespacios(observable, cambiar_dim)
        self.refrescar_matrices()
