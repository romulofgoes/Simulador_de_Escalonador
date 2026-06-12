from termcolor import cprint # para deixar o texto do terminal colorido: yellow

class Processo: # O elemento principal
    """
    """
    def __init__(self, ident: int, de_usuario:bool, fase_1: int, interruption_time:int, fase_2: int, qtde_discos: int, memory_size: int): 
        """ precisa adicionar se quer disco e quantos """
        """
            recebe os atributos iniciais da leitura do "processos.txt"
            tem atributo prox para poder gerar uma lista
        """
        self.ident = int(ident)
        self.de_usuario = bool(int(de_usuario)) # False - tempo_real e True - de usuário ("0"/"1" viram string, bool("0") seria True)
        self.fase_1 = int(fase_1)
        self.interruption_time = int(interruption_time)
        self.fase_2 = int(fase_2)
        self.qtde_discos = qtde_discos
        self.memory_size = int(memory_size) # em Mbytes
        self.prox = None
        self.estado = "novo"
        self.nivel_fila = 1 # fila de feedback atual (1, 2 ou 3); só vale para processos de usuário

    def mudaEstado(self, novo_estado):
        """
            Imprime e registra a transição de estado do processo
        """
        cprint(f"Processo #{self.ident}: de {self.estado} para {novo_estado}", "yellow")
        self.estado = novo_estado

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
            
            
        
        