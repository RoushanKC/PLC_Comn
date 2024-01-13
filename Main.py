import Connection
import Dataclass
import Event_manager
import Data_maps
import threading
from Shared_data import Shared_data

def console_data(q):
    print(q)
    
if __name__=='__main__':
    host='192.168.0.52'
    port=2000
    sh=Shared_data()
    conn=Connection.Connection(host ,port ,5740 ,2,1,sh)
    thread1=threading.Thread(target=conn.receive())
    thread1.start()
    while True:
        q=sh.update_queue.get()
        console_data(q)
    
    
    
    