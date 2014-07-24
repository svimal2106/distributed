import socket, os
import uu
from stat import ST_SIZE
directory = '/home/rohanj/work/network-project/01/'
 
block_size =1024

HOST = '172.24.16.100'
PORT = 31400

class Server:
	def __init__(self,Host,Port):
		self.Host = Host
		self.Port = Port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((self.Host,self.Port))
		self.s.listen(3)
		(self.conn, self.addr) = self.s.accept()
		print 'conn at address',self.addr
		self.conn.send('READY')
	
	def getmode(self):
		msg = self.conn.recv(128)
		for i in range(len(msg)):
			if msg[i]!='0':
				break
		mode = msg[i:]
		print "mode is :",mode
		return mode

	def getfilelist(self,directory):
		return os.listdir(directory)

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

	def getchunk(self,f):
		conn = self.conn
		fsize = long(conn.recv(128))
		print "file size", fsize
		count = long(fsize/block_size)
		rem = long(fsize%block_size)
		print "count :",count,"rem :",rem," count+rem:",count*block_size+rem
		j=0
		remain = fsize
		rec = 0
		while j<count:
			chunk = self.conn.recv(block_size) 
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
		print "value of (j-1)*blocksize: " ,str(j*block_size)
		print "value of rec ",str(rec)
		f.write(conn.recv(rem))
		print "final size of written file:",os.stat(f.name)[ST_SIZE]

	def getfilechunks(self,header,chunks):
		i=0	
		while i<chunks:
			if i<10:
				f=open(directory + header + "0" + str(i), 'wb+')
			else :
				f = open( directory + header + str(i),'wbi+')
			self.getchunk(f,self.conn)
			i=i+1
		print "all the ",chunks, "chunks are downloaded"
	


#f = open('/home/rohanj/work/network-project/01/send23','w')



#f = open('/home/rohanj/work/network-project/01/down.mkv','wb')
#fsize=int(conn.recv(8))
#print 'File size',fsize
def getfile(f):
	while 1:
		data = conn.recv(100)
		if not data:
			break
		f.write(data)
