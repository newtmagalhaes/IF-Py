from threading import Thread
import time

class CPU_bound(Thread):
  def __init__(self, id:str, range:int):
    """
    Executa uma thread orientada a CPU
    """
    Thread.__init__(self)
    self.thread_id = id
    self.r = range
  
  def run(self):
    for i in range(self.r):
      start = time.perf_counter()
      counter = 0
      while time.perf_counter() - start < 1:
        counter += 1
      print(f'Thread CPU-Bound {self.thread_id} while executou {counter} vezes na iteração {i}')
    
    print(f'fim da thread {self.thread_id}')

if __name__ == '__main__':
  t1 = CPU_bound('1', 10)
  t2 = CPU_bound('2', 6)
  print('threads inicializadas')

  t1.start()
  t2.start()
  
  t1.join()
  t2.join()
  print('fim do programa')
  