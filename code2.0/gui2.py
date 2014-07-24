import Tkinter as tk # gives tk namespace
import Tkinter,tkFileDialog
import client
import file



'''
HOST = ['172.24.16.100','172.24.16.100','172.24.16.100']
PORT = [3000,5000,6000]
cli = client.Client(HOST,PORT)
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

'''

class gui:
	
	def __init__(self,client):
		self.client = client
		self.root = tk.Tk()
		root = self.root
		self.root.title("Client")
		self.listbox1 = tk.Listbox(root, width=25, height=10)
	 	self.listbox1.grid(row=0, column=0)
		listbox1 = self.listbox1
		self.listbox2 = tk.Listbox(root, width=25, height=10)
		self.listbox2.grid(row=0, column=2)
		listbox2 = self.listbox2
		self.fin = open("serverlist.txt", "r")
		self.server_list = self.fin.readlines()
		self.fin.close()
		# strip the trailing newline char
		self.server_list = [chem.rstrip() for chem in self.server_list]
		for item in self.server_list:
		    listbox1.insert(tk.END, item)

		self.yscroll1 = tk.Scrollbar(command=listbox1.yview, orient=tk.VERTICAL)
		self.yscroll1.grid(row=0, column=1, sticky=tk.N+tk.S)
		self.yscroll2 = tk.Scrollbar(command=listbox1.yview, orient=tk.VERTICAL)
		self.yscroll2.grid(row=0, column=3, sticky=tk.N+tk.S)
		yscroll1 = self.yscroll1
		yscroll2 = self.yscroll2
		self.listbox1.configure(yscrollcommand=yscroll1.set)
		self.listbox1.bind('<ButtonRelease-1>', self.get_list)
		self.listbox2.configure(yscrollcommand=yscroll2.set)		
	 
	# use entry widget to display/edit selection
	# pressing the return key will update edited line		
		self.enter1 = tk.Entry(root, width=25, bg='yellow')
		self.enter1.insert(0, '')
		self.enter1.grid(row=1, column=0)
		self.enter1.bind('<Return>', self.set_list)
#or double click left mouse button to update line
		self.enter1.bind('<Double-1>', self.set_list)
		
		enter1 = self.enter1
		self.button1 = tk.Button(root, text='connect',command=self.connect_server)
		self.button1.grid(row=2, column=0, sticky=tk.W)
		self.button2 = tk.Button(root, text='rs_encode', command=self.rs_encode)
		self.button2.grid(row=3, column=0, sticky=tk.W)
		#self.button3 = tk.Button(root, text='rs_encode', command=self.rs_encode)
		#self.button3.grid(row=2, column=2, sticky=tk.E)
		self.button4 = tk.Button(root, text='Disconnect', command=self.delete_server)
		self.button4.grid(row=2, column=2, sticky=tk.E)
		self.button4 = tk.Button(root, text='send file', command=self.send_file)
		self.button4.grid(row=3, column=2, sticky=tk.E)
		root.mainloop()

	def send_file(self):
		fd = tkFileDialog.askopenfile(parent=self.root,mode='rb',title='Choose a file')
	
		seltext = self.enter1.get().split(":")
		ip = seltext[0]
		port = int(seltext[1])
		for i in range(len(self.client.socket)):
			if (ip == self.client.socket[i].server_ip):
				if(port==self.client.socket[i].server_port):
					break
		print "file to socket i = ",i
		print seltext[0],seltext[1]
		
		#self.client.sendchunk(fd,self.client.socket[i].s)

		self.client.socket[i].s.send("receive".zfill(10))		
		msg = self.client.socket[i].s.recv(10)
		print "msg ",msg
		self.client.socket[i].s.send((fd.name).zfill(128))
		self.client.sendchunk(fd,self.client.socket[i].s)
		
		#fd.close()
		print "I got bytes from this file."

	def rs_encode(self):
		n = len(self.client.socket)
		k = n-1
		
		fd = tkFileDialog.askopenfile(parent=self.root,mode='rb',title='Choose a file')
		file.split_encodefile(fd.name,n,k)
		for i in range(n):
			self.client.socket[i].s.send("receive".zfill(10))		
			msg = self.client.socket[i].s.recv(10)
			print "msg ",msg
			self.client.socket[i].s.send((fd.name+".part-"+str(i)).zfill(128))
			infd = open(fd.name+".part-"+str(i),'rb')
			self.client.sendchunk(infd,self.client.socket[i].s)

	def add_server(self):
		self.listbox1.insert(tk.END, self.enter1.get())
		self.enter1.delete(0, 50)

	
	def set_list(self,event):
		try:
			index = self.listbox1.curselection()[0]
			# delete old listbox line
			self.listbox1.delete(index)
		except IndexError:
			index = tk.END
			# insert edited item back into listbox1 at index
		self.listbox1.insert(index, self.enter1.get())
		self.enter1.delete(0, 50)

	def get_list(self,event):
		index = self.listbox1.curselection()[0]
		# get the selected line's text
		seltext = self.listbox1.get(index)
		print seltext
		# delete previous text in enter1
		self.enter1.delete(0, 50)
		# now display the selected text
		self.enter1.insert(0, seltext)

	
	def save_list(self):
	# get a list of listbox lines
	    temp_list = list(self.listbox1.get(0, tk.END))
	# add a trailing newline char to each line
	    temp_list = [chem + '\n' for chem in temp_list]
	# give the file a different name
	    fout = open("chem_data2.txt", "w")
	    fout.writelines(temp_list)
	    fout.close()

	def delete_server(self):
		try:
	# get selected line index
			index = self.listbox1.curselection()[0]
			seltext = self.listbox1.get(index).split(":")
			for i in range(len(self.client.socket)):
				if(self.client.socket[i].server_port == int(seltext[1])):
					if(self.client.socket[i].server_ip==seltext[0]):
						self.client.socket[i].s.close()
			self.listbox1.delete(index)
		except IndexError:
			pass

	 
	def connect_server(self):
		#function to send the connection request
		#index = self.listbox1.curselection()[0]
		seltext = self.enter1.get().split(":")
		#self.listbox1.insert(index, self.enter1.get())
		ip = seltext[0]
		port = int(seltext[1])
		status = self.client.connect(ip,port)
		print "Connection request has been sent to:",ip,port
		if (status == True):
			#connection successful
			print "success"
			self.add_server()
		else:
			#unsuccessful attempt
			print "failed"

