

import sys, socket, select
 
def chat_client():
    if(len(sys.argv) < 3) :
        print 'pakai alamat dan juga portnya ya...'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected. Silahkan mengikuti instruksi yang bawah'
    sys.stdout.write('Masukkan nama anda '); sys.stdout.flush()
    test=raw_input()
    print 'Silahkan mulai mengirim pesan'
    sys.stdout.write(test+ " says "); sys.stdout.flush()
    	
     
    while 1:
        socket_list = [sys.stdin, s]
         
        
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:            
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDC dari chat server'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write(test+" says "); sys.stdout.flush()     
            
            else :
                msg = sys.stdin.readline()
		msg = test+" says "+msg
                s.send(msg)
                sys.stdout.write(test+" says "); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())
