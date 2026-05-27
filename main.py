import time

from memoria_principal import MemoriaPrincipal
from cpu import Cpu
from processo import Processo
from escalonador_cp import Despachante
from escalonador_lp import EscalonadorLongoPrazo

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

def main():
    print("\n------------------SISTEMA INICIALIZA-----------------\n")
    memoria_ram = MemoriaPrincipal()
    print("Memória Ram foi instanciada.")
    cpu = Cpu()
    print("Cpu foi instanciada.")
    print()
    print("Leitura dos processos .txt...")
    p = read_processos("processos.txt")
    print("Os processos do arquivo de entrada foram lidos.")
    print()
    despachante = Despachante(memoria_ram)
    escalonador = EscalonadorLongoPrazo(memoria_ram, despachante)
    for processo_lido in p:
        escalonador.criaProcesso(processo_lido)
        print()
    print(f"Memória Ram: {memoria_ram.lista_memoria_livre}")
    print("\n==================FUNCIONAMENTO DO SISTEMA===============\n")
    while(despachante.fila is not None):
        processo_escalonado = despachante.escalona()
        if(processo_escalonado is None):
            break
        print(f"Fila atual:")
        despachante.imprime()
        print()
        while(processo_escalonado.fase_1>0):
            print(f"CPU está executando processo {processo_escalonado.ident}. Tempo estante de cpu: {processo_escalonado.fase_1}")
            cpu.executa(processo_escalonado)
        print()
if __name__ == "__main__":
    main()