class Dma:
    def __init__(self, disp_ent, disp_sai, cpu):
        for disp in disp_ent:
            self.disp = disp
        for disp in disp_sai:
            self.disp = disp
        if(self.disp is None): 
            self.disp = None
        self.cpu = cpu
    
    def buscaDisp(self, nome):
        for disp in self.disp:
            if(nome==disp.nome):
                return disp


    def sinalInterrupcao(self, nome):
        disp = self.buscaDisp(nome)
        disp.finaliza()
        self.cpu.interrupcao()
