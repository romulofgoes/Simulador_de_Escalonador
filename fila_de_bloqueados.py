from fcfs import Fcfs

class FilaBloqueados(Fcfs):
    """
    Fila dos processos em E/S (executando ou aguardando um disco livre).
    E uma FCFS comum, mas precisa de busca e remocao porque o processo sai
    da fila assim que seu sinal de interrupcao (fim de E/S) chega - nao
    necessariamente na ordem em que entrou.
    """
    def __init__(self):
        super().__init__()

    def remove(self, processo):
        anterior = None
        atual = self.lista
        while atual:
            if atual.ident == processo.ident:
                if anterior is None:
                    self.lista = atual.prox
                else:
                    anterior.prox = atual.prox
                atual.prox = None
                return atual
            anterior = atual
            atual = atual.prox
        return None
