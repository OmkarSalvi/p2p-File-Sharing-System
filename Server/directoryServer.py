import socket
import threading
import time
import logging

class Broker():
	def __init__(self):
		logging.info('Initializing Server')
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_ip=socket.gethostbyname(socket.gethostname())
		print "Server's IP address is: "+ str(server_ip)
		self.sock.bind((server_ip,1218 ))
		self.clients_list = []
	
	def checkquery(self,query):
		#print query
		m2 = query.split("\r\n")
		m3 = m2[0].split("|")
		request_type = m3[0]
		if request_type == 'Inform and update ':
			ret_type = '1'
		elif request_type == 'Query for content ':
			ret_type = '2'
		elif request_type == 'Exit ':
			ret_type = '3'
		else:
			ret_type = '4'
		#print ret_type
		return ret_type
	
	def updatedict(self,mesg, add ,pck_seq):
			m2 = mesg.split("\r\n")
			m3 = m2[0].split("|")
			client_name = m3[1]
			#print m2
			del m2[0]
			del m2[(len(m2)-2)]
			del m2[(len(m2)-1)]
			#print m2
			m4=[]
			for i in range(len(m2)):
				 #print i
				 m5 = m2[i].split("|")
				 #print m5
				 m4.append(m5[0])
				 #print m4
				 size[m4[i]] = m5[1]
				 #del m4[i+1]
			for i in range(len(m4)):
				temp = m4[i]
				#print i,temp,size[m4[i]],client_name
				if (direct!={}):
					if temp in direct.keys():
						#print "present"
						val = direct.get(temp)
						if client_name not in val:
							#print "appending"
							val.append(client_name)
					else:
						#print "filename not in direct keys"
						direct.setdefault(temp,[]).append(client_name)

				else:
					direct.setdefault(temp,[]).append(client_name)
			print "Current Diectory Contents: \n" + str(direct)
			respok1 = "200 |" + "OK \r\n\r\n" + str(pck_seq)
			print respok1
			#time.sleep(10)
			self.sock.sendto(respok1,add)
	
	def searchkey( self,mesg, add , pck_seq):
		m2 = mesg.split("\r\n")
		searchkey = m2[1]
		#print searchkey
		xo = "File does not exist"
		searchval = direct.get(searchkey,xo)
		sizeval = size.get(searchkey,"0")
		#print searchval
		if ((searchval == xo) | (searchval == [])):
			respok2 = "404 |" + xo + "\r\n" + "\r\n" + str(pck_seq)
		else:
			respok2 = "200 |" + "OK \r\n" 
			for i in range(len(searchval)):
				respok2+= (searchval[i]) + " |" + str(client_address[searchval[i]])+" |"+str(sizeval) + "\r\n"
		respok2 += "\r\n" + str(pck_seq)
		print respok2
		self.sock.sendto(respok2,add)

	def removeclient(self,clientname, add, pck_seq):
		for k,v in direct.items():
			for i in v:
				if i == clientname:
					v.remove(i)
		respok3 = "200 |" + "OK |" +"Thank you \r\n" + "\r\n" + str(pck_seq)
		self.sock.sendto(respok3,add)
		print respok3
		print direct
                
	def talkToClient(self, ip, msg):
		# logging.info("Sending 'ok' to %s", ip)
		# self.sock.sendto("ok", ip)
		if '|' not in msg:
			#print "We got connection from " , ip
			self.sock.sendto("You are connected\n",ip)
		else:
				#print "inside talk client loop"
				#msg, add = self.sock.recvfrom(128)
				print msg
				m2 = msg.split("\r\n")
				pack_seq = m2[len(m2)-1]
				m3 = m2[0].split("|")
				#print "####"+m2[0]
				client_name = m3[1]
				client_address[client_name]=ip
				qtype = self.checkquery(msg)
				if qtype == '1':
					self.updatedict( msg, ip, pack_seq )
				elif qtype == '2':
					self.searchkey(msg, ip, pack_seq)
				elif qtype == '3':
					self.removeclient(client_name, ip, pack_seq)
				else:
					self.sock.sendto("400 | Bad request",ip)
					#print "invalid request"
				
	def listen_clients(self):
		c1=0
		while True:
			c , address = self.sock.recvfrom(128)
			logging.info('Received data from client %s: %s', address, c)
			t = threading.Thread(target=self.talkToClient, args=(address,c,))
			#print "thread is created" + str(c1)
            #t = threading.Thread(target=self.makethread, args=(address,))
			t.start()
			c1 = c1 + 1

if __name__ == '__main__':
    # Make sure all log messages show up
	logging.getLogger().setLevel(logging.DEBUG)
	direct = dict()
	size = dict()
	client_address = dict()
	b = Broker()
	b.listen_clients()
