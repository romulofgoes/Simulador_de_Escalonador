from hardware.memoria_principal import MemoriaPrincipal
from sistema_operacional.escalonador_cp import Despachante
from sistema_operacional.fcfs import Fcfs
from termcolor import cprint # para deixar o texto do terminal colorido: cyan
import time # tempo de espera para melhor vizualização interativa

class EscalonadorLongoPrazo:
    def __init__(self, memoria_principal, despachante):
        self.memoria = memoria_principal
        self.despachante = despachante
        self.ordem_proc_pedidos = [] # lista de id's dos processos em disco ordenados por momento em que houve sua requisição

    def criaProcesso(self, processo, dma):
        tipo = "usuário" if processo.de_usuario else "tempo real"
        cprint(f"Escalonador: Processo {processo.ident} ({tipo}) criado, sendo carregado na memória RAM", "cyan")
        time.sleep(2)
        if(self.memoria.recebeProcesso(processo)):
            cprint(f"Escalonador: Processo {processo.ident} carregado na RAM, sendo inserido na fila de prontos do Despachante", "cyan")
            self.despachante.insereFila(processo)
        else:
            dma.disp[0].insere(processo)
            self.ordem_proc_pedidos.append(processo.ident)
            cprint(f"Escalonador: Processo {processo.ident} não coube na memória disponível e foi armazenado em {dma.disp[0].id}", "cyan")

    def escalonaProcesso(self, dma):
        if(len(self.ordem_proc_pedidos)>0) :
            processo = dma.disp[0].busca(self.ordem_proc_pedidos[0])
            if self.memoria.recebeProcesso(processo):
                cprint(f"Escalonador: Processo {processo.ident} carregado na RAM, sendo inserido na fila de prontos do Despachante", "cyan")
                self.ordem_proc_pedidos = self.ordem_proc_pedidos[1:]
                self.despachante.insereFila(processo)
            else: 
                cprint(f"Escalonador: Processo {processo.ident} não coube na memória disponível e continua armazenado em {dma.disp[0].id}", "cyan")
        else:
            cprint("Escalonador: Não há processos requisitados em Disco", "cyan")    
    

    

        
