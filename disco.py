from disp_E_S import dispositivoEntradaSaida
from processo import Processo
from copy import deepcopy

class Disco(dispositivoEntradaSaida):
    def __init__(self, id, nome, dma, storage=524288):
        super().__init__(nome, dma)
        self.id = id
        self.storage_size = storage # 512 GB ou 1/2 TB
        self.fila_processos = []

    def busca(self, processo_id):
        for p in self.fila_processos:
            if p.ident == processo_id:
                return p
        return None
    
    def insere(self, processo):
        if self.storage_size>processo.memory_size:
            if not self.busca(processo.ident):
                self.fila_processos.append(deepcopy(processo))
                self.storage_size-=processo.memory_size
                print(f"Disco {self.id}: Espaço restante: {self.storage_size} MB")
            else:
                for i, p in enumerate(self.fila_processos):
                    if p.ident == processo.ident:
                        self.fila_processos[i] = deepcopy(processo)
                        print(f"Processo {p.ident} atualizado no Disco {self.id}")
                        break
            return True
        print(f'Disco lotado!!! Processo {processo.ident} não pode ser armazenado no Disco {self.id}')
        return False

    def apaga(self, processo):
        p = self.busca(processo.ident)
        if p:
            for p in self.fila_processos:
                    if p.ident == processo.ident:
                        print(f"Processo {p.ident} agora é espaço livre")
                        self.fila_processos.remove(p)
                    break
        else:
            print(f"Processo {processo.ident} não está armazenado no Disco {self.id}")    
        
            


        
