from fcfs import Fcfs
from termcolor import cprint # para deixar o texto do terminal colorido

class Despachante:
    def __init__(self, memoria_principal):
        self.fila = None# escalonador de Longo Prazo
        self.memoria = memoria_principal

    
    def insereFila(self, processo):
        cprint(f"Processo {processo.ident} inserido na fila de prontos", "magenta")
        if(self.fila==None):
            self.fila = Fcfs()
        self.fila.put(processo)
    
    def escalona(self):
        p = self.fila.get()
        if(p is None): 
            return None
        cprint(f"Processo foi escalonado:  {p.ident}", "magenta")
        self.memoria.removeProcesso(p)
        return p
    
    def imprime(self):
        self.fila.imprime()
    