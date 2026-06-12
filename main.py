import time

from memoria_principal import MemoriaPrincipal
from cpu import Cpu
from processo import Processo
from escalonador_cp import Despachante
from escalonador_lp import EscalonadorLongoPrazo
from disco import Disco
from dma import Dma
from fila_de_bloqueados import FilaBloqueados
from feedback import QUANTUM

NUM_DISCOS = 4
TEMPO_DE_CICLO = 1 # segundos de pausa por unidade de tempo simulada, so para visualizacao


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


def executaTempoReal(cpu, despachante, dma, fila_bloqueados, processo):
    '''
        Tempo real e prioridade 0: roda em FCFS ate a conclusao, sem qualquer interrupcao
    '''
    processo.mudaEstado("executando")
    while not processo.foiFinalizado():
        avancaIO(cpu, dma, fila_bloqueados, despachante)
        print(f"CPU executando processo de tempo real {processo.ident} (sem interrupcao). Resta de fase 1: {processo.fase_1}")
        cpu.executa(processo)
        time.sleep(TEMPO_DE_CICLO)
    despachante.finalizaProcesso(processo)


def executaUsuario(cpu, despachante, dma, fila_bloqueados, processo):
    '''
        Usuario e prioridade 1: roda no maximo `QUANTUM` unidades de tempo por vez.
        Se terminar a fase de cpu, finaliza; se precisar de E/S, vai para a fila de
        bloqueados; se esgotar o quantum sem nenhum dos dois, e rebaixado de fila.
    '''
    processo.mudaEstado("executando")
    unidades_executadas = 0
    while True:
        if processo.foiFinalizado():
            despachante.finalizaProcesso(processo)
            return

        if processo.foiInterrompido():
            processo.mudaEstado("bloqueado")
            fila_bloqueados.put(processo)
            return

        if unidades_executadas == QUANTUM:
            processo.mudaEstado("pronto")
            despachante.rebaixaProcesso(processo)
            return

        print(f"CPU executando processo de usuario {processo.ident} (rq_{processo.nivel_fila}, {unidades_executadas + 1}/{QUANTUM} do quantum). Resta fase 1: {processo.fase_1}, fase 2: {processo.fase_2}")
        cpu.executa(processo)
        avancaIO(cpu, dma, fila_bloqueados, despachante)
        unidades_executadas += 1
        time.sleep(TEMPO_DE_CICLO)


def avancaIO(cpu, dma, fila_bloqueados, despachante):
    '''
        A cada ciclo do sistema: avanca um passo de E/S nos discos ocupados
        (devolvendo ao despachante quem terminou) e atribui discos livres aos
        processos que ainda aguardam na fila de bloqueados, em ordem de chegada.
    '''
    for disp in dma.disp:
        if disp.ocupado:
            processo_em_io = disp.processo
            disp.executa()
            if not disp.ocupado: # disp.executa() chamou dma.sinalInterrupcao, que ja sinalizou a cpu
                fila_bloqueados.remove(processo_em_io)
                processo_em_io.mudaEstado("pronto")
                despachante.devolveDeIO(processo_em_io)
                cpu.lidaComInterrupcao()

    aguardando = fila_bloqueados.lista
    while aguardando is not None:
        if not dma.estaAlocado(aguardando):
            disp_livre = dma.buscaDispLivre()
            if disp_livre is None:
                break
            disp_livre.chamada(aguardando)
        aguardando = aguardando.prox


def main():
    print()
    print("\n-----------------------------SISTEMA INICIALIZA-----------------------------\n")
    time.sleep(2)
    memoria_ram = MemoriaPrincipal()
    print("Memória RAM foi instanciada.")
    cpu = Cpu()
    print("CPU foi instanciada.")

    discos = [Disco(i, f"Disco {i + 1}", None) for i in range(NUM_DISCOS)]
    dma = Dma(discos, cpu)
    for disco in discos: # referencia circular: o disco precisa do dma para sinalizar e o dma precisa da lista de discos
        disco.dma = dma
    print(f"{NUM_DISCOS} discos e o DMA foram instanciados.")
    

    print("\nLeitura dos processos .txt...")
    p = read_processos("processos_gerados.txt")

    print("Os processos do arquivo de entrada foram lidos.\n")

    fila_bloqueados = FilaBloqueados()
    despachante = Despachante(memoria_ram)
    escalonador = EscalonadorLongoPrazo(memoria_ram, despachante)
  
    for processo_lido in p:
        time.sleep(1)
        escalonador.criaProcesso(processo_lido, dma)
        print()

    print("TESTE: ", escalonador.ordem_proc_pedidos)

    print("\n==================FUNCIONAMENTO DO SISTEMA===============\n")
    while despachante.haProcessosProntos() or fila_bloqueados.lista is not None:
        

        escalonador.escalonaProcesso(dma)
        processo_escalonado, eh_tempo_real = despachante.escalona()
        if processo_escalonado is None:
            despachante.imprime()
            time.sleep(TEMPO_DE_CICLO)
            continue

        print("Fila atual:")
        despachante.imprime()
        print()

        if eh_tempo_real:
            executaTempoReal(cpu, despachante, dma, fila_bloqueados, processo_escalonado)
        else:
            executaUsuario(cpu, despachante, dma, fila_bloqueados, processo_escalonado)
        print()

    print("\n------------------SISTEMA FINALIZADO-----------------\n")


if __name__ == "__main__":
    main()
