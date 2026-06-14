from sistema_operacional.processo import Processo

def read_processos(endereco_nome: str):
    '''
        Ler o arquivo de processos
        Retorna lista de objetos instanciados com os dados do processos
    '''
    p = list()
    with open(endereco_nome) as f:
        for line in f:
            params = []
            for param in line.split(","): # pega os itens, cada um
                    params.append(param.strip()) # tira o espaço sobrando
            processo = Processo(*params) # cria novo processo com esses parâmetros
            p.append(processo)
    return p