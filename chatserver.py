
 
import sys, socket, select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009
MAPPING = {}
DECODE ={}
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
                broadcast(server_socket, sockfd, "[%s:%s] memasuki chatting room kami\n" % addr)
		
            else:
                
                try:
		        data = sock.recv(RECV_BUFFER)
		        if data:
			   
			   ji = data.split()
			   global MAPPING
			   MAPPING[ji[0]]=sockfd
			   global DECODE
			   DECODE[sockfd]=ji[0]
			   #print "%s split " %ji[0]
			   #print "%s command" %ji[2]
			   #print "%s " % MAPPING[ji[0]]
			   if ji[2] =="sendto" :
				sendto(ji[3],ji)
			   elif ji[2] =="list" :
				daftar(sock,server_socket)
			   elif ji[2]=="sendall" :
				datajadian = "\n" + ji[0] + " says "
				count = 0
				while count !=len(ji):
					if count >2:
						datajadian += (ji[count]+" ")
					count+=1
				datajadian += "\n"
				broadcast(server_socket, sock, "\r"+datajadian )
			   else:
				broadcast1()
		        else:            
		           if sock in SOCKET_LIST:
		                SOCKET_LIST.remove(sock)     
		           broadcast(server_socket, sock, "Client (%s, %s) off\n" % addr) 
 
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) off\n" % addr)
                    continue

    server_socket.close()

def daftar(sock,server_socket):
	#print "%s" %sock
	#print "%s" %server_socket
	#sock.send("\n")
	#counter = 0	
	for socket in SOCKET_LIST :
		
		if sock != socket and server_socket!=socket:
			try:
				sock.send("\n"+DECODE[socket]+" is online\n")
			except :
				sock.close()
				if sock in SOCKET_LIST:
					SOCKET_LIST.remove(socket)
def sendto(destination,message):
	data = "\n"+message[0] + " says "
	count = 0 
	while count!=len(message):
		if count>3 :
			data+=(message[count]+" ")
		count +=1	
	data += "\n"
	#print "%s" %data
	#print "%s \n" %destination
	#print "%s\n" %MAPPING[destination].bind
	#print "%s\n" %MAPPING[message[0]].bind
	socket = MAPPING[destination]
	try :
		socket.send(data)
	except :
		socket.close()
		if socket in SOCKET_LIST :
			SOCKET_LIST.remove(socket)			
def broadcast (server_socket, sock, message):
    
    for socket in SOCKET_LIST:
        #print "%s" %socket
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                
                socket.close()
                
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)	
def broadcast1 ():
   #ujicoba
   print ""
 
if __name__ == "__main__":

    sys.exit(chat_server())
