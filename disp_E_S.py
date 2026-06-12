from processo import Processo
from termcolor import cprint # cor "white" destaque "on_blue"

# recurso de chamada do processo (se for mais de um, talvez seja preciso especificar na entrada do processo qual dispositivo ele requisita)
class dispositivoEntradaSaida:
    def __init__(self, nome, dma):
        self.nome = nome
        self.processo = None # processo no dispositivo
        self.ocupado = False # tipo um semáforo binário
        self.dma = dma
    
    def chamada(self, processo): # quando é chamado: recebe processo e passa a ficar ocupado
        self.processo = processo
        self.ocupado = True
    
    def finaliza(self): # quando finaliza: perde o processo e fica desocupado
        self.processo = None
        self.ocupado = False
    
    def executa(self):
        if(self.processo.executaInterrupcao()):
            cprint(f"Disp {self.nome} executando processo {self.processo.ident}", "white", "on_blue") # executa um ciclo de interrupção
        else:
            cprint(f"Disp {self.nome} terminou a chamada do processo {self.processo.ident}", "white", "on_blue") # conclui e envia sinal de interrupcao
            self.dma.sinalInterrupcao(self.nome) # sinal de interrupção
