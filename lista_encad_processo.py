from processo import Processo

class ListaEncadProcesso:
    def __init__(self, lista: Processo):
        self.lista = lista

    def remove(self, processo_finalizado):
        processo_prox = self.lista
        processo_ant = None
        while(processo_prox or processo_prox != processo_finalizado):
            proceso_ant = processo_prox
            processo_prox = processo_prox.prox
        if(processo_ant):
            processo_ant.prox = processo_prox.prox
        else: 
            self.lista = processo_prox.prox
        processo_finalizado = None

    def push(self, processo_escalonado):
        self.lista
        
            
        
    