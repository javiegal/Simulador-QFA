import tkinter as tk
from tkinter import ttk
from vista.vista_crear import VistaCrear
from tkinter import messagebox


class VistaInicio(tk.Frame):
    """
    Pantalla inicial de la interfaz. Contiene dos frames de creación de
    autómatas pudiendo pasar de uno al otro mediante un combobox
    """

    def __init__(self, master, controlador, num_automatas):
        super().__init__(master)
        self.controlador = controlador

        frame_navegacion = tk.LabelFrame(self)
        sel_automata = tk.Label(frame_navegacion, text='Autómata:')
        self.combobox_seleccion = ttk.Combobox(frame_navegacion,
                                               state='readonly')
        self.combobox_seleccion['values'] = ['Autómata ' + str(i + 1) for i in
                                             range(num_automatas)]
        self.combobox_seleccion.set('Autómata 1')
        self.combobox_seleccion.bind("<<ComboboxSelected>>",
                                     self.cambiar_automata)

        sel_automata.grid(row=0, column=0, padx=5, pady=5)
        self.combobox_seleccion.grid(row=0, column=1)

        self.boton_simular = tk.Button(frame_navegacion,
                                       text='Simular autómata 1',
                                       command=self.simular_automata)
        self.boton_simular.grid(row=0, column=3, pady=5, padx=10, sticky='e')
        boton_comparar = tk.Button(frame_navegacion, text='Comparar autómatas',
                                   command=self.comparar_automatas)
        boton_comparar.grid(row=0, column=2, sticky='e')

        frame_navegacion.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        frame_navegacion.grid_columnconfigure(2, weight=1)

        separator = ttk.Separator(self, orient='horizontal')
        separator.grid(row=1, column=0, pady=10, sticky='ew')

        self.vistas = []
        for i in range(num_automatas):
            self.vistas.append(VistaCrear(self, controlador, i))
        self.vista_actual = 0

        self.vistas[self.vista_actual].grid(row=2, column=0, sticky='nsew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def set_controlador(self, controlador):
        self.controlador = controlador
        self.vistas[0].set_controlador(controlador)
        self.vistas[1].set_controlador(controlador)

    def cambiar_automata(self, event):
        """
        Cambia la vista entre los dos posibles autómatas a crear
        :param event:
        :return:
        """
        if self.combobox_seleccion.get() == 'Autómata 1':
            self.vista_actual = 0
            self.boton_simular.configure(text='Simular autómata 1')
        else:
            self.vista_actual = 1
            self.boton_simular.configure(text='Simular autómata 2')

        self.vistas[(self.vista_actual + 1) % 2].grid_forget()
        self.vistas[self.vista_actual].grid(row=2, column=0, sticky='nsew')

    def simular_automata(self):
        """
        Transmite al controlador que ha sido pulsado el botón simular si el
        autómata introducido es correcto
        :return:
        """
        try:
            s_init = self.vistas[self.vista_actual].get_s_init()
            simbolo, matriz = self.vistas[
                self.vista_actual].get_transformacion()
            observable = self.vistas[self.vista_actual].get_observable()
        except SyntaxError:
            messagebox.showerror(message='Errores de sintaxis en el autómata')
        else:
            correcto = self.controlador.simular_automata(s_init, observable,
                                                         simbolo, matriz,
                                                         self.vista_actual)
            if not correcto:
                messagebox.showerror(message='El autómata no es correcto')

    def comparar_automatas(self):
        """
        Transmite al controlador que ha sido pulsado el botón comparar si los
        dos autómatas de las vistas son correctos
        :return:
        """
        try:
            s_init = self.vistas[0].get_s_init()
            simbolo, matriz = self.vistas[0].get_transformacion()
            observable = self.vistas[0].get_observable()

            s_init_2 = self.vistas[1].get_s_init()
            simbolo_2, matriz_2 = self.vistas[1].get_transformacion()
            observable_2 = self.vistas[1].get_observable()
        except SyntaxError:
            messagebox.showerror(
                message='Errores de sintaxis en alguno de los autómatas')
        else:
            correcto = self.controlador.comparar_automatas(s_init, simbolo,
                                                           matriz, observable,
                                                           s_init_2, simbolo_2,
                                                           matriz_2,
                                                           observable_2)
            if not correcto:
                messagebox.showerror(
                    message='Los autómatas deben ser dos MOQFA correctos y tener el mismo alfabeto')

    def actualizar_automata(self, id_qfa, dim=None, tipo=None, s_init=None,
                            simbolo=None, transformacion=None,
                            observable=None, alfabeto=None):
        self.vistas[id_qfa].mostrar_automata(dim, tipo, s_init, simbolo,
                                             transformacion, observable,
                                             alfabeto)
