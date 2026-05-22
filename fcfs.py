from processo import Processo

class Fcfs:
    def __init__(self, lista: Processo):
        self.lista = lista

    def get(self):
        if(not self.lista):
            return None
        processo_escalonado = self.lista
        self.lista = self.lista.prox
        return processo_escalonado
        

    def put(self, processo_carregado):
        if(not self.lista): 
            self.lista = processo_carregado
            return
        processo_prox = self.lista
        while(processo_prox.prox):
            processo_prox = processo_prox.prox
        processo_prox.prox = processo_carregado
    

        
            
        
    