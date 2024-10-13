from tkinter import Frame, Canvas, Button
from frutinha import Frutinha
from threading import Thread
from time import sleep


class Cobrinha:
    frame: Frame = None
    canvas: Canvas = None
    botoes: tuple[Button] = None
    fruta: Frutinha = None
    placar: int = 0
    maior: int = 0
    comando_dir = None
    comando_esq = None
    comando_nad = None
    morto: bool = False
    proximo: str = 'fre'
    thread: Thread = None
    pontos: tuple[tuple[int]] = (
        (250, 140),
        (250, 150),
        (250, 160)
    )

    def __init__(self: object, frame: Frame, pai: object) -> None:
        self.frame = frame
        self.canvas = Canvas(frame,
                             bg="#9aca04",
                             width=510,
                             height=360,
                             )
        self.fruta = Frutinha(self.canvas)
        self.__pai = pai

    def set_proximo(self: object, proximo: str) -> None:
        self.proximo = proximo

    def ajustar_botoes(self: object, proximo: str) -> None:
        botoes = self.botoes
        comandos = [botao.cget('command') for botao in botoes]
        comandos.insert(0, comandos[-1])
        comandos.append(comandos[1])
        comandos = tuple(comandos)
        deslocamento = 1
        if proximo == 'dir':
            deslocamento += -1
        elif proximo == 'esq':
            deslocamento += +1
        for indice, botao in enumerate(botoes):
            pos = indice + deslocamento
            botao.config(command=comandos[pos])

    def mexer(self: object, direcao: str) -> None:
        if direcao not in ('esq', 'dir', 'fre'):
            return
        pontos = self.pontos
        delta: int = (pontos[0][0] - pontos[1][0], pontos[0][1] - pontos[1][1])
        novos_pontos: list[tuple[int, int]] = [pontos[0]]
        self.ajustar_botoes(direcao)
        if delta[0] != 0:
            dir: tuple[int, int] = (delta[1], delta[0])
            esq: tuple[int, int] = (delta[1], delta[0] * - 1)
        else:
            dir: tuple[int, int] = (delta[1] * - 1, delta[0])
            esq: tuple[int, int] = (delta[1], delta[0])
        match (direcao):
            case 'fre':
                mudanca: tuple[int, int] = delta
            case 'dir':
                mudanca: tuple[int, int] = dir
            case 'esq':
                mudanca: tuple[int, int] = esq
        for indice, par_ord in enumerate(pontos):
            if indice == 0:
                novos_pontos[0] = list(novos_pontos[0])
                novos_pontos[0][0] += mudanca[0]
                novos_pontos[0][1] += mudanca[1]
                novos_pontos[0] = tuple(novos_pontos[0])
                if self.fruta.testar_colisao(novos_pontos[-1]):
                    memoria = pontos[-1]
                    self.placar += 1
                    self.fruta.criar_fruta(pontos + tuple(novos_pontos))
                else:
                    memoria = None
            else:
                novos_pontos.append(pontos[indice - 1])
        if memoria is not None:
            novos_pontos.append(memoria)
        self.pontos = tuple(novos_pontos)

    def verificar_colisoes(self: object) -> None:
        if (self.pontos[0] in self.pontos[1:] or
                0 == self.pontos[0][0] or
                50 == self.pontos[0][1] or
                510 == self.pontos[0][0] or
                360 == self.pontos[0][1]):
            return True
        else:
            return not True  # Why not use not to make what the not does? :)

    def morrer(self: object) -> None:
        self.morto = True
        self.proximo = 'fre'
        for botao in self.botoes:
            botao.config(state='disabled')
        canvas = self.canvas
        if self.placar > self.maior:
            self.maior = self.placar
        canvas.create_rectangle(100, 100, 400, 200,
                                fill='#000000',
                                outline='#8f8f8f')
        canvas.create_text(250, 150, text='{}\n{}\n{}'.format(
            'Você perdeu! KKKK',
            'Pontuação: ' + str(self.placar),
            'Melhor: ' + str(self.maior)
        ),
                           font=('Monospace', '15'),
                           fill='#ffffff')
        self.placar = 0
        self.__pai.recomecar()
        self.pontos = (
            (250, 140),
            (250, 150),
            (250, 160)
        )

    def iniciar(self: object) -> None:
        self.fruta.criar_fruta(self.pontos)
        self.morto = False
        if self.comando_dir is None:
            botoes = list()
            master = Frame(self.frame.master, bg="#333c63")
            master.pack()
            self.comando_dir = lambda: self.set_proximo('dir')
            self.comando_esq = lambda: self.set_proximo('esq')
            self.comando_nad = lambda: self.set_proximo('fre')
            botoes.append(Button(master,
                                 text="←"))
            botoes.append(Button(master,
                                 text='↑'))
            botoes.append(Button(master,
                                 text="→"))
            botoes.append(Button(master,
                                 text='↓'))
            botoes[0].grid(row=1, column=0)
            botoes[1].grid(row=0, column=1)
            botoes[2].grid(row=1, column=2)
            botoes[3].grid(row=1, column=1)
            self.botoes = tuple(botoes)
        for botao in self.botoes:
            botao.config(
                       state='normal',
                       bg="#b4c0db",
                       fg='#0b4342')
        self.botoes[0].config(command=self.comando_esq)
        self.botoes[1].config(command=self.comando_nad)
        self.botoes[2].config(command=self.comando_dir)
        self.botoes[3].config(command=self.comando_nad)
        self.thread = Thread(target=self.framework)
        self.thread.daemon = True
        self.thread.start()

    def framework(self: object) -> None:
        while not self.morto:
            sleep(0.5)
            self.desenhar(self.proximo)
            self.proximo = 'fre'

    def desenhar(self: object, direcao: str = '') -> None:
        canvas: Canvas = self.canvas
        self.mexer(direcao)
        canvas.delete("all")
        canvas.create_rectangle(4, 50, 508, 358,
                                outline="#223e00",
                                fill="",
                                width=5)
        canvas.create_text(25, 22, text=str(self.placar),
                           font=('Monospace', '20'),
                           fill='#223e00')
        canvas.create_line(6, 40, 506, 40,
                           width=5,
                           fill='#223e00')
        self.fruta.por_fruta()
        canvas.create_line(self.pontos,
                           arrow='',
                           width=5,
                           arrowshape=(6, 6, 1),
                           capstyle='round',
                           fill="#223e00")
        canvas.pack(pady='10')
        if self.verificar_colisoes():
            self.morrer()
