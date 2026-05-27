from fcfs import Fcfs

class Despachante:
    def __init__(self, memoria_principal):
        self.fila = None# escalonador de Longo Prazo
        self.memoria = memoria_principal

    
    def insereFila(self, processo):
        print(f"Processo {processo.ident} inserido na fila de prontos")
        if(self.fila==None):
            self.fila = Fcfs()
        self.fila.put(processo)
    
    def escalona(self):
        p = self.fila.get()
        if(p is None): 
            return None
        print("Processo foi escalonado:  ", p.ident)
        self.memoria.removeProcesso(p)
        return p
    
    def imprime(self):
        self.fila.imprime()
    