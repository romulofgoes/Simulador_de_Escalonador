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
TEMPO_DE_CICLO = 1.5 # segundos de pausa por unidade de tempo simulada, so para visualizacao


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


def executaTempoReal(cpu, despachante, processo):
    '''
        Tempo real e prioridade 0: roda em FCFS ate a conclusao, sem qualquer interrupcao
    '''
    processo.mudaEstado("executando")
    while not processo.foiFinalizado():
        print(f"CPU executando processo de tempo real {processo.ident} (sem interrupcao). Resta de fase 1: {processo.fase_1}")
        cpu.executa(processo)
        time.sleep(TEMPO_DE_CICLO)
    despachante.finalizaProcesso(processo)


def executaUsuario(cpu, despachante, fila_bloqueados, processo):
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
    print("\n------------------SISTEMA INICIALIZA-----------------\n")
    time.sleep(2)
    memoria_ram = MemoriaPrincipal()
    print("Memória Ram foi instanciada.")

    #mudança 1: crio 4 intancias da cpu original
    cpus = [Cpu() for _ in range(4)]
    print("As 4 CPUs foram instanciadas.")

    discos = [Disco(i, f"Disco {i + 1}", None) for i in range(NUM_DISCOS)]

    #passo somente apenas a primeira CPU pro DMA para não quebrar o __init__ (manter alterações só na main mesmo)
    dma = Dma(discos, cpus[0])
    for disco in discos: # referencia circular: o disco precisa do dma para sinalizar e o dma precisa da lista de discos
        disco.dma = dma
    fila_bloqueados = FilaBloqueados()
    print(f"{NUM_DISCOS} discos e o DMA foram instanciados.")

    print()
    print("Leitura dos processos .txt...")
    p = read_processos("processos.txt")
    print("Os processos do arquivo de entrada foram lidos.")
    print()

    despachante = Despachante(memoria_ram)
    escalonador = EscalonadorLongoPrazo(memoria_ram, despachante)
    for processo_lido in p:
        time.sleep(2)
        escalonador.criaProcesso(processo_lido, dma)
        print()

    print("\n==================FUNCIONAMENTO DO SISTEMA===============\n")


    #segunda mudança: array pra rastrear o que roda em cada cpu
    #estrutura: [processo_atual, eh_tempo_real, unidades_executadas_no_quantum]
    status_cpus = [[None, False, 0] for _ in range(4)]

    #sistema roda enquanto houver processos na fila ou alguma cpu estiver ocupada
    while despachante.haProcessosProntos() or fila_bloqueados.lista is not None or any(status[0] is not None for status in status_cpus):
        
        #deixei a chamada de IO passando a cpu[0] pra assinatura
        avancaIO(cpus[0], dma, fila_bloqueados, despachante)

        #escalona processos pelo Escalonador de Longo Prazo do Disco para a MP
        escalonador.escalonaProcesso(dma)

        #PRIMEIRO PASSO: preencher as cpus que estão vazias
        for i in range(4):
            if status_cpus[i][0] is None: # cpu vazia
                processo, eh_tr = despachante.escalona()
                if processo is not None:
                    processo.mudaEstado("executando")
                    status_cpus[i] = [processo, eh_tr, 0] # preenche cpu com processo e info de tempo real + quantum

        #SEGUNDO PASSO: executar um ciclo em todas as cpus ocupadas simultaneamente
        for i in range(4):
            processo, eh_tr, qtd = status_cpus[i]
            if processo is not None:
                cpus[i].executa(processo)
                status_cpus[i][2] += 1 #incrementa unidades executadas no quantum
                time.sleep(TEMPO_DE_CICLO)
                tipo = "Tempo Real" if eh_tr else f"Usuario (rq_{processo.nivel_fila})"
                print(f"CPU {i+1} executando P{processo.ident} [{tipo}] -> Fase 1: {processo.fase_1} | Fase 2: {processo.fase_2}")
        
        time.sleep(TEMPO_DE_CICLO)
        print("-" * 50) #linha p separar os ciclos no terminal

        #TERCEIRO PASSO: verificar o que aconteceu com cada processo apos rodarem o ciclo
        for i in range(4):
            processo, eh_tr, qtd = status_cpus[i]
            if processo is not None:
                #processo terminou?
                if processo.foiFinalizado():
                    despachante.finalizaProcesso(processo)
                    status_cpus[i] = [None, False, 0] # libera cpu
                
                #processo precisa ir pro disco? E/S
                elif processo.foiInterrompido():
                    processo.mudaEstado("bloqueado")
                    fila_bloqueados.put(processo)
                    status_cpus[i] = [None, False, 0] # libera cpu
                
                #quantum esgotou para processo de usuario?
                elif not eh_tr and qtd >= QUANTUM:
                    processo.mudaEstado("pronto")
                    despachante.rebaixaProcesso(processo)
                    status_cpus[i] = [None, False, 0] # libera cpu

    print("\n------------------SISTEMA FINALIZADO-----------------\n")


if __name__ == "__main__":
    main()
