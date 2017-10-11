import socket
import urllib
import sys,re
import user,get_data
from thread import *
global auth_key
auth_key='Zzb7flWH2Ucblx8Ok5QqbkfzUKEyffRh'
HOST = 'localhost'   
PORT = 8809
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
s.listen(10)
print 'Socket now listening'
 
def clientthread(conn):
    global auth_key
    if True:
        reqs=['create_user','user',]
        data = conn.recv(4096)
        d=str(data.split('\n')[0]).split()[1][2:].split('&')
        reply = 'Something went wrong!'
        try:
            if ('create_user' in d[0]) and ('notes' in d[1]) and (d[2].split('=')[-1]==auth_key):
                user.add_user(d[0].split('=')[-1],d[1].split('=')[-1])
                reply = 'User %s added successfully!'%(d[0].split('=')[-1])
            elif ('add_user_keyword' in d[0]) and ('keyword' in d[1]) and (d[2].split('=')[-1]==auth_key):
                arg1,arg2= d[0].split('=')[-1],d[1].split('=')[-1]
                arg2=urllib.unquote(urllib.unquote(arg2))
                user.add_user_keyword(arg1,arg2)
                reply = 'Keyword added successfully!'
            elif ('user' in d[0]) and ('msg' in d[1]) and (d[2].split('=')[-1]==auth_key):
                arg1,arg2= d[0].split('=')[-1],d[1].split('=')[-1]
                arg2=urllib.unquote(urllib.unquote(arg2))
                get_data.add_data(arg1,arg2)
                reply = get_data.add_data(arg1,arg2)
            elif ('user' in d[0]) and ('accuracy' in d[1]) and (d[2].split('=')[-1]==auth_key):
                arg1,arg2= d[0].split('=')[-1],d[1].split('=')[-1]
                if arg2=='good':
                    get_data.dead_user(arg1)
                reply = 'feedback received!'
            elif ('user' in d[0]) and ('graph' in d[1]) and (d[2].split('=')[-1]==auth_key):
                arg1,arg2= d[0].split('=')[-1],d[1].split('=')[-1]
                reply = get_data.get_graph(arg1)          
        except Exception as e:
            print e
            reply = 'Something went wrong!k'
        
        conn.sendall(reply)
        conn.close()
 
while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    start_new_thread(clientthread ,(conn,))
 
s.close()
