class MemoriaPrincipal:
    def __init__(self):
        #memoria começa com um bloco único de 32GB (32768 MB) totalmente livre
        #cada partição vai guardar onde começa, o tamanho, se está livre e quem está usando

        self.particoes = [{
            'inicio': 0,
            'tamanho': 32768, 
            'livre': True,
            'id_processo': None
        }]
    
    def recebeProcesso(self, processo):
        """
        aqui eu tento carregar o processo na memória usando First-Fit, e retorno True se conseguiu alocar, ou False se não coube.
        """
        print(f"Tentando alocar {processo.memory_size} MB para o Processo {processo.ident}...")
        
        for i, bloco in enumerate(self.particoes):
            #procura o primeiro bloco que esteja livre e seja grande o suficiente
            if bloco['livre'] and bloco['tamanho'] >= processo.memory_size:
                sobra = bloco['tamanho'] - processo.memory_size
                
                #bloco atual passa a ser do processo
                bloco['livre'] = False
                bloco['id_processo'] = processo.ident
                bloco['tamanho'] = processo.memory_size
                
                #se sobrou espaço no bloco original, criamos uma nova partição livre com o resto
                if sobra > 0:
                    nova_particao = {
                        'inicio': bloco['inicio'] + processo.memory_size,
                        'tamanho': sobra,
                        'livre': True,
                        'id_processo': None
                    }
                    #insere o novo bloco vazio logo após o bloco que foi ocupado
                    self.particoes.insert(i + 1, nova_particao)
                
                print(f"Sucesso! Processo {processo.ident} carregado na RAM.")
                self.imprimeMapa()
                return True
                
        print(f"Falha: Memoria insuficiente ou muito fragmentada para o Processo {processo.ident}.") 
        """
        não sei se precisa de algoritmo pra lidar com fragmentações distantes entre si, é mt mais trabalhoso. Vou fazer um algoritmo de coalescência 
        pra juntar blocos livres adjacentes, mas se tiver muitos blocos pequenos livres separados, 
        não tem muito o que fazer além de esperar eles serem alocados ou desalocados pra tentar juntar eles.
        """
        
        return False

    def removeProcesso(self, processo):
        """
        Desaloca o processo e junta blocos livres vizinhos.
        """
        for i, bloco in enumerate(self.particoes):
            if not bloco['livre'] and bloco['id_processo'] == processo.ident:
                bloco['livre'] = True
                bloco['id_processo'] = None
                print(f"Processo {processo.ident} desalocado. Liberando {bloco['tamanho']} MB.")
                
                #após liberar, precisamos juntar os espaços vizinhos
                self._coalescencia() #fazer!
                self.imprimeMapa()
                return True
        return False

    #fazer função de coalescência para juntar blocos livres adjacentes
    def _coalescencia(self):
        """
        método interno para desfragmentação.
        Une partições livres adjacentes em uma só. necessário pra não ter muitos blocos pequenos livres 
        que não conseguem alocar processos maiores.
        """
        i = 0
        while i < len(self.particoes) - 1:
            bloco_atual = self.particoes[i]
            proximo_bloco = self.particoes[i + 1]
            
            #se o bloco atual e o bloco da frente estão livres, então juntamos eles
            if bloco_atual['livre'] and proximo_bloco['livre']:
                bloco_atual['tamanho'] += proximo_bloco['tamanho']
                #remove o próximo bloco da lista, pois ele foi juntado com o atual
                self.particoes.pop(i + 1)
                #!!!!!!!!!!!!!!!!!!!!IMPORTANTE: Não incrementamo o 'i' aqui, pois precisamos verificar se o NOVO próximo bloco (alo rodinei) também é livre para continuar juntando.
            else:
                i += 1 #agora sim

    def imprimeMapa(self):
        """
        imprimi um mapa aq pra saber o que está acontecendo.
        """
        mapa = []
        for p in self.particoes:
            status = "Livre" if p['livre'] else f"P{p['id_processo']}"
            mapa.append(f"[{status}: {p['tamanho']}MB]")
        print("Mapa da Memoria: " + " -> ".join(mapa))