
 
import sys, socket, select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009
MAPPING = {}
alamat = {}
def chat_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    SOCKET_LIST.append(server_socket)
 
    print "Chat server mulai pada port " + str(PORT)
 
    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      		
        for sock in ready_to_read:
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) terhubung" % addr
                #broadcast(server_socket, sockfd, "\r[%s:%s] memasuki chatting room kami\n" % addr)
            else:
                
                try:
		        data = sock.recv(RECV_BUFFER)
		        if data:
			   global MAPPING
			   global alamat
			   ji = data.split()
			   if ji[2] =="sendto" :
				test =False
				for key,value in MAPPING.iteritems():
					if value == sock :
						test=True
				if test==True :
					sendto(ji[3],ji)
				
			   elif ji[2] =="list" :
				test =False
				for key,value in MAPPING.iteritems():
					if value == sock :
						test=True
				if test==True :
					daftar(sock,server_socket)
				
				
			   elif ji[2]=="sendall" :
				datajadian = "\r" + ji[0] + " says "
				count = 0
				while count !=len(ji):
					if count >2:
						datajadian += (ji[count]+" ")
					count+=1
				datajadian += "\n"
				test =False
				for key,value in MAPPING.iteritems():
					if value == sock :
						test=True
				if test==True :
					broadcast(server_socket, sock, datajadian)
				
			   elif (ji[0]==ji[2]):
				login(sock,ji[0],server_socket,addr)
			   elif ji[2]=="login" :
				login(sock,ji[3],server_socket,addr)
			   else:
				sock.send("\rinvalid command\n")
		        else:          
		           if sock in SOCKET_LIST:
		                SOCKET_LIST.remove(sock)
			   simpan = MAPPING[sock]     
		           broadcast(server_socket, sock, "\rClient (%s) off\n" % simpan) 
 
                except:
		    
		    for key,value in alamat.iteritems() :
			if value == addr:
                    		broadcast(server_socket, sock, "\r(%s) off\n"%key )
                    continue

    server_socket.close()

def daftar(sock1,server_socket):
	data ="\rlist yang online\n"	
	for socket in SOCKET_LIST :
		for key,value in MAPPING.iteritems():
			if socket == value :
				data+=(key + " is online \n")
	try:	
		sock1.send(data)
	except:
		socket.close()
		if socket in SOCKET_LIST :
			SOCKET_LIST.remove(socket)
	
def sendto(destination,message):
	data = "\r"+message[0] + " says "
	count = 0 
	while count!=len(message):
		if count>3 :
			data+=(message[count]+" ")
		count +=1	
	data += "\n"
	socket = MAPPING[destination]
	try :
		socket.send(data)
	except :
		socket.close()
		if socket in SOCKET_LIST :
			SOCKET_LIST.remove(socket)
def login(sock,name,server_socket,addr):
	test =True
	for key,value in MAPPING.iteritems():
		if key == name :
			test=False
	if(test==False):
		sock.send("\rusername sudah dipake\n")
	else :
		MAPPING[name]=sock
		alamat[name]=addr
		broadcast1(sock,server_socket,name)			
def broadcast (server_socket, sock, message):
    
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)	
def broadcast1 (sock,server_socket,name):
   	broadcast(server_socket,sock,"\r%s sudah terhubung dengan system \n"%name)
 
if __name__ == "__main__":

    sys.exit(chat_server())
