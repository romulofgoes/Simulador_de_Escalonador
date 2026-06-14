from sistema_operacional.fcfs import Fcfs

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
    

    def avancaIO(self, cpu, dma, despachante):
        '''
            A cada ciclo do sistema: avanca um passo de E/S nos discos ocupados
            (devolvendo ao despachante quem terminou) e atribui discos livres aos
            processos que ainda aguardam na fila de bloqueados, em ordem de chegada.
        '''
        for disps in dma.lista_ocupados:
            processo_em_io = disps[0]
            for i, disp in enumerate(disps[1]):
                disp.executa()
                if not disp.ocupado: # disp.executa() chamou dma.sinalInterrupcao, que ja sinalizou a cpu
                    disps[1][i]=""
            if disps[1][0] == "":
                cpu.lidaComInterrupcao()
                self.remove(processo_em_io)
                processo_em_io.mudaEstado("pronto")
                despachante.devolveDeIO(processo_em_io)
                processo_em_io.interruption_time = 0
                disps[0] = ""
        dma.lista_ocupados = [x for x in dma.lista_ocupados if x[0]!= ""]
        aguardando = self.lista
        while aguardando is not None:
            if not dma.chamada(aguardando):
                break
            aguardando = aguardando.prox
