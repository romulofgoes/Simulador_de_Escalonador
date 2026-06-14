class Dma:
    """
    Classe que agrega os dispositivos de entrada e saída.
    Administra o sinal de interrupção para enviar ao processador
    Administra chamada do processo para buscar o dispositivo requisitado

            *** Acredito que aqui também pode ficar a liberação e, talvez, a entrada de processo na fila de bloqueados.
    """
    def __init__(self, disp_ent_sai, cpu):
        self.disp = disp_ent_sai # Lista de dispositivos no hardware
        self.cpu = cpu # agrega a cpu, talvez deva ser uma lista com as 4 cpu's
        self.lista_ocupados = [] # lista com ["id do processo", [disp_1 ..., disp_n]] por elemento da lista
    
    def buscaDisp(self, nome):
        for disp in self.disp:
            if(nome==disp.nome):
                return disp

    def buscaDispLivre(self):
        disp_livres = []
        for disp in self.disp:
            if not disp.ocupado:
                disp_livres.append(disp)
        return disp_livres

    def estaAlocado(self, processo):
        return any(disp.processo is processo for disp in self.disp)

    def sinalInterrupcao(self, nome):
        disp = self.buscaDisp(nome)
        disp.finaliza()
        self.cpu.interrupcao()

    def chamada(self, processo):
        if self.estaAlocado(processo):
            return False
        disp_livres = self.buscaDispLivre()
        if len(disp_livres) >= processo.qtde_discos:
            disp_ocupados = []
            for i, disp in enumerate(disp_livres):
                if(i>=processo.qtde_discos): 
                    break
                disp.chamada(processo)
                disp_ocupados.append(disp)
            self.lista_ocupados.append([processo, disp_ocupados])
            return True
        return False
        



