from controlador import Controlador
from modelo.modelo import Modelo
from vista.ui import UI


def main():
    num_automatas = 2
    modelo = Modelo(num_automatas)
    ui = UI(num_automatas)
    controlador = Controlador(modelo, ui)
    ui.set_controlador(controlador)
    ui.mainloop()


if __name__ == '__main__':
    main()
