import queue
import threading
from Data_maps import send_offset_map
from Shared_data import Shared_data
from Dataclass import Data_class


class Event_manager:
    _instance=None
    _lock=threading.Lock()
    _publish_all=True
    _lock_sub=threading.Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance=super().__new__(cls)
            return cls._instance
    
    def __init__(self):
        self.event_callbacks={} #key=event ,value =list of callbacks
        self.coreEngine= Data_class.getInstance()
        self.sd=Shared_data.getInstance()
        

    
    def subscribe(self ,event ,callback):
        with self._lock_sub:
            if event not in self.event_callbacks:
                self.event_callbacks[event]=[]
            self.event_callbacks[event].append(callback)
    
    def unsubscribe(self ,event ,callback):
        if event in self.event_callbacks:
            self.event_callbacks[event].remove(callback)
            print(f"callback removed")
        if not self.event_callbacks[event]:
            del self.event_callbacks[event]
            print(f"event : {event} deleted")
    
    def publish(self ,event ,data):
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                callback(event ,data)
        else :
            print(f"cannot publish ,create event :{event} for the data ")
     
            
    #this method fetch dictionary from data_class as per offset provided.
    def fetch_DataClass(self ,offset_map):
        fetch_dict={}
        for item in offset_map:
            key=item["name"]
            if(key=="raktDicke_Pos"):
                break
            _key ,val=self.coreEngine.get_key_value(key)
            if val==None:
                continue
            fetch_dict[key]=val
        return fetch_dict
    
    #this should be used by entity who want to send data to PLC       
    def notify_send_queue(self ,data):
        self.send_queue.put(data)
            
    #this should be used by entity who want to send data to Frontend
    #def notify_update_queue(self ,data_map):
    #    self.update_queue.put(data_map)
    
    #this method send data to PLC ,it will check data in send_queue ,
    #wrap data as per current system state ,convert data to b stream and send it to PLC
    def send_dataPLC(self ,conn):
        while True:
            data=self.send_queue.get()
            if data:
                all_data=self.fetch_DataClass(send_offset_map)
                for key ,val in data.items():
                    all_data[key]=val
                b_stream=conn.encode(all_data)
                conn.client.sendall(b_stream)
                    
    #event manager loop ,publish data with enabled delta encoding.   
    def em_loop(self):
        #shared_data=Shared_data()
        while True:
            data_map=self.sd.fetch_queue()
            print(data_map)
            for key ,value in data_map.items():
                if(key=="rAktDicke_Bolzen"):
                    data={key ,value}
                    self.publish(key ,data)
                    print(data)
                elif(key=="raktDicke_Pos"):
                    data={key ,value}
                    self.publish(key ,data)
                else:
                    _key ,_val=self.coreEngine.get_key_value(key)
                    if (self._publish_all==True or value!=_val or _val==None):
                        self.coreEngine.set_value(key ,value)
                        data={key ,value}
                        self.publish(key ,data)
            self._publish_all=False
                        
                    
    
    #method to put em_loop if thread and start it on thread.
    def start_em_thread(self):
        print("asd")
        self.em_thread=threading.Thread(target=self.em_loop)
        self.em_thread.start()
    
    #method to put send_dataPLC on thread.
    def start_send_dataPLC(self):
        self.send_dataPLC_thread=threading.Thread(target=self.send_dataPLC)
        self.send_dataPLC_thread.start()
        
        
            
        


