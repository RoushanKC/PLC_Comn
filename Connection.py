import socket
import time
import collections

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
        client=socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        socket.setdefaulttimeout(self.timeout)
        return client
    
    def connection_handling():
        pass
    
    def on_timeout():
        pass
    
    def receive(self ,conn):
        client=conn.establish_connection()
        data=client.recv(self.packet_size)
        timestamp=time.time()
        packet=Packet(timestamp ,data)
        
        
        
    
    