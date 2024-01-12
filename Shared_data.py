import queue

class Shared_data:
    _instance=None
    def __new__(cls):
        if not cls._instance:
            cls._instance=super().__new__(cls)
            cls._instance.update_queue=queue.Queue()
        return cls._instance
    
    def notify_update_queue(self ,data_map):
        self.update_queue.put(data_map)
        