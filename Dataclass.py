import datetime
from dataclasses import dataclass   #external dependency if <Py 3.6

#currently flexibleInt is not used but commented for reusebility
'''
class FlexibleInt:
    def __init__(self, value, byte_size=1):
        valid_sizes = (1, 2, 4)
        if byte_size not in valid_sizes:
            raise ValueError(f"Invalid byte size: {byte_size}. Must be one of {valid_sizes}")

        if not -2**(8*byte_size-1) <= value <= 2**(8*byte_size-1)-1:
            raise ValueError(f"Value does not fit in {byte_size} bytes")

        self.value = value
        self.byte_size = byte_size

    def to_bytes(self):
        return self.value.to_bytes(self.byte_size, byteorder='big', signed=True)

    def __int__(self):
        return self.value
'''

@dataclass
class Data_class:
    #data members as per sheet provided by SBI
    dTimestamp : datetime = 0
    xAlive : bool = False
    xRemote : bool = False
    xReserve1 :bool = False
    xReserve2 :bool = False
    xReserve3 :bool = False
    xReserve4 :bool = False
    xReserve5 :bool = False
    xReserve6 :bool = False
    xReserve7 :bool = False
    uiTelegramNo : int = 0
    uiReserve1 : int = 0
    rReserve2 : float = 0.0
    rReserve3 : float = 0.0
    rReserve4 : float = 0.0
    rReserve5 : float = 0.0
    rReserve6 : float = 0.0
    rReserve7 : float = 0.0
    xMessungEin : bool = False
    xRegelungEin : bool = False
    xQuerRegEin : bool = False
    xLaengsRegEin : bool = False
    xKalibrierungEin : bool = False
    xLinienmessungEin : bool = False
    xReserve1 : bool = False
    xReserve2 : bool = False
    xReserve3 : bool = False
    xAL_1 :bytearray = bytearray(2)
    xAL_2 : bytearray = bytearray(2)
    rAktPos_Sensor = float = 0.0
    xResetAlarm: bool = False
    xRolleWechseln: bool = False
    
    
    #private class variable
    _instance=None
   # _publish_all=True
    #constructor calling singleton
    @staticmethod
    def getInstance():
        if Data_class._instance==None:
            Data_class()
        return Data_class._instance
    
    def __init__(self):
        if Data_class._instance!=None:
            print("use getInstance method for initialization")
        else : Data_class._instance=self
    '''
    #memory allocater
    def __new__(cls):
        if(cls._instance is None):
            cls._instance=super(Data_class ,cls).__new__(cls)
        return cls._instance
    
    #object initialization while insuring it is singleton
    
    def __init__(self ,data_maps: dict = None):
        if data_maps is not None:    
            for key ,value in data_maps.items():
                setattr(self ,key ,value)
        # later we would like to do initialization where if the instance is called for the first time it will instansiate like this otherwise we would like to call a 1 args constructor inside a 2 args constructor where defalt values will be prev timestamp values of PLC.
    '''
    def __getattr__(self, name):
        return None
    # data class setter ,setattr method wraper class
    def set_value(self ,key ,value):
        if not hasattr(self ,key):
            print("inserted new data member :" ,key)
        setattr(self ,key ,value)
    
    # data class getter .getattr method wraper class
    def get_key_value(self ,key):
        value =getattr(self ,key)
        return key ,value

'''
    # this method will run on thread ,main method of data class that will publish data   
    def update(self ,key ,value ,event_manager):
        _key ,_value=self.get_key_value(key)
        if(_value !=value or self._publish_all==True):
            if self._publish_all==True:
                self._publish_all=False
            self.set_values(key ,value)
            event=key
            event_manager.publish(event ,(key ,value))
'''
    
        
            
    

