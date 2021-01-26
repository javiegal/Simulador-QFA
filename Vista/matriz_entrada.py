import tkinter as tk
from sympy.parsing.sympy_parser import parse_expr
from sympy.matrices import Matrix


class MatrizEntrada(tk.Frame):
    """
    Frame para introducir una matriz
    """
    def __init__(self, master, num_filas, num_cols, matriz, state='normal'):
        super().__init__(master)

        self.state = state
        self.elementos_matriz = []
        self.num_filas = num_filas
        self.num_cols = num_cols
        # identidad = np.eye(dim, dtype=complex)
        for i in range(num_filas):
            fila = []
            for j in range(num_cols):
                e = tk.Entry(self)
                e.grid(row=i, column=j, sticky='nsew')
                e.insert(0, matriz[i, j])
                e.config(state=state)
                fila.append(e)
            self.elementos_matriz.append(fila)
            self.grid_rowconfigure(i, weight=1)
        for j in range(num_cols):
            self.grid_columnconfigure(j, weight=1)

    def set_matriz(self, matriz):
        """
        Rellena las matriz con aquella que se le ha pasado como parámetro
        :param matriz:
        :return:
        """
        for i in range(self.num_filas):
            for j in range(self.num_cols):
                self.elementos_matriz[i][j].delete(0, 'end')
                self.elementos_matriz[i][j].insert(0, matriz[i, j])

    def get_matriz_ev(self):
        """
        Devuelve la matriz parseada
        :return:
        """
        try:
            lista_filas = []
            for i in range(self.num_filas):
                fila = []
                for j in range(self.num_cols):
                    fila.append(parse_expr(self.elementos_matriz[i][j].get()))
                lista_filas.append(fila)
            return Matrix(lista_filas)
        except SyntaxError as e:
            raise e

    def set_state(self, state):
        """
        Habilita o deshabilita las entradas de la matriz
        :param state:
        :return:
        """
        self.state = state
        for i in range(self.num_filas):
            for j in range(self.num_cols):
                self.elementos_matriz[i][j].config(state=state)

    def get_state(self):
        return self.state
