from processo import Processo
import time

class Cpu: #processador - serão 4 instâncias (?)
    def __init__(self):
        self.sinalInterrupcao=False # sinal de interrupção - para política de feedback que para o processo para ver o sinal de interrupção
    
    def interrupcao(self): # recebeu sinal de interrupção
        self.sinalInterrupcao = True

    def executa(self, processo): # essa função executa - decrementa fase_1 ou fase_2 do processo
        if(not processo.foiFinalizado() and not processo.foiInterrompido()): # para quando processo é interrompido ou finalizado
            processo.executaCiclo()
        
        else:
            if(processo.foiInterrompido()):
                print("Processo foi interrompido!")
            print("Processo finalizou.")

    def lidaComInterrupcao(self): # confirma o tratamento do sinal e o reseta antes de voltar a executar
        self.sinalInterrupcao = False

