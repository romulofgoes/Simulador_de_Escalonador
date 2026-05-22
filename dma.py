class Dma:
    """
    Classe que agrega os dispositivos de entrada e saída.
    Administra o sinal de interrupção para enviar ao processador
    Administra chamada do processo para buscar o dispositivo requisitado

            *** Acredito que aqui também pode ficar a liberação e, talvez, a entrada de processo na fila de bloqueados.
    """
    def __init__(self, disp_ent_sai, cpu):
        for disp in disp_ent_sai:
            self.disp = disp # Lista de dispositivos no hardware
        if(self.disp is None): 
            self.disp = None
        self.cpu = cpu # agrega a cpu, talvez deva ser uma lista com as 4 cpu's
    
    def buscaDisp(self, nome):
        for disp in self.disp:
            if(nome==disp.nome):
                return disp


    def sinalInterrupcao(self, nome):
        disp = self.buscaDisp(nome)
        disp.finaliza()
        self.cpu.interrupcao()
