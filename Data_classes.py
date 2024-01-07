from dataclasses import dataclass ,field

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


@dataclass(frozen=True)
class Data_class:
    xAlive : bool = False
    xRemote : bool = False
    xReserve1 :bool = False
    xReserve2 :bool = False
    xReserve3 :bool = False
    xReserve4 :bool = False
    xReserve5 :bool = False
    xReserve6 :bool = False
    xReserve7 :bool = False
    uiTelegramNo : FlexibleInt = FlexibleInt(2)
    uiReserve1 : FlexibleInt = FlexibleInt(2)
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
    rAktPos_Sensor = float =0.0
     
    def __init__(self ,data_maps: dict):
        super().__init__()
        for key ,value in data_maps.items():
            setattr(self ,key ,value)
        # later we would like to do initialization where if the instance is called for the first time it will instansiate like this otherwise we would like to call a 1 args constructor inside a 2 args constructor where defalt values will be prev timestamp values of PLC.
    
    

