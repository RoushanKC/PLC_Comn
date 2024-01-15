import queue
import threading

class Shared_data:
    _instance=None
    _lock=threading.Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance=super().__new__(cls)
            return cls._instance
    
    def __init__(self):
        self.shared_queue=queue.Queue()
    
    @classmethod
    def getInstance(cls):
        return cls()
   
    def notify_queue(self ,data):
        self.shared_queue.put(data)
            

        