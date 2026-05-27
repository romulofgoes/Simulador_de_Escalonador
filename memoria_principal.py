class MemoriaPrincipal:

    """
    *** Dúvidas de implementação não definidas:
        - O processo tem sua imagem carregada aqui pelo 'escalonador_lp', mas e aí?
            -> entra processo 1: cria-se um nó do espaço vazio ou do espaço do processo??
            -> o que esse processo tem: todos os seus dados ou basta denotar o armazenamento?? 
            Ou seja, é uma lista de processos ou de endereços? 

        - E, depois de uma memória fragmentada, o que rola com os espaços vazios?
            -> pegaria o primeiro espaço livre que encaixa o processo?
            -> essa memória poderia ser atualizada para que ela voltasse a não ficar tão fragmentada?

    A cada processo finalizado é preciso atualizar a MP.
    
    """
    def __init__(self, memoria_livre: list=[[0, 32768]], size=1):
        self.lista_memoria_livre = memoria_livre
        self.size_lista = size
    
    def getInstance(self=None): #Padrão Singleton - para manter em uma só instância a memória
        if(self.lista_memoria_livre==None):
            memoria = MemoriaPrincipal([[0, 32768]]) # a memoria está vazia: endereços disponíveis de 0 a 2^10 Mbytes
        return memoria
    
    def recebeProcesso(self, processo): # carrega o processo na RAM e altera a lista de vazios
        print(f"Processo {processo.ident} sendo carregado na memória")
        for i in range(self.size_lista):
            t = self.lista_memoria_livre[i]
            if(t[1]-t[0]>processo.memory_size):
                print("Tamando memoria livre: ", self.lista_memoria_livre)
                t[0] = t[0] + processo.memory_size
                return True
        print("Memoria cheia!")
        return False
    
    def removeProcesso(self, processo): # retira o processo do parametro da memoria principal
        for t in self.lista_memoria_livre:
            t[1] -= processo.memory_size
            print(f"Processo {processo.ident} desalocado da memória!")
    
             
