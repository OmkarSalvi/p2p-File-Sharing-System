import socket
import os
import glob
import time
import threading


inside = True
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientName=socket.gethostname()
print "Client name is: " + str(clientName)
Server = raw_input("Enter IP address of the Server you wish to connect: ") 
Port = 3100
server_address = (Server, Port)
client_ip= socket.gethostbyname(socket.gethostname())
print "Client IP address is: " + str(client_ip)
s.sendto(clientName,server_address)
mmsg,add=s.recvfrom(128)
print mmsg

def _formrequest_(opt):
	if opt == 1:
                pack_seq = 1
                success = 0
                a=glob.glob('*txt')
                file1 = ""
                request = "Inform and update |" + clientName + "|" + client_ip +"\r\n"
                #print "length of header = " + str(len(request)) + "\n"
                offset = 128 - len(request)
                for i in range(len(a)):
                    frag = a[i] + "|" + str(os.path.getsize(a[i]))+ "Bytes\r\n"
                    #print "length of file field = " + str(len(frag)) + "\n"
                    if (offset < len(frag)):
                        #print "inside if offset"
                        count = 0
                        while(success == 0):
                            if (count == 0):
                                request = request+"\r\n"+str(pack_seq)
                            start = time.time()
                            s.sendto(request,server_address)
                            #pack_seq += 1
                            print request
                            try:
                                ack, add = s.recvfrom(128)
                                elapsed = (time.time()-start)
                                print str(elapsed)
                                print ack
                                ack_seq_no = _extract_(ack,opt)
                                #print str(ack_seq_no)
                                if (ack_seq_no == str(pack_seq)):
                                    #print "inside ack no = pack no"
                                    pack_seq += 1
                                    success = 1
                                else:
                                    success = 0
                                    count += 1
                                if (success == 1):
                                    request = "Inform and update |" + clientName + "|" + client_ip +"\r\n"
                                    request += frag
                                    offset = 128 - len(request)
                            except socket.timeout:
                                print "Request timed out" 
                                success = 0
                                count += 1
                    else:
                        #print "inside else offset"
                        request += frag
                        offset -= len(frag)
						
                success = 0
                while(success == 0):
					request = request+"\r\n"+str(pack_seq)
					s.sendto(request,server_address)
					#print request
					pack_seq += 1 
					
					try:
						ack, add = s.recvfrom(128)
						print str(ack)
						success = 1
						ack_seq_no = _extract_(ack,opt)
					except:
						print "Request timed out"
						success = 1
						success -= 1
	elif opt == 2:
		pack_seq = 1
		qfile=raw_input("Enter the desired file name in  --> ")
		request = "Query for content |" + clientName + "|" + client_ip +"\r\n"+ qfile + "\r\n"
		s.sendto(request+"\r\n"+str(pack_seq),server_address)
		ack, add = s.recvfrom(128)
		#print ack
		m1 = ack.split("\r\n")
		m3 = m1[0].split("|")
		if (m3[0] == '200 '):
			ack_seq_no = _extract_(ack,opt)
			request_file=raw_input("Do you want to request a file?  (Y/N)? ->")
			if request_file == 'Y':
				os.system("python tcp-client.py &")
			else:
				print("Thank you for communication !!!")
	elif opt == 3:
		pack_seq = 1
		request = "Exit |" + clientName + "|" + client_ip +"\r\n"
		s.sendto(request+"\r\n"+str(pack_seq),server_address)
		ack, add = s.recvfrom(128)
		#print ack
		ack_seq_no = _extract_(ack,opt)
	
	else: 
		request = str(opt)
		s.sendto(request + " |" + "\r\n",server_address)
		ack, add = s.recvfrom(128)
		#print ack

		
def _extract_(mesg,optn):
	m1 = mesg.split("\r\n")
	#print m1
	seq_no = m1[len(m1)-1]
	m3 = m1[0].split("|")
	#print str(m3[0])
	if optn==3:
		print "connection closed successfully"
		s.close()
	elif len(m1) > 3:
		del m1[0]
		peer_name = []
		del m1[len(m1)-2]
		del m1[len(m1)-1]
		#print m1
		if (m3[0] == '200 '):
			print "File is with client(s): "
			for j in range(len(m1)):
				peer = m1[j].split("|")
				i=peer[1].split(",")
				ip=i[0].replace("(","")
				print str(peer[0]) + "having IP: "+ str(ip) + " running on port no.: " + str(Port) + "\n"
		#peer_name.append(peer[0])
		#for i in range(len(peer)):
			#peer = m1[i].split("|")
			#peer_name.append(peer[0])
		
		#else:
			#print str(m3)
	return seq_no 


###TCP###
class Tcp():
	def tcp_server_thread(self,port):
		host = socket.gethostbyname(socket.gethostname())
		port=port+200
		t1 = threading.Thread(target=self.tcp_server, args=(host,port))
		t1.start()
		
	def tcp_server(self,host,port):
			
			self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
			#print "step1"
			self.s1.bind((host,port))
			#print "step 2"

			self.s1.listen(5)

			#print "Server Started."
			while True:
				c, addr = self.s1.accept()
				#print "client connected ip:<" + str(addr) + ">"
				t = threading.Thread(target=self.RetrFile, args=("RetrThread", c))
				t.start()

					
			self.s1.close()
		
	def RetrFile(self,name,s1):
		httpreq = s1.recv(128)
		print httpreq
		#filename = s1.recv(128)
		
		file  = httpreq.split("|")
		version = file[2].split("~")
		filename = file[1] 
		#print filename	
	
		if file[0] == "GET ":
			status = "200" 
		elif version[1] != "1.1 ":
			status = "505"
		else:
			status = "400"
		#print "ok" + file[1] +"^^"+file[2] +"^^"+str(version[1])+"##"	
		#print version[1] + "~~~"	
		#print status +"^^"
		
		if os.path.isfile(filename):
			#print str(os.path.getsize(filename))
			s1.send(status + str(os.path.getsize(filename)))
			userResponse = s1.recv(128)
			if userResponse[:2] == 'OK':
				with open(filename, 'rb') as f:
					bytesToSend = f.read(128)
					s1.send(bytesToSend)
					while bytesToSend != "":
						bytesToSend = f.read(128)
						s1.send(bytesToSend)
		else:
			status="404"
			s1.send(status)
			#s1.send("ERR ")
		#print('connection closing..'+str(s1))
		s1.close()

if __name__ == '__main__':
	tcp=Tcp()
	tcp.tcp_server_thread(Port)
	while inside:
		option = input("Enter 1-->Inform and update  2-->Query for content  3-->Exit ")
		s.settimeout(10) # set 100ms timeout
		#if ((option !=1) & (option != 2) & (option !=3)):
			#print ("please select a valid option")#err 404 bad request
			
		#else:
		_formrequest_(option)
		if option == 3:
			inside = False
