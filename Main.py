import Connection
#import Dataclass
#import Event_manager
import threading
import time
import queue
from Shared_data import Shared_data

class Em:
    def __init__(self):
        self.s_data=Shared_data.getInstance()
    
    def publish(self):
        while True:
            try:
                data=self.s_data.shared_queue.get(block=True)
                print(data)
            except queue.Empty:
                time.sleep(0.5)
    def start_th(self):
        threading.Thread(target=self.publish()).start() 
    
if __name__=='__main__':
    host='192.168.0.52'
    port=2000
    conn=Connection.Connection(host ,port ,5740 ,2,1)
    em=Em()
    conn.th_start()
    em.start_th()
   
    #core_engine=Dataclass.Data_class.getInstance()
    #em=Event_manager.Event_manager(core_engine ,conn ,sh)
    #print(em.coreEngine)
    #
    
    
    