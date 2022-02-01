import tkinter as tk
from tkinter import ttk


class VistaSimular(tk.Frame):
    """
    Frame que permite simular un autómata introduciendo palabras y mostrando la
    probabilidad de aceptación de las mismas
    """

    def __init__(self, parent, controlador, id_qfa=0):
        super().__init__(parent)

        self.id_qfa = id_qfa
        self.controlador = controlador
        self.alfabeto = []

        self.boton_atras = tk.Button(self, text='<',
                                     command=self.master.mostrar_inicio)
        self.boton_atras.grid(row=0, column=0, padx=5, pady=5, sticky='nsw')

        frame_palabra = tk.LabelFrame(self, text='Ejecutar una palabra')
        palabra_label = tk.Label(frame_palabra, text='Introduce la palabra:')

        self.entry_palabra = tk.StringVar()
        self.entry_palabra.trace("w", self.limitar_entrada)
        entry = tk.Entry(frame_palabra, textvariable=self.entry_palabra)
        palabra_button = tk.Button(frame_palabra, text='Ejecutar',
                                   command=self.simular_palabra)
        self.alfabeto_label = tk.Label(frame_palabra, text='')

        palabra_label.grid(row=0, column=0, padx=5)
        entry.grid(row=0, column=1)
        palabra_button.grid(row=0, column=2, padx=5, pady=5)
        self.alfabeto_label.grid(row=0, column=3, padx=20)

        frame_comb = tk.LabelFrame(self, text='Ejecutar varias palabras')
        var = tk.StringVar(frame_comb)
        var.set('3')
        self.tam_spinbox = tk.Spinbox(frame_comb, from_=2, to=15,
                                      justify='right', textvariable=var,
                                      width=3)
        comb_button = tk.Button(frame_comb, text='Ejecutar',
                                command=self.simular_comb)
        comb_label = tk.Label(frame_comb, text='Tamaño máximo:')

        self.tam_spinbox.grid(row=0, column=1)
        comb_button.grid(row=0, column=2, padx=5, pady=5)
        comb_label.grid(row=0, column=0, padx=5)

        frame_text = tk.Frame(self)
        scrollbar = ttk.Scrollbar(frame_text, orient='vertical')
        self.text = tk.Text(frame_text, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)
        self.text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        frame_text.grid(row=2, column=0, columnspan=2, pady=5, padx=5,
                        sticky='nsew')
        frame_palabra.grid(row=0, column=1, pady=5, padx=5, sticky='nsew')
        frame_comb.grid(row=1, column=0, columnspan=2, pady=10, padx=5,
                        sticky='nsew')

        frame_text.grid_rowconfigure(0, weight=1)
        frame_text.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def set_controlador(self, controlador):
        self.controlador = controlador

    def set_alfabeto(self, alfabeto):
        """
        Muestra el alfabeto con el que se pueden construir las palabras que
        puede procesar el autómata
        :param alfabeto:
        :return:
        """
        self.alfabeto = alfabeto
        alfabeto_str = '{'
        for palabra in alfabeto:
            alfabeto_str += palabra + ', '
        alfabeto_str = alfabeto_str[:-2] + '}'
        self.alfabeto_label.configure(text='Alfabeto = ' + alfabeto_str)

    def set_id_qfa(self, id_qfa):
        self.id_qfa = id_qfa

    def simular_palabra(self):
        """
        Lee la palabra escrita y escribe la probabilidad de aceptación de la
        misma
        :return:
        """
        palabra = self.entry_palabra.get()
        probabilidad = self.controlador.simular_palabra(palabra, self.id_qfa)
        self.text.configure(state='normal')
        self.text.insert(
            'end',
            palabra +
            ', probabilidad de aceptación: ' +
            f'{float(probabilidad): .2f}' +
            '\n')
        self.text.configure(state='disabled')

    def simular_comb(self):
        """
        Lee todas las palabras hasta la longitud establecida y escribe las
        probabilidades de aceptación de cada una
        :return:
        """
        maximo = int(self.tam_spinbox.get())
        probabilidades = self.controlador.simular_combinaciones(maximo,
                                                                self.id_qfa)
        for k, v in probabilidades.items():
            self.text.configure(state='normal')
            self.text.insert(
                'end',
                k +
                ', probabilidad de aceptación: ' +
                f'{float(v): .2f}' +
                '\n')
            self.text.configure(state='disabled')

    def limitar_entrada(self, *args):
        """
        Impide escribir símbolos que no estén en el alfabeto
        :param args:
        :return:
        """
        palabra = self.entry_palabra.get()
        if len(palabra) > 0 and palabra[-1] not in self.alfabeto:
            self.entry_palabra.set(palabra[:-1])

    def borrar_info(self):
        """
        Borra la información que haya mostrada
        :return:
        """
        self.text.configure(state='normal')
        self.text.delete('1.0', 'end')
        self.text.configure(state='disabled')
        self.entry_palabra.set('')
