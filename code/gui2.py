import Tkinter as tk # gives tk namespace
import Tkinter,tkFileDialog
import client
import file

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
		#self.fin = open("serverlist.txt", "r")
		#self.server_list = self.fin.readlines()
		#self.fin.close()
		# strip the trailing newline char
		#self.server_list = [chem.rstrip() for chem in self.server_list]
		#for item in self.server_list:
		    #listbox1.insert(tk.END, item)
		#	self.client.Hosts.append(item.split(":")[0])
		#	self.client.Ports.append(int(item.split(":")[1]))
		#print self.client.Hosts , self.client.Ports
		#self.client.connectall()
		#for i in range(len(self.client.socket)):
		#	if self.client.socket[i].status == 1:
		#		ip = self.client.socket[i].server_ip
		#		port = self.client.socket[i].server_port
		#		listbox1.insert(tk.END,ip+":"+str(port))
		

		self.yscroll1 = tk.Scrollbar(command=listbox1.yview, orient=tk.VERTICAL)
		self.yscroll1.grid(row=0, column=1, sticky=tk.N+tk.S)
		self.yscroll2 = tk.Scrollbar(command=listbox1.yview, orient=tk.VERTICAL)
		self.yscroll2.grid(row=0, column=3, sticky=tk.N+tk.S)
		yscroll1 = self.yscroll1
		yscroll2 = self.yscroll2
		self.listbox1.configure(yscrollcommand=yscroll1.set)
		self.listbox1.bind('<ButtonRelease-1>', self.get_list)
		self.listbox2.bind('<ButtonRelease-1>', self.get_list2)
		self.listbox2.configure(yscrollcommand=yscroll2.set)		
	 
	# use entry widget to display/edit selection
	# pressing the return key will update edited line		
		self.enter1 = tk.Entry(root, width=25, bg='yellow')
		self.enter1.insert(0, '')
		self.enter1.grid(row=1, column=0)
		self.enter1.bind('<Return>', self.connect_server)
#or double click left mouse button to update line
		self.enter1.bind('<Double-1>', self.connect_server)
		
		enter1 = self.enter1

		self.enter2 = tk.Entry(root, width=25, bg='yellow')
		self.enter2.insert(0, '')
		self.enter2.grid(row=1, column=2)
		self.enter2.bind('<Return>', self.set_list)
#or double click left mouse button to update line
		self.enter2.bind('<Double-1>', self.set_list)
				

		self.button1 = tk.Button(root, text='connect',command=self.connect_server)
		self.button1.grid(row=2, column=0, sticky=tk.W)
		self.button4 = tk.Button(root, text='Disconnect', command=self.delete_server)
		self.button4.grid(row=3, column=0, sticky=tk.W)

		self.button2 = tk.Button(root, text='rs_encode', command=self.rs_encode)
		self.button2.grid(row=2, column=2, sticky=tk.E)


		self.button5 = tk.Button(root, text='send file', command=self.send_file)
		self.button5.grid(row=3, column=2, sticky=tk.E)
		self.button6 = tk.Button(root, text='view files', command=self.get_filelist)
		self.button6.grid(row=4, column=0, sticky=tk.W)


		self.button3 = tk.Button(root, text='download', command=self.fun)
		self.button3.grid(row=4, column=2, sticky=tk.E)

		self.button7 = tk.Button(root, text='decode', command=self.rs_decode)
		self.button7.grid(row=5, column=2, sticky=tk.E)
		self.button7 = tk.Button(root, text='split/send', command=self.split_send)
		self.button7.grid(row=5, column=0, sticky=tk.W)
		self.button8 = tk.Button(root, text='join files', command=self.join)
		self.button8.grid(row=6, column=2, sticky=tk.E)

		root.mainloop()

	def send_file(self):
		fd = tkFileDialog.askopenfile(parent=self.root,mode='rb',title='Choose a file')
		if fd == None:
			return
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

	def split_send(self):
		fd = tkFileDialog.askopenfile(parent=self.root,mode='rb',title='Choose a file')
		if fd == None:
			return
		n = len(self.client.socket)
		
		file.split_file(fd,n)
		for i in range(n):
			self.client.socket[i].s.send("receive".zfill(10))		
			msg = self.client.socket[i].s.recv(10)
			print "msg ",msg
			self.client.socket[i].s.send((fd.name+".part-"+str(i)+"_"+str(n)).zfill(128))
			infd = open(fd.name+".part-"+str(i)+"_"+str(n),'rb')
			self.client.sendchunk(infd,self.client.socket[i].s)

	def join(self):
		fd = tkFileDialog.askopenfile(parent=self.root,mode='rb',title='Choose a file')
		chunks = 0
		if fd == None:
			return
		lis = fd.name.split("/")
		fname = lis[len(fd.name.split("/"))-1]
		folder = "/".join(lis[0:len(lis)-1])+"/"
		print folder
		for i in range(len(fname)-6):
			if fname[i:i+6]==".part-":
				header = folder+fname[0:i]
				filename = fname[0:i]
				for j in range(len(fname)-i+6):
					if fname[i+j]=='_':
						chunks = int(fname[i+j+1])
						break
				print header
				break
			if i > len(fname)-6:
				print "file not supported"
				return
		print filename,header,chunks
		file.join_files(header,header,chunks)
		
		
#Note: value of k can be changed here			
		
		
	def rs_encode(self):
		n = len(self.client.socket)
		k = n-2          # to change the value of k (0<k<n)
		
		fd = tkFileDialog.askopenfile(parent=self.root,mode='rb',title='Choose a file')
		if fd == None:
			return
		file.split_encodefile(fd.name,n,k)
		for i in range(n):
			self.client.socket[i].s.send("receive".zfill(10))		
			msg = self.client.socket[i].s.recv(10)
			print "msg ",msg
			self.client.socket[i].s.send((fd.name+".enpart-"+str(i)).zfill(128))
			infd = open(fd.name+".enpart-"+str(i),'rb')
			self.client.sendchunk(infd,self.client.socket[i].s)

	def rs_decode(self):
		folder = tkFileDialog.askdirectory(parent = self.root)
		if folder == None:
			return
		print folder
		filelist = self.client.getfilelist(folder)
		print sorted(filelist)
		result = file.decode_store(sorted(filelist),folder+"/")
		if(result == True):
			top = tk.Toplevel()
			top.title("Message:")
			msg = tk.Message(top, text="successfully decoded")
			msg.pack()
			button = tk.Button(top, text="OK", command=top.destroy)
			button.pack()
		else:
			top = tk.Toplevel()
			top.title("Message:")
			msg = tk.Message(top, text="insufficient files available.")
			msg.pack()
			button = tk.Button(top, text="OK", command=top.destroy)
			button.pack()
			
			


	def fun(self):
		folder = tkFileDialog.askdirectory(parent = self.root)
		if folder == None:
			return
		print folder
		fname = self.enter2.get()
		seltext = self.enter1.get().split(":")
		ip = seltext[0]
		port = int(seltext[1])
		for i in range(len(self.client.socket)):
			if (ip == self.client.socket[i].server_ip):
				if(port==self.client.socket[i].server_port):
					break
		s = self.client.socket[i].s
		s.send("download".zfill(10))
		msg = s.recv(10)
		fd = open(folder+"/"+fname,'wb')
		s.send(fname.zfill(128))
		self.client.getchunk(fd,s)
		print "file received"

	def get_filelist(self):
		temp_list = list(self.listbox2.get(0, tk.END))
		self.listbox2.delete(0, len(temp_list))
		seltext = self.enter1.get().split(":")
		ip = seltext[0]
		port = int(seltext[1])
		for i in range(len(self.client.socket)):
			if (ip == self.client.socket[i].server_ip):
				if(port==self.client.socket[i].server_port):
					break
		s = self.client.socket[i].s
		s.send("listfiles".zfill(10))
		total_files = int(s.recv(10))
		for i in range(total_files):
			msg = self.client.getmsg(s,35)
			print msg
			self.listbox2.insert(tk.END, msg)
		

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

	def get_list2(self,event):
		index = self.listbox2.curselection()[0]
		# get the selected line's text
		seltext = self.listbox2.get(index)
		print seltext
		# delete previous text in enter1
		self.enter2.delete(0, 50)
		# now display the selected text
		self.enter2.insert(0, seltext)
	
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
						self.client.socket[i].s.send("logout".zfill(10))
						self.client.socket[i].s.close()
			self.listbox1.delete(index)
		except IndexError:
			pass

	 
	def connect_server(self,event = None):
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

