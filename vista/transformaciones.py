import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from vista.matriz_entrada import MatrizEntrada
from sympy.matrices import eye


class Transformaciones(tk.LabelFrame):
    """
    Frame para introducir el alfabeto y las transformaciones unitarias
    """

    def __init__(self, master, dim, tipo, controlador, id_qfa):
        super().__init__(master, text='Alfabeto y transformaciones unitarias')
        self.dim = dim
        self.tipo = tipo
        self.controlador = controlador
        self.id_qfa = id_qfa
        self.t_dolar = eye(self.dim)
        self.seleccionado = None

        frame_anadir = tk.Frame(self)

        frame_alfabeto = tk.Frame(self)
        scrollbar = ttk.Scrollbar(frame_alfabeto, orient='vertical')
        self.alfabeto = tk.Listbox(frame_alfabeto, height=5, width=30,
                                   selectmode='single',
                                   yscrollcommand=scrollbar.set,
                                   exportselection=False)
        scrollbar.config(command=self.alfabeto.yview)
        self.alfabeto.grid(row=0, column=0, sticky='nsew')
        self.alfabeto.bind('<<ListboxSelect>>', self.cambiar_seleccion)
        scrollbar.grid(row=0, column=1, sticky='ns')
        frame_alfabeto.grid(row=1, column=0, columnspan=3, pady=5, padx=5,
                            sticky='nsew')
        frame_alfabeto.grid_rowconfigure(0, weight=1)

        self.entry_char = tk.StringVar()
        entry_simbolo = tk.Entry(frame_anadir, textvariable=self.entry_char,
                                 width=10)

        self.entry_char.trace("w", self.limitar_caracteres)

        self.anadir_simbolo = tk.Button(frame_anadir, text='Añadir',
                                        command=self.insertar_simbolo)
        self.boton_eliminar_simbolo = tk.Button(self, text='Eliminar',
                                                state='disabled',
                                                command=self.eliminar_simbolo)
        self.dolar = tk.Button(self, text='Transformación $',
                               command=self.cambiar_seleccion_dolar)

        self.transf_label = tk.Label(self, text='', font=("TkDefaultFont", 10))
        self.transf_label.grid(row=0, column=3, sticky='nsew')

        identidad = eye(self.dim)
        self.matriz = MatrizEntrada(self, self.dim, self.dim, identidad,
                                    state='disabled')
        self.check_unitaria = tk.Button(self, text='Comprobar unitaria',
                                        command=self.comprobar_matriz_unitaria,
                                        state='disabled')

        self.matriz.grid(row=1, column=3, padx=20, pady=5, sticky='nsew')
        self.check_unitaria.grid(row=2, column=3)

        entry_simbolo.grid(row=0, column=0, padx=5)
        self.anadir_simbolo.grid(row=0, column=1)

        frame_anadir.grid(row=0, column=0, padx=5, sticky='w')
        self.boton_eliminar_simbolo.grid(row=2, column=1, pady=5, sticky='e')
        if self.tipo == 'MMQFA':
            self.dolar.grid(row=2, column=0, padx=5, sticky='w')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def set_controlador(self, controlador):
        self.controlador = controlador

    def limitar_caracteres(self, *args):
        """
        Limita a uno el número de símbolos que se pueden introducir e impide
        introducir '$' si es un MMQFA
        :param args:
        :return:
        """
        if len(self.entry_char.get()) > 0:
            self.entry_char.set(self.entry_char.get()[-1])
        if self.tipo == 'MMQFA' and self.entry_char.get() == '$':
            self.entry_char.set('')

    def set_tipo(self, tipo):
        """
        Cambia el tipo del autómata
        :param tipo:
        :return:
        """
        anterior = self.tipo
        self.tipo = tipo
        if self.tipo == 'MMQFA':
            self.t_dolar = eye(self.dim)
            self.dolar.grid(row=2, column=0, padx=5, sticky='w')
        else:
            # No mostrar $ si se viene de un MMQFA
            if anterior == 'MMQFA' and self.seleccionado == '$':
                self.seleccionado = None
                self.alfabeto.selection_clear(0, 'end')
                self.transf_label.config(text='')
                self.boton_eliminar_simbolo.configure(state='disabled')
                self.matriz.set_state(state='disabled')
            self.dolar.grid_forget()

    def mostrar_transformacion(self, simbolo, transformacion, cambiar_dim):
        """
        Muestra transformación indicando que pertenece al símbolo
        :param simbolo:
        :param transformacion:
        :param cambiar_dim:
        :return:
        """
        self.transf_label.config(
            text='Transformación asociada al símbolo ' + simbolo)
        self.matriz.set_state(state='normal')
        self.cambiar_matriz(transformacion, cambiar_dim)
        self.seleccionado = simbolo
        if self.tipo != 'MMQFA' or self.seleccionado != '$':
            self.alfabeto.selection_set(
                self.alfabeto.get(0, 'end').index(self.seleccionado))

        self.boton_eliminar_simbolo.configure(state='normal')
        self.check_unitaria.configure(state='normal')

    def insertar_simbolo(self):
        """
        Inserta un símbolo en el alfabeto y selecciona la matriz para ese
        símbolo
        :return:
        """
        # Añadir símbolo en la listbox del alfabeto
        simbolo = self.entry_char.get()
        if simbolo not in self.alfabeto.get(0, 'end'):
            self.alfabeto.insert('end', simbolo)

            # Añadir la transformación asociada al símbolo
            identidad = eye(self.dim)
            self.controlador.anadir_transformacion(simbolo, identidad,
                                                   self.id_qfa)

            # Seleccionar el nuevo elemento
            self.alfabeto.selection_clear(0, 'end')
            self.alfabeto.selection_set('end')
            self.alfabeto.event_generate("<<ListboxSelect>>")

    def guardar_matriz_actual(self):
        """
        Llama al controlador para guardar la matriz mostrada como
        transformación asociada al símbolo seleccionado
        :return:
        """
        if self.seleccionado is not None:
            try:
                matriz = self.matriz.get_matriz_ev()
                self.controlador.anadir_transformacion(self.seleccionado,
                                                       matriz, self.id_qfa)
            except SyntaxError as e:
                raise e

    def cambiar_seleccion_dolar(self):
        """
        Selecciona la transformación asociada a '$'
        :return:
        """
        try:
            self.guardar_matriz_actual()
        except SyntaxError:
            pass

        transformacion = self.controlador.get_transformacion('$', self.id_qfa)
        self.mostrar_transformacion('$', transformacion, False)

    def cambiar_seleccion(self, event):
        """
        Cambia la selección de símbolo, mostrando la transformación del símbolo
        seleccionado
        :param event:
        :return:
        """
        try:
            self.guardar_matriz_actual()
        except SyntaxError:
            pass
        seleccionado = self.alfabeto.curselection()
        if len(seleccionado) > 0:
            simbolo = self.alfabeto.get(seleccionado)

            # Mostrar la transformación
            transformacion = self.controlador.get_transformacion(simbolo,
                                                                 self.id_qfa)
            self.mostrar_transformacion(simbolo, transformacion, False)

    def eliminar_simbolo(self):
        """
        Elimina el símbolo del alfabeto que está seleccionado
        :return:
        """
        simbolo = self.alfabeto.get(self.alfabeto.curselection())
        self.controlador.eliminar_transformacion(simbolo, self.id_qfa)
        self.alfabeto.delete(self.alfabeto.curselection()[0])
        self.boton_eliminar_simbolo.configure(state='disabled')

        # La condición es por si está seleccionado el $
        if simbolo == self.seleccionado:
            self.check_unitaria.configure(state='disabled')
            self.transf_label.config(text='')
            self.matriz.set_state(state='disabled')
            self.seleccionado = None

    def comprobar_matriz_unitaria(self):
        """
        Comprueba si la matriz que se está visualizando es unitaria
        :return:
        """
        try:
            self.guardar_matriz_actual()
            if self.controlador.comprobar_unitaria(self.seleccionado,
                                                   self.id_qfa):
                messagebox.showinfo(
                    message='La matriz introducida es unitaria')
            else:
                messagebox.showerror(
                    message='La matriz introducida no es unitaria')
        except SyntaxError:
            messagebox.showerror(
                message='La matriz introducida no es correcta')

    def escribir_alfabeto(self, alfabeto):
        """
        Muestra en la lista el alfabeto recibido como parámetro
        :return:
        """
        self.seleccionado = None
        self.alfabeto.delete(0, 'end')
        if alfabeto:
            for simbolo in alfabeto:
                self.alfabeto.insert('end', simbolo)

    def cambiar_matriz(self, matriz, cambiar_dim):
        """
        Actualiza el frame de la matriz a mostrar, creándolo de nuevo en caso
        de que se haya actualizado la dimensión
        :param matriz:
        :param cambiar_dim:
        :return:
        """
        if cambiar_dim:
            state = self.matriz.get_state()
            self.matriz = MatrizEntrada(self, self.dim, self.dim, matriz,
                                        state=state)
            self.matriz.grid_forget()
            self.matriz.grid(row=1, column=3, padx=20, pady=5, sticky='nsew')
        else:
            self.matriz.set_matriz(matriz)

    def set_dim(self, dim):
        self.dim = dim

    def get_transformacion(self):
        try:
            return self.seleccionado, self.matriz.get_matriz_ev()
        except SyntaxError as e:
            raise e
