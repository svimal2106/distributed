import socket, os
import time
import uu
import file
from stat import ST_SIZE
#list of host servers to connect with respective ports
Hosts = ['172.24.16.100']
Ports = [31400]             
block_size =1024
directory = '/home/rohanj/work/network-project/files/'

class Client:
	def __init__(self,Hosts,Ports):
		self.Hosts = Hosts
		self.Ports = Ports
		self.socket = range(len(Hosts))
		#self.connectall()
		
	def getfilelist(self,directory):
		return os.listdir(directory)


	def connectall(self):
		self.socket = range(len(Hosts))
		#print Hosts,Ports
		for i in range(len(self.Hosts)):
			ip = Hosts[i]
			port = Ports[i]
			self.socket[i] = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),1,ip,port)
			print "trying to connect:",ip
			self.socket[i].s.connect((ip,port))
			if self.socket[i].s.recv(5)!='READY':
				print "unnable to connect: ",self.Hosts[i]
				self.socket[i].s.close()
				self.socket[i].status = 0
			else:
				print "success :",self.Hosts[i],":",self.Ports[i]
				self.socket[i].status = 1

	def connect(self,ip,port):
		self.Hosts.append(ip)
		self.Ports.append(int(port))
		s = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),1,ip,port)
		self.socket.append(s)
		index = len(self.socket)-1
		self.socket[index].s.connect((ip,port))
		print "trying to connect to:",ip,":",port
		if self.socket[index].s.recv(5)!='READY':
			print "unnable to connect: ",self.Hosts[i]
			self.socket[index].s.close()
			self.socket[index].status = 0
			return False
		else:
			print "success :",ip,":",port
			return True

	def getmsg(self,s,l):
		msg = s.recv(l)
		for i in range(l):
			if msg[i]!='0':
				break
		mode = msg[i:128]
		print "msg is :",mode
		return mode

	def getchunk(self,f,conn):
		fsize = long(conn.recv(128))
		print "file size", fsize
		count = long(fsize/block_size)
		rem = long(fsize%block_size)
		print "count :",count,"rem :",rem," count+rem:",count*block_size+rem
		j=0
		remain = fsize
		rec = 0
		while rec<fsize-rem:
			chunk = conn.recv(block_size) 
			if not chunk:
				print "error"
				break
			f.write(chunk)
			rec+=len(chunk)
			#rec = os.stat(f.name)[ST_SIZE]
			#print "written to file ",j
			if os.stat(f.name)[ST_SIZE]>=fsize:
				print "file limit exceeeds ",os.stat(f.name)[ST_SIZE]  
				break
			j=j+1
		print "value of j not executed:",j
		f.write(conn.recv(rem))
		print "final size of written file:",os.stat(f.name)[ST_SIZE]



	def split_send(self,f):
		n = len(self.socket)
		print "n:",n,"calling file.split_file"
		file.split_file(f,n)
		fname = f.name
		for i in range(n):
			self.socket[i].s.send("receive".zfill(128))
			msg = self.getmsg(self.socket[i].s)
			print msg
			print "file name :",fname
			self.socket[i].s.send(fname.zfill(128))
			outfd = open(fname+".part-"+str(i),'rb')
			print "sending chunk ",str(i)
			self.sendchunk(f,self.socket[i].s)
			msg = self.getmsg(self.socket[i].s)
			print msg

	def sendfile(self,f,s):
		fsize=os.stat(f.name)[ST_SIZE]
		s.send(str(fsize).zfill(128))
		s.sendall(f.read())             
        #f.close()

	def sendchunk(self,f,s):
		fsize=os.stat(f.name)[ST_SIZE]
		print "fsize ",fsize," fname ",f.name
		s.send(str(fsize).zfill(128))
        
		count = fsize/block_size
		rem = fsize % block_size
		j = 0
		remain = fsize
		sent=0   
		while remain>rem:
			sent = sent+s.send(f.read(block_size))
			#print "send ",j
			remain = fsize-sent
			j=j+1
		sent = sent+s.send(f.read(rem))
		f.close()
		print "total data sent:",sent

	def sendfilechunks(self,directory,header,chunks):
		i=0
		while i<chunks:
			if i<10:
				f=open(directory + header + "0" + str(i), 'r')
			else:
				f = open(directory + header + str(i),'r')
			self.sendchunk(f)
			i=i+1
		print "chunck " , i , " is uploaded"



class Socket:
	def __init__(self,s,status,ip,port):
		self.s = s
		self.status = status
		self.server_ip = ip
		self.server_port = port

