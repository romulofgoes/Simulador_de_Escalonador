from memoria_principal import MemoriaPrincipal
from escalonador_cp import Despachante
from fcfs import Fcfs
from termcolor import cprint # para deixar o texto do terminal colorido: cyan
import time # tempo de espera para melhor vizualização interativa

class EscalonadorLongoPrazo:
    def __init__(self, memoria_principal, despachante):
        self.memoria = memoria_principal
        self.despachante = despachante

    def criaProcesso(self, processo):
        tipo = "usuário" if processo.de_usuario else "tempo real"
        cprint(f"Escalonador: Processo {processo.ident} ({tipo}) criado, sendo carregado na memória RAM", "cyan")
        time.sleep(2)
        if(self.memoria.recebeProcesso(processo)):
            cprint(f"Escalonador: Processo {processo.ident} carregado na RAM, sendo inserido na fila de prontos do Despachante", "cyan")
            self.despachante.insereFila(processo)
        else:
            cprint(f"Escalonador: Processo {processo.ident} não coube na memória disponível e foi descartado", "cyan")
    
    

    

        
