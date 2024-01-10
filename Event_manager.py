import queue
import threading
from Dataclass import Data_class


class Event_manager:
    _instance=None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance=super(Event_manager ,cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.event_callbacks={} #key=event ,value =list of callbacks
        self.update_queue=queue()
    
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
            

    def notify(self ,data_map):
        self.update_queue.put(data_map)
        
    def em_loop(self):
        while True:
            data_class=Data_class.getInstance()
            data_map=self.update_queue.get()
            for key ,value in data_map.items():
                data_class.update(key ,value ,self)
    
    def start_em_thread(self):
        self.em_thread=threading.Thread(target=self.em_loop)
        self.em_thread.start()
            
        


