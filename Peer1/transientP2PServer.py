

import socket
import threading
import os
	
def main():
	#while True:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		host = raw_input("Enter IP: ")
		port = input("Input Port no.: ")
		port=port+200
		#print("Started Working as a client")
		s.connect((host, port))
		filename = raw_input("Filename? -> ")
		if filename != 'q':
			httpreq = "GET |"+ filename + "| HTTP~1.1 \r\n"
			s.send(httpreq)
			#s.send(filename)
			data = s.recv(128)			
			status = data[:3]
			if status == "200":
				phrase = "OK"
			elif status == "404":
				phrase = "File Not Found"
			elif status == "400":
				phrase = "Bad Request"
			elif status == "505":
				phrase = "Invalid Version"
			
			#replymsg = "P2P-TCP/1.1 " + status + " " + phrase + "\n"
			replymsg = status + "|" + phrase + "\n"
			#print replymsg
			
			if data[:3] == '200':
			
				filesize = long(data[3:])
				#print filesize
				message = raw_input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
				#message = 'Y'
				if message == 'Y':
					s.send("OK")
					f = open(filename, 'wb')
					data = s.recv(128)
					totalRecv = len(data)
					f.write(data)
					while totalRecv < filesize:
						data = s.recv(128)
						totalRecv += len(data)
						f.write(data)
						print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
					print "Download Complete!"
					f.close()
			else:
				print "File Does Not Exist!!!"
		#print("connection closing for host "+host)
		s.close()
						
	

if __name__ == '__main__':
    main()




