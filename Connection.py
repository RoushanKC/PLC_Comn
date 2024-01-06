import socket
import time
import collections
import struct
from PLC_Comn.Data_maps import type_dict ,offset_map ,format_map

class Packet:
    def __init__(self ,timestamp ,data):
        self.timestamp=timestamp
        self.data=data

class Connection(Packet):
    def __init__(self ,host ,port ,packet_size ,timeout ,refresh_rate):
        self.host=host
        self.port=port
        self.packet_size=packet_size
        self.timeout=timeout
        self.refresh_rate=refresh_rate
    
    def return_packet(Packet):
        return Packet
    
    def establish_connection(self):
        self.client=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        self.client.connect((self.host ,self.port))
        socket.setdefaulttimeout(self.timeout)
    
    def connection_handling(self):
        print("log connection timeout ,timestamp :" ,time.time())
        retry_interval=self.timeout
        while True:
            try:
                self.client.connect((self.host ,self.port))
                print("connection re-established")
                break
            except socket.error as e:
                print("connection failed: ",e)
                print("log required")
                time.sleep(retry_interval)
                retry_interval*=2
        
    def Alive_bit():
        pass
    
    def decode(packet):
        parsed_data={}
        data=packet.data
        for items in offset_map:
            addr=items["address"]
            name=items["name"]
            type=items["type"]
            offset_len=type_dict[type]
            format_char=format_map[type]
            temp_data=data[addr:addr+offset_len]
            value=struct.unpack(">"+format_char ,temp_data)[0]
            parsed_data[name]=value
        return parsed_data
 
    def receive(self):
        self.establish_connection()
        self.client.sendall(b'11')
        while True:
            try:
                data=self.client.recv(self.packet_size)
                if not data:
                    print("log function implementation!")
                else:
                    timestamp=time.time()
                    packet=Packet(timestamp ,data)
                    data_map=self.decode(packet)
                    notify(data_map)
            except socket.timeout:
                print("implement-log")
                self.connection_handling(self)
            time.sleep(self.refresh_rate)
                    

        
        
        
    
    