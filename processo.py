class Processo:
    def __init__(self, ident: int, de_usuario:bool, fase_1: int, interruption_time:int, fase_2: int, memory_size: int):
        self.ident = ident
        self.de_usuario = de_usuario # False - tempo_real e True - de usuário
        self.fase_1 = fase_1
        self.interruption_time = interruption_time
        self.fase_2 = fase_2
        self.memory_size = memory_size
        self.prox = None

    def executaCiclo(self):
        if(self.fase_1>0):
            self.fase_1-=1
        else:
            self.fase_2-=1

    def foiInterrompido(self):
        if(self.fase<0):
            print ("Error na interrupção!")
            return 0
        if(self.fase_1==0 and self.interruption_time>0):
            return True
        return False
    
    def foiFinalizado(self):
        if((self.fase_1 + self.fase_2)==0):
            return True
        return False
    

    def executaInterrupcao(self):
        if(self.interruption_time>0):
            self.interruption_time-=1
            return True
        return False
            
            
        
        