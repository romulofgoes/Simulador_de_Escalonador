class Processo: # O elemento principal
    """ 
    """
    def __init__(self, ident: int, de_usuario:bool, fase_1: int, interruption_time:int, fase_2: int, memory_size: int):
        """
            recebe os atributos iniciais da leitura do "processos.txt"
            tem atributo prox para poder gerar uma lista
        """
        self.ident = int(ident)
        self.de_usuario = bool(de_usuario) # False - tempo_real e True - de usuário
        self.fase_1 = int(fase_1)
        self.interruption_time = int(interruption_time)
        self.fase_2 = int(fase_2)
        self.memory_size = int(memory_size) # em Mbytes
        self.prox = None

    def executaCiclo(self):
        """
            Faz a decrementação de unidade de tempo da fase_1 primeiro e depois da fase_2 
        """
        if(self.fase_1>0):
            self.fase_1-=1
        else:
            self.fase_2-=1

    def foiInterrompido(self):
        """
            Método que retorna True se o processo requisita interrupção e False, se não
        """
        if(self.fase_1<0):
            print ("Error na interrupção!")
            return 0
        if(self.fase_1==0 and self.interruption_time>0):
            return True
        return False
    
    def foiFinalizado(self):
        """
            Método que retorna True se não há mais necessidade de CPU
        """
        if((self.fase_1 + self.fase_2)==0):
            return True
        return False
    

    def executaInterrupcao(self):
        """
            retorna True se ainda está no dispositivo, False se não
            Decrementa a interrupão em 1 unidade.
        """
        if(self.interruption_time>0):
            self.interruption_time-=1
            return True
        return False
            
            
        
        