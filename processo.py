class Processo:
    def __init__(self, ident: int,  fase_1: int, cpu_time:int, fase_2: int, memory_size: int):
        self.ident = ident
        self.fase_1 = fase_1
        self.cpu_time = cpu_time
        self.fase_2 = fase_2
        self.memory_size = memory_size
        self.prox = None