from sistema_operacional.fcfs import Fcfs

QUANTUM = 2 # unidades de tempo de cada fatia de cpu na politica de feedback (definido no enunciado)

class Feedback:
    """
    Fila de prontos dos processos de usuario: feedback com 3 niveis de prioridade.

    - processo novo entra em rq_1 (maior prioridade)
    - se esgota o quantum sem concluir a fase de cpu, e rebaixado para a fila
      seguinte (rq_1 -> rq_2 -> rq_3), permanecendo em rq_3 caso ja esteja nela
    - ao retornar de E/S, o processo volta para a fila em que estava (nivel_fila),
      preservando a prioridade conquistada
    """
    def __init__(self):
        self.rq_1 = Fcfs()
        self.rq_2 = Fcfs()
        self.rq_3 = Fcfs()
        self.filas = [self.rq_1, self.rq_2, self.rq_3]

    def vazia(self):
        return all(fila.lista is None for fila in self.filas)

    def insereNovo(self, processo):
        processo.nivel_fila = 1
        self.rq_1.put(processo)

    def reinsere(self, processo):
        self.filas[processo.nivel_fila - 1].put(processo)

    def rebaixa(self, processo):
        if processo.nivel_fila < len(self.filas):
            processo.nivel_fila += 1
        self.filas[processo.nivel_fila - 1].put(processo)

    def proximoProcesso(self):
        for fila in self.filas:
            processo = fila.get()
            if processo is not None:
                return processo
        return None

    def imprime(self):
        for i, fila in enumerate(self.filas, start=1):
            print(f"  rq_{i}:")
            fila.imprime()
