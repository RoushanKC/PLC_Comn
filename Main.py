import Connection
import Dataclass
import Event_manager
import Data_maps
import threading


if __name__=='__main__':
    host='192.168.0.52'
    port=2000
    em=Event_manager.Event_manager()
    conn=Connection.Connection(host ,port ,5740 ,2,1,em)
    thread1=threading.Thread(target=Connection.receive())
    thread1.start()
    
    
    
    