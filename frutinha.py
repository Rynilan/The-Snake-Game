from tkinter import Canvas
from random import random


class Frutinha:
    tela: Canvas
    fruta: tuple[int, int] = (0, 0)

    def __init__(self: object, tela: Canvas) -> None:
        self.tela = tela

    def criar_fruta(self: object, cobra: tuple[int]) -> None:
        self.fruta = (10 + int(random() * 50) * 10,
                      60 + int(random() * 30) * 10)
        while self.fruta in cobra:
            print('ai dento')
            self.fruta = (10 + int(random() * 50) * 10,
                          10 + int(random() * 30) * 10)

    def testar_colisao(self: object, coordenadas: tuple[int, int]) -> bool:
        return bool(self.fruta[1] == coordenadas[1] and
                    self.fruta[0] == coordenadas[0])

    def por_fruta(self: object) -> None:
        self.tela.create_text(self.fruta, text='🍎')
