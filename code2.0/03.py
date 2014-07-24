import server

HOST = 'matrix'
PORT = 4000
ser = server.Server(HOST,PORT)
directory = '/home/rohanj/work/network-project/code/03/'
mode = ""
print "getting mode"

mode = ser.conn.recv(10)

print mode
while (mode!="disconnect"):
	if (mode == "000receive"):
		ser.conn.send("00filename")
		fname1 = ser.getmode().split('/')
		fname = fname1[len(fname1)-1]
		
		fd = open(directory+fname,'wb')
		ser.getchunk(fd)
		print "file received"
		#ser.conn.send("received".zfill(128))
	
	
	mode = ser.conn.recv(10)

print "server closing"
#f = open(directory+"receive",'wb')
#ser.getchunk(f,ser.conn)

