import queue
import threading
import time
import socket
import struct
import concurrent.futures
from Data_maps import type_dict ,receive_offset_map ,format_map

class Shared_data:
    _instance=None
    _lock=threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance=super().__new__(cls)
            return cls._instance
    
    def __init__(self):
        self.shared_queue=queue.Queue(maxsize=5)
        
    @classmethod
    def getInstance(cls):
        return cls()
    
    def put_data(self ,data):
        print("put 1: ", self.shared_queue.qsize())
        self.shared_queue.put(data ,block=True)
        print("put 2: ", self.shared_queue.qsize())
    
    def get_data(self):
        print("get 1: ", self.shared_queue.qsize())
        data = self.shared_queue.get(block=True)
        print("get 2: ", self.shared_queue.qsize())
        return data
   
class Connection:
    _instance=None
    _lock=threading.Lock()
    
    def __new__(cls ,*args ,**kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance=super().__new__(cls)
            return cls._instance
    
    def __init__(self ,host ,port ,refresh_rate ,packet_size):
        self.s_data=Shared_data.getInstance()
        self.host=host
        self.port=port
        self.refresh_rate=refresh_rate
        self.packet_size=packet_size
        self.client=None
        
    def establish_connection(self):
        if self.client is None:
            self.client=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        self.client.connect((self.host ,self.port))
        socket.setdefaulttimeout(5)
        
    def connection_handling(self):
        pass
    
    #decoder decode the data buffer recieved from plc and return decoded data
    def decode(self ,dataP):
        parsed_data={}
        packet=dataP
        parsed_data["dTimestamp"]=time.time()
        for items in receive_offset_map:
            addr=items["address"]
            addr=int(addr/8)
            name=items["name"]
            typeF=items["type"]
            offset_len=type_dict[typeF]
            decode_format=format_map[typeF]
            if addr==0:
                #bit manup impl
                pass
            elif addr==30:
                #bit manup impl
                pass
            elif(addr==694):
                bolt_arr=[]
                for i in range(206):
                    bolt_addr=addr+(i*4)
                    tdata=packet[bolt_addr : bolt_addr+offset_len]
                    if(len(tdata)==offset_len):
                        value=struct.unpack(decode_format ,tdata)
                    bolt_arr.append(value)
                parsed_data[name]=bolt_arr
            elif(addr==1540):
                pos_arr=[]
                for i in range(1050):
                    pos_addr=addr+(i*4)
                    tdata=packet[pos_addr : pos_addr+offset_len]
                    if(len(tdata)==offset_len):
                        value=struct.unpack(decode_format ,tdata)
                    pos_arr.append(value)
                parsed_data[name]=pos_arr
            else:
                tdata=packet[addr : addr+offset_len]
                if(len(tdata)==offset_len):
                    value=struct.unpack(decode_format ,tdata)
                    parsed_data[name]=value
        return parsed_data
    
    def receive(self):
        self.establish_connection()
        self.client.sendall(b'11')
        while True:
            try:
                data=self.client.recv(self.packet_size)
                if not data:
                    print("closing connection")
                    self.client.close()
                else:
                    data_map=self.decode(data)
                    self.s_data.put_data(data_map)
            except socket.timeout:
                print("socket timeout ,closing connection")
                self.client.close()
                
    def start_th(self):
        threading.Thread(target=self.receive()).start()
                    
'''       
class Em:
    def __init__(self):
        self.s_data=Shared_data.getInstance()
    
    def publish(self):
        while True:
            try:
                data=self.s_data.get_data()
                print(data)
            except queue.Empty:
                pass
            time.sleep(1)
                
    def start_th(self):
        threading.Thread(target=self.publish()).start()
'''

class Event_manager:
    _instance=None
    _lock=threading.Lock()
    _publish_all=True
    _lock_sub=threading.Lock()
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance=super().__new__(cls)
            return cls._instance
    
    def __init__(self):
        self.event_callbacks={} #key=event ,value =list of callbacks
        #self.coreEngine= Data_class.getInstance()
        self.sd=Shared_data.getInstance()
        

    
    def subscribe(self ,event ,callback):
        with self._lock_sub:
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
            
    def em_loop(self):
        while True:
            data_map=self.sd.get_data()
            array_pos=data_map["raktDicke_Pos"]
            print(len(array_pos))
            self.publish("raktDicke_Pos" ,array_pos)
            
class Controller:
    
    def callback(self ,event ,data):
        if event=="raktDicke_Pos":
            print(data)
   

if __name__=='__main__':
    host='192.168.0.52'
    port=2000
    con=Connection(host ,port ,1 ,5740)
    em=Event_manager()
    #em.start_th()
    #con.start_th()
    ctrl=Controller()
    em.subscribe("raktDicke_Pos" ,ctrl.callback)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.submit(con.receive)
        ex.submit(em.em_loop)
    