import Connection
#import Dataclass
#import Event_manager
import threading
import time
import queue
from Shared_data import Shared_data
from Event_manager import Event_manager
import concurrent.futures

class Controller:
    
    def callback(self ,event ,data):
        if event=="rAktDicke_Bolzen":
            print(data)

    
if __name__=='__main__':
    host='192.168.0.52'
    port=2000
    conn=Connection.Connection(host ,port ,5740 ,2,1)
    em=Event_manager()
    ctr1=Controller()
    sd=Shared_data.getInstance()
    em.subscribe("rAktDicke_Bolzen" ,ctr1.callback)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(conn.receive)
        ex.submit(em.em_loop)
    
    
   
    #core_engine=Dataclass.Data_class.getInstance()
    #em=Event_manager.Event_manager(core_engine ,conn ,sh)
    #print(em.coreEngine)
    #
    
    
    