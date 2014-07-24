import client
import file
import gui2

HOST = ['172.24.16.100','172.24.16.100','172.24.16.100']
PORT = [3000,5000,6000]
cli = client.Client([],[])
gui = gui2.gui(cli)

'''

inp = raw_input().split(' ')

fname = inp[0]
n = int(inp[1])
k = int(inp[2])
print n,k,fname
file.split_encodefile(fname,n,k)

directory = '/home/rohanj/work/network-project/code/'
for i in range(n):
	f = open(directory+fname+".part-"+str(i),'rb')
	cli.sendchunk(f,cli.socket[i].s)

#f = open(directory+"axis.mp4",'rb')
#cli.sendchunk(f,cli.socket[0].s)
'''
