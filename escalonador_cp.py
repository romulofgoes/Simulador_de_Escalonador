from fcfs import Fcfs
from feedback import Feedback, QUANTUM
from termcolor import cprint # para deixar o texto do terminal colorido: magenta

class Despachante:
    def __init__(self, memoria_principal):
        self.fila_tempo_real = Fcfs() # processos de prioridade 0: FCFS, sem preempcao
        self.fila_usuario = Feedback() # processos de prioridade 1: feedback com 3 niveis
        self.memoria = memoria_principal

    def insereFila(self, processo):
        processo.mudaEstado("pronto")
        if processo.de_usuario:
            cprint(f"Despachante: Processo {processo.ident} inserido na fila de prontos de usuario (rq_1)", "magenta")
            self.fila_usuario.insereNovo(processo)
        else:
            cprint(f"Despachante: Processo {processo.ident} inserido na fila de prontos de tempo real", "magenta")
            self.fila_tempo_real.put(processo)

    def haProcessosProntos(self):
        return self.fila_tempo_real.lista is not None or not self.fila_usuario.vazia()

    def escalona(self):
        """
        Processos de tempo real tem prioridade absoluta sobre os de usuario.
        Retorna a tupla (processo, eh_tempo_real) ou (None, None) se nao ha ninguem pronto.
        """
        p = self.fila_tempo_real.get()
        if p is not None:
            cprint(f"Despachante: processo de tempo real {p.ident} escalonado (FCFS, executa ate a conclusao sem interrupcao)", "magenta")
            return p, True

        p = self.fila_usuario.proximoProcesso()
        if p is not None:
            cprint(f"Despachante: processo de usuario {p.ident} escalonado (rq_{p.nivel_fila}, quantum {QUANTUM} u.t.)", "magenta")
            return p, False

        return None, None

    def devolveDeIO(self, processo):
        self.fila_usuario.insereNovo(processo)

    def rebaixaProcesso(self, processo):
        self.fila_usuario.rebaixa(processo)

    def finalizaProcesso(self, processo):
        """
        So libera a memoria principal quando o processo de fato termina,
        nao no momento em que e escalonado para a cpu.
        """
        processo.mudaEstado("terminado")
        self.memoria.removeProcesso(processo)

    def imprime(self):
        print("Fila de tempo real (FCFS):")
        self.fila_tempo_real.imprime()
        print("Fila de usuario (feedback):")
        self.fila_usuario.imprime()
