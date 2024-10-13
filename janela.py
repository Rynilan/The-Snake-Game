from tkinter import Tk, Label, Button, Frame, mainloop
from cobrinha import Cobrinha


class Janela:

    master: Tk
    titulo: Label
    sair: Button
    animation: Frame
    animar: Button
    cobrinha: Cobrinha

    def __init__(self: object, master: Tk) -> None:
        master["bg"] = "#333c63"
        master.bind("<Escape>", lambda evento: self.kill())
        self.titulo = Label(master,
                            bg="#333c63",
                            fg='#b4c0db',
                            text="🐍 Jogo da cobrinha 🐍",
                            font=("Monospace", "20"))
        self.titulo.pack(side="top",
                         fill="x")
        self.sair = Button(master,
                           bg="#b4c0db",
                           fg='#0b4342',
                           text="sair",
                           font=("Monospace", "20"),
                           command=master.destroy)
        self.sair.pack(side="bottom",
                       fill="x")
        self.animation = Frame(master,
                               bg="#333c63")
        self.animation.pack(fill="both")
        self.cobrinha = Cobrinha(self.animation, self)
        self.animar = Button(self.animation,
                             bg="#b4c0db",
                             fg="#0b4342",
                             text="iniciar",
                             font=("Monospace", "20"),
                             command=self.iniciar_animacao)
        self.animar.pack(side="top", expand=True)
        mainloop()

    def kill(self: object) -> None:
        exit(0)
        self.master.destroy()

    def iniciar_animacao(self: object) -> None:
        self.animar.pack_forget()
        self.cobrinha.iniciar()

    def recomecar(self: object) -> None:
        self.animar['text'] = 'Recomeçar'
        self.animar.pack()
