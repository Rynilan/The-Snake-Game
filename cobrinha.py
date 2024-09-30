from tkinter import Frame, Canvas, Button
from frutinha import Frutinha


class Cobrinha:
    frame: Frame
    canvas: Canvas
    botoes: tuple[Button]
    fruta: Frutinha
    placar: int = 0
    maior: int = 0
    comando_dir = None
    comando_esq = None
    comando_fre = None
    comando_fic = None
    pontos: tuple[tuple[int]] = (
        (250, 140),
        (250, 150),
        (250, 160)
    )

    def __init__(self: object, frame: Frame, pai: object) -> None:
        self.frame = frame
        self.canvas = Canvas(frame, bg="#ffffff", width=510, height=310)
        self.fruta = Frutinha(self.canvas)
        self.__pai = pai

    def mexer(self: object, direcao: str) -> None:
        if direcao not in ('esq', 'dir', 'fre'):
            return
        pontos = self.pontos
        delta: int = (pontos[0][0] - pontos[1][0], pontos[0][1] - pontos[1][1])
        novos_pontos: list[tuple[int, int]] = [pontos[0]]
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
                0 in self.pontos[0] or
                510 in self.pontos[0] or
                310 == self.pontos[0][1]):
            return True
        else:
            return not True  # Why not use not to make what the not does? :)

    def morrer(self: object) -> None:
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
        self.frame.master.unbind("<KP_Up>")
        self.frame.master.unbind("<KP_Right>")
        self.frame.master.unbind("<KP_Left>")
        self.__pai.recomecar()
        self.pontos = (
            (250, 140),
            (250, 150),
            (250, 160)
        )

    def iniciar(self: object) -> None:
        self.fruta.criar_fruta(self.pontos)
        botoes = list()
        master = Frame(self.frame.master, bg="#8f8f8f")
        master.pack()
        if self.comando_fic is None:
            self.comando_dir = lambda: self.desenhar('dir')
            self.comando_esq = lambda: self.desenhar('esq')
            self.comando_fre = lambda: self.desenhar('fre')
            self.comando_fic = lambda: self.desenhar('fic')
            botoes.append(Button(master,
                                 text="←",
                                 command=self.comando_esq))
            botoes.append(Button(master,
                                 text="↑",
                                 command=self.comando_fre))
            botoes.append(Button(master,
                                 text="→",
                                 command=self.comando_dir))
            botoes.append(Button(master,
                                 text="↓",
                                 state='disabled',
                                 command=self.comando_fic))
            botoes[0].grid(row=1, column=0)
            botoes[1].grid(row=0, column=1)
            botoes[2].grid(row=1, column=2)
            botoes[3].grid(row=1, column=1)
        self.frame.master.bind("<KP_Up>", lambda evento: self.comando_fre())
        self.frame.master.bind("<KP_Right>", lambda evento: self.comando_dir())
        self.frame.master.bind("<KP_Left>", lambda evento: self.comando_esq())
        self.botoes = botoes
        self.desenhar()

    def desenhar(self: object, direcao: str = '') -> None:
        canvas: Canvas = self.canvas
        self.mexer(direcao)
        canvas.delete("all")
        canvas.create_rectangle(0, 0, 512, 312,
                                outline="#b22222",
                                fill="",
                                width=10)
        canvas.create_text(250, 150, text=str(self.placar),
                           font=('Monospace', '100'),
                           fill='#dddddd')
        self.fruta.por_fruta()
        canvas.create_line(self.pontos,
                           arrow='first',
                           width=5,
                           arrowshape=(6, 6, 1),
                           capstyle='round',
                           fill="#00aa40")
        canvas.pack()
        if self.verificar_colisoes():
            self.morrer()
