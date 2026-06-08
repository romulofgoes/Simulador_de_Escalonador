# Simulador de Escalonador de Processos

Trabalho prático de Sistemas Operacionais: simulação de um sistema com 4 CPUs,
4 discos e 32 GiB de memória principal, que escalona processos de tempo real
e de usuário.

## Requisitos

- Python 3.12+
- [termcolor](https://pypi.org/project/termcolor/) (`pip install termcolor`)

## Como rodar

```
python main.py
```

A simulação lê `processos.txt`, carrega os processos na memória e mostra,
em tempo real no terminal, cada mudança de estado, escalonamento, ciclo de
CPU e operação de E/S, com cores diferentes por componente do sistema.

## Entrada (`processos.txt`)

Cada linha descreve um processo:

```
<id>, <de_usuario>, <duração da fase 1 de CPU>, <duração de I/O>, <duração da fase 2 de CPU>, <MB de RAM>
```

- `de_usuario`: `0` para processo de tempo real (prioridade 0), `1` para processo de usuário (prioridade 1)
- Um processo sem fase 2 e sem I/O (campos zerados) é CPU-bound
- Processos de tempo real não usam I/O e não podem exigir mais que 512 MiB de RAM

Exemplo:

```
7, 1, 4, 2, 4, 800
12, 1, 10, 4, 8, 1200
5, 0, 15, 0, 0, 512
```

## Políticas de escalonamento

- **Tempo real (prioridade 0)**: fila FCFS, executa até a conclusão sem
  interrupção e tem prioridade absoluta sobre processos de usuário.
- **Usuário (prioridade 1)**: feedback com 3 filas (`rq_1` a `rq_3`) e
  quantum de 2 unidades de tempo. Um processo entra em `rq_1`; se esgota o
  quantum sem terminar a fase de CPU, é rebaixado uma fila (até `rq_3`, onde
  permanece). Ao retornar de uma operação de E/S, volta para a fila em que
  estava.

## Memória principal

Gerenciada por partições dinâmicas com alocação *first-fit* e coalescência
de blocos livres adjacentes (`memoria_principal.py`). O espaço de um
processo só é liberado quando ele termina sua execução.

## Estrutura do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| `main.py` | Inicializa o sistema e orquestra o ciclo de simulação |
| `processo.py` | Modelo do processo (fases de CPU/I-O, estados, transições) |
| `escalonador_lp.py` | Escalonador de longo prazo: cria processos e os carrega na memória |
| `escalonador_cp.py` | Despachante (escalonador de curto prazo): seleciona o próximo processo a executar |
| `fcfs.py` | Fila FCFS usada pelos processos de tempo real |
| `feedback.py` | Fila de feedback com 3 níveis usada pelos processos de usuário |
| `cpu.py` | Execução de um ciclo de CPU e tratamento de interrupções |
| `disp_E_S.py` / `dma.py` | Dispositivos de E/S (discos) e DMA, que sinalizam o fim de uma operação |
| `fila_de_bloqueados.py` | Fila dos processos aguardando ou em E/S |
| `memoria_principal.py` | Gerenciamento da memória principal (partições, alocação, liberação) |
