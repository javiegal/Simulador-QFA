import tkinter as tk
from tkinter import ttk
from Vista.transformaciones import Transformaciones
from Vista.aceptacion import Aceptacion
from Vista.matriz_entrada import MatrizEntrada
from sympy.matrices import Matrix, eye


class VistaCrear(tk.Frame):
    """
    Frame para mostrar un autómata y poder modificarlo rellenando los campos necesarios
    """

    def __init__(self, master, controlador, id_qfa, dim=3, tipo='MOQFA'):
        super().__init__(master, padx=5, pady=2)
        self.dim = dim
        self.tipo = tipo
        self.controlador = controlador
        self.id_qfa = id_qfa

        # Frame opciones
        self.frame_opc = tk.LabelFrame(self, text='Opciones generales')
        self.frame_opc.grid(row=0, column=0, sticky='nsew')

        frame2 = tk.Frame(self.frame_opc)
        tipo_label = tk.Label(frame2, text='Tipo de autómata:')
        self.combobox = ttk.Combobox(frame2, state='readonly', width=10)
        self.combobox['values'] = ['MOQFA', 'MMQFA']
        self.combobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.cambiar_tipo)

        tipo_label.grid(row=0, column=0, padx=5, sticky='w')
        self.combobox.grid(row=0, column=1, padx=5, sticky='w')

        separator = ttk.Separator(frame2, orient='vertical')
        separator.grid(row=0, column=2, padx=10, sticky='n')

        dim_label = tk.Label(frame2, text='Dimensión de H:')
        dim_label.grid(row=0, column=3, padx=5, pady=5)

        var = tk.StringVar(frame2)
        var.set(str(dim))
        self.dim_spinbox = tk.Spinbox(frame2, from_=2, to=6, justify='right', textvariable=var, width=3)
        self.dim_spinbox.grid(row=0, column=4, pady=5, padx=5)
        boton_dimension = tk.Button(frame2, text='Establecer', command=self.cambiar_dim)
        boton_dimension.grid(row=0, column=5, padx=5)

        ejemplos_label = tk.Label(frame2, text='Seleccionar ejemplo:')
        ejemplos_label.grid(row=0, column=6, padx=5, pady=5, sticky='e')

        self.ejemplos = ['MOD3', 'MOD7', 'a*b*', 'NEQ', 'i', 's1', 's2', 'Ej. MMQFA']
        self.ejemplos_box = ttk.Combobox(frame2, state='readonly', width=10)
        self.ejemplos_box.grid(row=0, column=7, padx=5)
        self.ejemplos_box['values'] = self.ejemplos

        self.ejemplos_box.bind("<<ComboboxSelected>>", self.seleccionar_ejemplo)

        self.frame_s_init = tk.Frame(self.frame_opc)
        s_init_label = tk.Label(self.frame_s_init, text='Estado inicial:')

        vector = Matrix([1] + [0] * (self.dim - 1))
        self.s_init = MatrizEntrada(self.frame_s_init, 1, self.dim, vector.T)

        s_init_label.grid(row=0, column=0, padx=5, sticky='w')
        self.s_init.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        frame2.grid(row=0, column=0, sticky='nsew')
        frame2.grid_columnconfigure(6, weight=1)

        self.frame_s_init.grid(row=1, column=0, sticky='nsew')
        self.frame_s_init.grid_columnconfigure(1, weight=1)

        self.frame_opc.grid_columnconfigure(0, weight=1)

        # Frame transformaciones
        self.transformaciones = Transformaciones(self, self.dim, self.tipo, self.controlador, self.id_qfa)
        self.transformaciones.grid(row=1, column=0, sticky='nsew', pady=5)

        # Frame regla de aceptación
        self.aceptacion = Aceptacion(self, self.dim, self.tipo, self.controlador, self.id_qfa)
        self.aceptacion.grid(row=2, column=0, sticky='nsew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def set_controlador(self, controlador):
        self.controlador = controlador
        self.transformaciones.set_controlador(controlador)
        self.aceptacion.set_controlador(controlador)

    def cambiar_tipo(self, event):
        """
        Cambia el tipo de autómata actual haciendo los cambios necesarios en la vista y llamando al controlador para
        que actualice el modelo
        :param event:
        :return:
        """
        tipo = self.combobox.get()
        if tipo != self.tipo:
            self.tipo = tipo
            self.aceptacion.set_tipo(tipo)
            self.transformaciones.set_tipo(tipo)
            self.controlador.actualizar_tipo(tipo, self.id_qfa)

    def cambiar_dim(self):
        """
        Actualiza la dimensión en todos los frames
        :return:
        """
        # Establecer dimensión
        dim = int(self.dim_spinbox.get())
        self.controlador.actualizar_dim(dim, self.id_qfa)
        self.actualizar_dim_matrices(dim)

    def reescribir_s_init(self, vector):
        """
        Reescribe el estado inicial según el vector recibido como parámetro
        :param vector:
        :return:
        """
        self.s_init.grid_forget()
        self.s_init = MatrizEntrada(self.frame_s_init, 1, self.dim, vector.T)
        self.s_init.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

    def mostrar_automata(self, dim, tipo, s_init, simbolo, transformacion, observable, alfabeto):
        """
        Muestra el autómata dado por las opciones recibidas
        :param dim:
        :param tipo:
        :param s_init:
        :param simbolo:
        :param transformacion:
        :param observable:
        :param alfabeto:
        :return:
        """
        cambiar_dim = self.dim != dim
        cambiar_tipo = self.tipo != tipo

        if cambiar_dim:
            self.dim_spinbox.delete(0, 'end')
            self.dim_spinbox.insert(0, str(dim))
            self.dim = dim
            self.transformaciones.set_dim(dim)
            self.aceptacion.set_dim(dim)
            self.reescribir_s_init(s_init)
        else:
            self.s_init.set_matriz(s_init.T)

        if cambiar_tipo:
            self.tipo = tipo
            self.transformaciones.set_tipo(tipo)
            self.aceptacion.set_tipo(tipo)

        self.transformaciones.escribir_alfabeto(alfabeto)
        self.transformaciones.mostrar_transformacion(simbolo, transformacion, cambiar_dim)
        self.aceptacion.mostrar_observable(observable, cambiar_dim)

    def get_s_init(self):
        """
        Devuelve el estado inicial parseado
        :return:
        """
        try:
            return self.s_init.get_matriz_ev().T
        except SyntaxError as e:
            raise e

    def seleccionar_ejemplo(self, event):
        """
        Llama al controlador para actualizar el autómata según el ejemplo seleccionado
        :param event:
        :return:
        """
        ejemplo = self.ejemplos_box.get()
        self.controlador.seleccionar_ejemplo(ejemplo, self.id_qfa)

    def get_transformacion(self):
        try:
            return self.transformaciones.get_transformacion()
        except SyntaxError as e:
            raise e

    def get_observable(self):
        try:
            return self.aceptacion.get_observable()
        except SyntaxError as e:
            raise e

    def actualizar_dim_matrices(self, dim):
        """
        Actualiza la dimensión de las matrices de las transformaciones, estado inicial y observable
        :param dim:
        :return:
        """
        self.dim = dim
        self.transformaciones.set_dim(dim)
        self.aceptacion.set_dim(dim)
        self.reescribir_s_init(eye(dim))
        self.transformaciones.cambiar_matriz(eye(dim), True)
        self.aceptacion.mostrar_observable([eye(dim), eye(dim), eye(dim)], True)
