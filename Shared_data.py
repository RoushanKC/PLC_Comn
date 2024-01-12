import queue

class Shared_data:
    def __init__(self):
        self.update_queue=queue.Queue()  #queue for sending data to frontend
        self.send_queue=queue.Queue(maxsize=1) #queue for sending to PLC