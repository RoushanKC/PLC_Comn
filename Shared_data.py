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
        self.shared_queue=queue.Queue(maxsize=3)
    
    @classmethod
    def getInstance(cls):
        return cls()
   
    def notify_queue(self ,data):
        self.shared_queue.put(data ,block=True)
        print(self.shared_queue.qsize())
        
    def fetch_queue(self):
        data=self.shared_queue.get(block=True)
        print(self.shared_queue.qsize())
        return data
            

        