from memoria_principal import MemoriaPrincipal
from escalonador_cp import Despachante
from fcfs import Fcfs

class EscalonadorLongoPrazo:
    def __init__(self, memoria_principal, despachante):
        self.memoria = memoria_principal
        self.despachante = despachante

    def criaProcesso(self, processo):
        print("Escalonador: Processo está sendo carregado na memória RAM")
        if(self.memoria.recebeProcesso(processo)):
            print("Escalonador: Processo está sendo inserido na fila de prontos do Despachante")
            self.despachante.insereFila(processo)
    
    

    

        
