from processo import Processo
import time

class cpu:
    def __init(self):
        self.sinalInterrupcao=False
    
    def interrupcao(self):
        self.sinalInterrupcao = True

    def executa(processo):
        if(not processo.foiFinalizado() and not processo.foiInterrompido):
            time.sleep(1)
            processo.executaCiclo()
        
        else:
            if(processo.foiInterrompido()):
                print("Processo foi interrompido!")
            print("Processo finalizou.")
    
    

