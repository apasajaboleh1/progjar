import socket,time,datetime,sys	
server_addr=(host,port)='localhost',80
queue_data=5;

	
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_addr)
sock.listen(queue_data)
print 'serve at %s port %s'%server_addr
while True:
	client_con,client_addr=sock.accept()
	test="<!DOCTYPE HTML><html><h1>sukses gan</h1></html>"
	data="HTTP/1.1 200 OK \n\n%s"%test
	request = client_con.recv(1024)
	request_data=request.split()
	temp=request_data[1]
	temp1=temp[1:]
	if temp=="/" :
		
		http_response=data	
    		client_con.sendall(http_response)
	else :
		try :
			#print temp1
			f=open(temp1,"r+")
			ambil_data=f.read()
			f.close()
			if ambil_data :
				data_send="HTTP/1.1 200 OK \n\n%s"%ambil_data
				client_con.sendall(data_send)
		except :
    			err="HTTP/1.1 404 Not Found\n\n <h1>NOT FOUND</h1>"
                	client_con.sendall(err)
	client_con.close()
		

