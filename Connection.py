import socket
import time
#import collections
import struct
#import queue
from Data_maps import type_dict ,receive_offset_map ,send_offset_map,format_map ,format_map_pack
from Event_manager import Event_manager

# this is our abstraction of data buffer
class Packet:
    def __init__(self ,timestamp ,data):
        self.timestamp=timestamp
        self.data=data

# this class communicate with plc controller
class Connection(Packet):
    #instantiation of connection class
    def __init__(self ,host ,port ,packet_size ,timeout ,refresh_rate ,event_manager):
        self.host=host
        self.port=port
        self.packet_size=packet_size
        self.timeout=timeout
        self.refresh_rate=refresh_rate
        self.event_manager=event_manager
    
    # returns the packet
    def return_packet(Packet):
        return Packet
    
    #establish a socket
    def establish_connection(self):
        self.client=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        self.client.connect((self.host ,self.port))
        socket.setdefaulttimeout(self.timeout)
    
    # handling of socket in case of failures
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
    
    #alive bit implementation is pending ,need to toggle and keep track
    def Alive_bit():
        pass
    
    #decoder decode the data buffer recieved from plc and return decoded data
    def decode(packet):
        parsed_data={}
        data=packet.data
        for items in receive_offset_map:
            addr=items["address"]
            name=items["name"]
            type=items["type"]
            offset_len=type_dict[type]
            format_char=format_map[type]
            temp_data=data[addr:addr+offset_len]
            value=struct.unpack(">"+format_char ,temp_data)[0]
            parsed_data[name]=value
        parsed_data['dTimestamp']=packet.timestamp
        return parsed_data
    
    def encode(data):
        #make data map for send packet
        #iterate data_map to pack data into b stream
        #return b stream
        byte_ar=b""
        for item in receive_offset_map:
            name=item["name"]
            value=data[name]
            type_str=item["type"]
            format_spec=format_map_pack[type_str]
            byte_ar+=struct.pack(format_spec ,value)
            
        return byte_ar
    
    # establish connection ,recieve data then decode it then notify to data class   
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
                    #data_class=Data_classes.Data_class(data_map)
                    #log
                    print(data_map)
                    em=Event_manager()
                    em.notify_update_queue(data_map) #this is a callback to singleton Data_class class
            except socket.timeout:
                print("implement-log")
                self.connection_handling(self)
            time.sleep(self.refresh_rate)
            
#create function to run both receive and send on two different threads.

                    

        
        
        
    
    