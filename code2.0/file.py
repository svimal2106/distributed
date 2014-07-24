import os , string
from stat import ST_SIZE
import reedcode
import shutil
from array import array
import struct

def split_file(infd,chunks):
	#infd = open(fname,'rb')
	fname = infd.name
	fsize = os.stat(infd.name)[ST_SIZE]
	chunk_size = fsize/chunks
	rem = chunk_size%chunks
	for i in range(chunks):
		outfd = open(fname+".part-"+str(i),'wb')
		sent = 0
		while sent<chunk_size:
			buffer = infd.read(1024)
			outfd.write(buffer)
			sent = sent+1024
	print "file has been split"

def join_files(fname,header,chunks):
	outfd = open(fname,'wb')
	for i in range(chunks):
		infd = open(header+".part-"+str(i),'rb')
		shutil.copyfileobj(infd,outfd)
	


def encode(infd,readk,code,outFD):
	buffer = array('B')
	buffer.fromfile(infd,readk)
	for i in range(readk,code.k):
		buffer.append(0)
	encoded= code.Encode(buffer)
	for j in range(code.n):
	        outFD[j].write(struct.pack('B',encoded[j]))

def split_encodefile(fname,n,k):
	infd = open(fname,'rb')
	fsize = os.stat(fname)[ST_SIZE]
	rscode = reedcode.RScode(n,k,8,shouldUseLUT=-(k!=1))
	rscode.show()
	outfdlist = range(n)	
	for i in range(n):
		name = fname+".part-"+str(i)
		outfdlist[i] = open(name,'wb')
		#header format: <filename> <n> <k> <packet number> <file size>
		outfdlist[i].write(fname+" "+str(n)+" "+str(k)+" " +str(i)+" "+str(fsize)+'\n')

	if (k==1): #simply copying the files
		for i in range(n):
			shutil.copyfileobj(infd,outfdlist[i])
			infd = open(fname,'rb')
	else:
		remain = fsize
		rem = fsize%k
		while (remain>rem):
			encode(infd,k,rscode,outfdlist)
			remain = remain-k
		encode(infd,rem,rscode,outfdlist)


def decode(writeSize,inFDs,outFD,code):
	buffer = array('B')
	for j in range(code.k):
		buffer.fromfile(inFDs[j],1)
	result = code.Decode(buffer.tolist())
	for j in range(writeSize):
		outFD.write(struct.pack('B',result[j]))

def decode_store(fnames,outname):
	temp = open(fnames[0],'rb')
	tempheader = temp.readline().split(" ")
	n = int(tempheader[1])
	k = int(tempheader[2])
	fsize = long(tempheader[4])
	rscode = reedcode.RScode(n,k,8)
	temp.close()		
	infdlist = range(len(fnames))
	headers = range(len(fnames))
	packets = range(len(fnames))
	j=0
	#for i in range(len(fnames)):		
	#	infdlist[i] = None
	for i in range(len(fnames)):
		#temp = open(fnames[i],'rb')
		#index = temp.getline().split(" ")[3]
		#temp.close()
		infdlist[i]=open(fnames[i],'rb')
		headers[i] = infdlist[i].readline()
		packets[i] = int(headers[i].split(" ")[3])
	declist = packets[0:k]
	outfd = open(outname,'wb')
	rscode.modifyencoder(declist)
	remain = fsize
	rem = fsize%k
	print "decoding..."
	while (remain>rem):
		decode(k,infdlist,outfd,rscode)
		remain = remain-k
	decode(rem,infdlist,outfd,rscode)
	print "decoding successful"
		

'''inp = raw_input().split(' ')
fname = inp[0]
n = int(inp[1])
k = int(inp[2])
print n,k,fname
split_encodefile(fname,n,k)
decList = map(lambda x: fname + '.part-' + `x`,[0,1,2,3])
decode_store(decList,"myresult")
'''


	
		

	


