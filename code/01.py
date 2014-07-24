import server

HOST = 'localhost'
PORT = 2001
ser = server.Server(HOST,PORT)
directory = '/home/rohanj/work/network-project/code/01/'

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

	if (mode == "00download"):
		ser.conn.send("00filename")
		fname = ser.getmode()
		print fname
		fd = open(directory+fname,'rb')
		ser.sendchunk(fd,ser.conn)
		print "file is send"

	if (mode == "0listfiles"):
		flist = ser.getfilelist(directory)
		ser.conn.send(str(len(flist)).zfill(10))
		for fname in flist:
			print fname
			ser.conn.send(fname.zfill(35))
	if (mode == "logout".zfill(10)):
		ser.conn.close()
		ser.s.listen(3)
		(ser.conn, ser.addr) = ser.s.accept()
		print 'conn at address',ser.addr
		ser.conn.send('READY')
	
	mode = ser.conn.recv(10)

print "server closing"
#f = open(directory+"receive",'wb')
#ser.getchunk(f,ser.conn)

