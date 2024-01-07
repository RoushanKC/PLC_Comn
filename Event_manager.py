class Event_manager:
    def __init__(self):
        self.subscribers=[]
    
    def subscribe(self ,subscriber):
        self.subscribers.append(subscriber)
    
    def unsubscribe(self ,subscriber):
        self.subscribers.remove(subscriber)
    
    def notify(self ,event ,data_class):
        for subscriber in self.subscribers:
            subscriber.update(event ,data_class)


