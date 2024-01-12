import Connection
import Dataclass
import Event_manager
import Data_maps
import threading


if __name__=='__main__':
    
    thread1=threading.Thread(target=Connection.receive())
    thread1.start()
    
    
    
    