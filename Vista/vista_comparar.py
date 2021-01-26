import tkinter as tk
from tkinter import ttk


class VistaComparar(tk.Frame):
    """
    Frame que permite comparar dos autómatas computando secuencias de inputs de hasta la longitud introducida
    """

    def __init__(self, master, controlador):
        super().__init__(master)

        self.alfabeto = []
        self.controlador = controlador

        boton_atras = tk.Button(self, text='<', command=self.master.mostrar_inicio)
        boton_atras.grid(row=0, column=0, padx=5, pady=5, sticky='nsw')

        frame_comb = tk.LabelFrame(self, text='Ejecutar secuencias de inputs')
        var = tk.StringVar(frame_comb)
        var.set('3')
        self.tam_spinbox = tk.Spinbox(frame_comb, from_=2, to=15, justify='right', textvariable=var, width=3)
        comb_button = tk.Button(frame_comb, text='Ejecutar', command=self.ejecutar_comparacion)
        comb_label = tk.Label(frame_comb, text='Tamaño máximo:')

        self.tam_spinbox.grid(row=0, column=1)
        comb_button.grid(row=0, column=2, padx=5, pady=5)
        comb_label.grid(row=0, column=0, padx=5)

        frame_comb.grid(row=0, column=1, pady=5, padx=5, sticky='nsew')

        frame_resultados = tk.Frame(self)
        scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical")
        self.tabla = ttk.Treeview(frame_resultados, columns=('qfa1', 'qfa2', 'comp'), selectmode='none',
                                  yscrollcommand=scrollbar.set, height=25)
        scrollbar.config(command=self.tabla.yview)

        self.tabla.heading("#0", text="Secuencia de inputs", anchor='w')
        self.tabla.heading("qfa1", text="Probabilidad autómata 1")
        self.tabla.column('qfa1', anchor='center', width=150)
        self.tabla.heading("qfa2", text="Probabilidad autómata 2")
        self.tabla.column('qfa2', anchor='center', width=150)
        self.tabla.heading("comp", text="Iguales")
        self.tabla.column('comp', anchor='center', width=100)

        self.tabla.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        frame_resultados.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        frame_resultados.columnconfigure(0, weight=1)
        frame_resultados.rowconfigure(0, weight=1)

        self.label_conformidad = tk.Label(self, text='Autómatas relacionados: ')
        self.label_conformidad.grid(row=2, column=0, columnspan=2, padx=5, sticky='w')

        self.grid_columnconfigure(1, weight=1)

    def set_controlador(self, controlador):
        self.controlador = controlador

    def borrar_informacion(self):
        """
        Borra la información que haya escrita en la tabla
        :return:
        """
        self.tabla.delete(*self.tabla.get_children())
        self.label_conformidad.configure(text='')

    def mostrar_comparacion(self, comparacion):
        """
        Muestra los resultados recibidos de la comparación
        :param comparacion:
        :return:
        """
        self.borrar_informacion()
        conforme = True
        for k, v in comparacion.items():
            self.tabla.insert('', 'end', text=k, values=(f'{float(v[0]): .2f}', f'{float(v[1]): .2f}', v[2]))
            conforme &= v[2]
        self.label_conformidad.configure(text='Autómatas relacionados: ' + str(conforme))

    def ejecutar_comparacion(self):
        """
        Llama al modelo para realizar la comparación entre los autómatas
        :return:
        """
        tam = int(self.tam_spinbox.get())
        self.mostrar_comparacion(self.controlador.ejecutar_comparacion(tam))
