import random

with open("processos.txt", "w") as f:
    id = 1
    x = int(input("Quantos processos?"))

    for _ in range(x):
        de_usuario = random.choice([0, 1])
        fase_1 = random.randrange(1, 10)
        qtde_discos = random.randrange(0, 4) if de_usuario else 0
        interruption_time = random.randrange(1, 10) if qtde_discos>0 else 0
        fase_2 = random.randrange(1, 10) if interruption_time>0 else 0
        memory_size = random.randrange(100, 10000)
        f.write(f"{id:04d}, {de_usuario}, {fase_1}, {interruption_time}, {fase_2}, {qtde_discos}, {memory_size}\n")
        id+=1