import socket
import time
#import collections
import struct
#import queue
from Data_maps import type_dict ,receive_offset_map ,send_offset_map,format_map

# this is our abstraction of data buffer
class Packet:
    def __init__(self ,timestamp ,data):
        self.timestamp=timestamp
        self.data=data

# this class communicate with plc controller
class Connection(Packet):
    #instantiation of connection class
    def __init__(self ,host ,port ,packet_size ,timeout ,refresh_rate ,sh):
        self.host=host
        self.port=port
        self.packet_size=packet_size
        self.timeout=timeout
        self.refresh_rate=refresh_rate
        self.sh=sh
    
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
    def decode(self ,dataP):
        parsed_data={}
        packet=dataP.data
        parsed_data["dTimestamp"]=dataP.timestamp
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
    
    def encode(self ,data):
        #make data map for send packet
        #iterate data_map to pack data into b stream
        #return b stream
        byte_ar=b""
        for item in send_offset_map:
            name=item["name"]
            value=data[name]
            type_str=item["type"]
            format_spec=format_map[type_str]
            byte_ar+=struct.pack(format_spec ,value)
            
        return byte_ar
    
    # establish connection ,recieve data then decode it then notify to data class   
    def receive(self):
        self.establish_connection()
        self.client.sendall(b'11')
        while True:
            try:
                data=self.client.recv(self.packet_size)
                print(len(data))
                if not data:
                    print("log function implementation!")
                    self.client.close()
                else:
                    timestamp=time.time()
                    packet=Packet(timestamp ,data)
                    data_map=self.decode(packet)
                    #data_class=Data_classes.Data_class(data_map)
                    #log
                    print(data_map)
                    self.sh.notify_update_queue(data_map) #this is a callback to singleton Data_class class
            except socket.timeout:
                print("implement-log")
                self.connection_handling(self)
            time.sleep(self.refresh_rate)
            
#create function to run both receive and send on two different threads.

                    

        
        
        
    
    