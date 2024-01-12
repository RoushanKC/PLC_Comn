import queue
import threading
from Dataclass import Data_class
from Connection import Connection
from Data_maps import send_offset_map


class Event_manager:
    _instance=None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance=super(Event_manager ,cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.event_callbacks={} #key=event ,value =list of callbacks

    
    def subscribe(self ,event ,callback):
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
    def fetch_DataClass(offset_map):
        fetch_dict={}
        dataclass=Data_class.getInstance()
        for item in offset_map:
            key=item["name"]
            _key ,val=dataclass.get_key_value(key)
            fetch_dict[key]=val
        return fetch_dict
    
    #this should be used by entity who want to send data to PLC       
    def notify_send_queue(self ,data):
        self.send_queue.put(data)
            
    #this should be used by entity who want to send data to Frontend
    def notify_update_queue(self ,data_map):
        self.update_queue.put(data_map)
    
    #this method send data to PLC ,it will check data in send_queue ,
    #wrap data as per current system state ,convert data to b stream and send it to PLC
    def send_dataPLC(self):
        while True:
            data=self.send_queue.get()
            if data:
                all_data=self.fetch_DataClass(send_offset_map)
                for key ,val in data.items():
                    all_data[key]=val
                b_stream=Connection.encode(all_data)
                Connection.client.sendall(b_stream)
                    
    #event manager loop ,publish data with enabled delta encoding.   
    def em_loop(self):
        while True:
            data_class=Data_class.getInstance()
            data_map=self.update_queue.get()
            for key ,value in data_map.items():
                data_class.update(key ,value ,self)
    
    #method to put em_loop if thread and start it on thread.
    def start_em_thread(self):
        self.em_thread=threading.Thread(target=self.em_loop)
        self.em_thread.start()
    
    #method to put send_dataPLC on thread.
    def start_send_dataPLC(self):
        self.send_dataPLC_thread=threading.Thread(target=self.send_dataPLC)
        self.send_dataPLC_thread.start()
        
            
        


