import socket, os
import time
import uu
import file
from stat import ST_SIZE
#list of host servers to connect with respective ports
Hosts = ['172.24.16.100']
Ports = [31400]             
block_size =2048
directory = '/home/rohanj/work/network-project/files/'

class Client:
	def __init__(self,Hosts,Ports):
		self.Hosts = Hosts
		self.Ports = Ports
		self.socket = range(len(Hosts))
		#self.connectall()
		

	def connectall(self):
		for i in range(len(self.Hosts)):
			self.socket[i] = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),1)
			print "trying to connect:",self.Hosts[i]
			self.socket[i].s.connect((self.Hosts[i],self.Ports[i]))
			if self.socket[i].s.recv(5)!='READY':
				print "unnable to connect: ",self.Hosts[i]
				self.socket[i].s.close()
				self.socket[i].status = 0
			else:
				print "success :",self.Hosts[i],":",self.Ports[i]

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

	def getmsg(self,s):
		msg = s.recv(128)
		for i in range(len(msg)):
			if msg[i]!='0':
				break
		mode = msg[i:]
		print "msg is :",mode
		return mode


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

