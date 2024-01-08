from dataclasses import dataclass

@dataclass
class Data_class:
    name1 : str = "abc"
    name2 : str = "abc"
    name3 : str = "abc"
    '''
    def __init__(self ,data_map:dict):
        super().__init__()
        for key ,value in data_map.items():
            setattr(self ,key ,value)
            '''
            
    def get_field(self ,name):
        try:
            field_value=getattr(self ,name)
            return name ,field_value
        except AttributeError:
            raise ValueError(f"field dosent_exist")
    
    def set_field(self ,name ,value):
        try:
            setattr(self ,name ,value)
            print(f"Field '{name}' updated to '{value}'")
        except AttributeError:
            raise ValueError(f"value not set or field dosen't exist")
    

  
class Events:
    name1='name1'
    name2='name2'
    name3='name3'
    
class communication_controller:
    def __init__(self):
        self.event_callbacks={}  #key=event ,value =list of callbacks
        
    def subscribe(self ,event ,callback): #this should maintain a collection which map a particular event to all callbacks from all controllers
        if event not in self.event_callbacks:
            self.event_callbacks[event]=[]
        self.event_callbacks[event].append(callback)
        
    def notify(self ,event ,data): # this is part of event manager which will have map of all controller.callbacks that have subscribed to particular event
        if event in self.event_callbacks:
            for callback in self.event_callbacks[event]:
                callback(event ,data)
    
    
class Controller_1():
    data_class=Data_class()
    def callbacks(self ,event ,data): #this should call set_field() with specific args
        if event==Events.name1:
            self.data_class.set_field('name1' ,data)
        if event==Events.name2:
            self.data_class.set_field('name2' ,data)
        if event==Events.name3:
            self.data_class.set_field('name3' ,data)
class Controller_2():
    data_class=Data_class()
    
    def callbacks(self ,event ,data): #this should call set_field() with specific args
        if event==Events.name1:
            self.data_class.set_field('name1' ,data)
        if event==Events.name2:
            self.data_class.set_field('name2' ,data)
        if event==Events.name3:
            self.data_class.set_field('name3' ,data)

if __name__=="__main__":
    com_ctrl=communication_controller()
    ctrl_1=Controller_1()
    ctrl_2=Controller_2()
    
    com_ctrl.subscribe(Events.name1 ,ctrl_1.callbacks)
    com_ctrl.subscribe(Events.name2 ,ctrl_2.callbacks)
    
    com_ctrl.notify(Events.name1 ,'roushan')
    com_ctrl.notify(Events.name2 ,'kumar')
    
    val=ctrl_1.data_class.get_field('name1')
    print(val)