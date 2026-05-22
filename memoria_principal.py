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
    def __init__(self):
        self.lista_memoria_livre = None