from fcfs import Fcfs

class FilaBloqueados(Fcfs):
    """
    A princípio é na verdade uma lista cuja implementação envolve busca e remoção pq o processo sai quando o seu sinal de interrupção chega
    """
    def __init__(self, lista):
        super().__init__(lista)