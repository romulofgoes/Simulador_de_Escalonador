from processo import Processo

class dispositivoEntradaSaida:
    def __init__(self, nome, dma):
        self.nome = nome
        self.processo = None
        self.ocupado = False
        self.dma = dma
    
    def chamada(self, processo):
        self.processo = processo
        self.ocupado = True
    
    def finaliza(self):
        self.processo = None
        self.ocupado = False
    
    def executa(self):
        if(self.processo.executaInterrupcao()):
            print("Disp {self.nome} entrada executando processo {self.processo.ident}")
        else:
            print("Disp {self.nome} terminou a chamada do processo {self.processo.ident}")
            self.dma.sinalInterrupcao(self.name)
