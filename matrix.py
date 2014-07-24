import operator
class Matrix:
   

    def __init__(self,rows,columns,add = operator.__add__,subt = operator.__sub__,
                 mul = operator.__mul__,div = operator.__div__):
         #self.matrix = zeros(rows,Int)
         #for i range(rows):
          #   self.matrix[i] = zeros(columns,Int)
          self.add = add
          self.subt = subt
          self.mul = mul
          self.div = div
          self.rownum = rows
          self.colnum = columns
          self.matrix = []
          for i in range(rows):
	      self.matrix.append([])
	      for j in range(columns):
		  if i==j:
		     self.matrix[i].append(1.0)
		  else:
		     self.matrix[i].append(0.0) 
		     

		  
    def display(self):
        print self.matrix
        

        
    def replicate(self):
        new = Matrix(self.rownum,self.colnum)
        new.matrix = []
        for i in range(self.rownum):
	    new.matrix.append([])
	    for j in range(self.colnum):
	        new.matrix[i].append(self.matrix[i][j])
	return new
	
    def getelement(self,row,col):
        if row >= self.rownum or col >= self.colnum:
	   raise ValueError,'invalid row or column number'
        return self.matrix[row][col]
     
     
    def setelement(self,row,num,data):
        if row >= self.rownum or col >= self.colnum:
	   raise ValueError,'invalid row or column number'
        self.matrix[row][col] = data
        
    def multcolvector(self,vector):
        #temp = []
        if (self.colnum != len(vector)):
            raise ValueError, 'dimension mismatch'
        result = []
        for r in range(self.rownum):
            result.append(reduce(self.add,map(self.mul,self.matrix[r],vector)))
        return result
        
    def getrow(self,rowno):
        if rowno >= self.rownum:
	   raise ValueError,'row number too big'
        temp = []
        for i in range(self.colnum):
	    temp.append(self.matrix[rowno][i])
        return temp
       
    def getcolumn(self,colno):
        if colno >= self.colnum:
	   raise ValueError,'column number too big'
        temp = []
        for i in range(self.rownum):
	    temp.append(self.matrix[i][colno])
        return temp
    
    def setrow(self,rowno,arg):
        if self.colnum != len(arg):
	   raise ValueError,'cannot set row,bad length of argument array'
        for i in range(self.colnum):
	   self.matrix[rowno][i] = arg[i]
      
        
    def transpose(self):
        temp = Matrix(self.colnum,self.rownum)
        for i in range(temp.rownum):
	   temp.setrow(i,self.getcolumn(i))
	return temp
        
    def appendidentity(self):
        temp = Matrix(self.rownum,self.colnum)
        for i in range(self.rownum):
	    self.matrix[i].extend(temp.matrix[i]);
	    
    def swaprows(self,row1,row2):
        temp = self.matrix[row1]
        self.matrix[row1] = self.matrix[row2]
        self.matrix[row2] = temp
        
    def findmaxindex(self,currentindex):
        #temp = self.getcolumn(currentindex)
        index = currentindex
        maxnow= self.matrix[currentindex][currentindex]
        for i in range(currentindex,self.rownum):
	    if self.matrix[currentindex][i] > maxnow:
	       index = i
	       maxnow = self.matrix[currentindex][i]
	return index
	
   
	
    def subtract(self,index1,index2,factor):
        for i in range(2*self.colnum):
	    self.matrix[index2][i] = self.subt(self.matrix[index2][i],factor*self.matrix[index1][i])
	    
    def downrowoperation(self,index):
        for i in range(index+1,self.rownum):
	    factor = self.div(self.matrix[i][index],self.matrix[index][index])
	    self.subtract(index,i,factor)
    
    def uprowoperation(self,index):
        for i in range(index-1,-1,-1):
	    factor = self.div(self.matrix[i][index],self.matrix[index][index])
	    self.subtract(index,i,factor)
        
    def lowerdecomposition(self):
        for i in range(self.rownum-1):
	    index = self.findmaxindex(i)
	    if index != i:
	       self.swaprows(i,index)
	    self.downrowoperation(i) 

    def upperdecomposition(self):
         for i in range(self.rownum-1,0,-1):
	     self.uprowoperation(i)
	     
    def divide(self,index,elem):
        for i in range(2*self.colnum):
	    self.matrix[index][i] =self.div(self.matrix[index][i],elem)
	     
    def normalise(self):
        for i in range(self.rownum):
	    elem = self.matrix[i][i]
	    self.divide(i,elem)

    def retrieve(self):
        temp = Matrix(self.rownum,self.colnum)
        for i in xrange(0,self.rownum):
	    for j in xrange(self.colnum,2*self.colnum):
	        temp.matrix[i][j-self.colnum] = self.matrix[i][j]
	return temp
	
    def makecopy(self):
        temp = Matrix(self.rownum,self.colnum)
        for i in range(self.rownum):
	    for j in range(self.colnum):
	      temp.matrix[i][j] = self.matrix[i][j]
	return temp
	    
    def inverse(self):
        if self.determinant() == 0:
	   raise ValueError,'Matrix is not invertible'
	temp = self.replicate()
        temp.appendidentity()
        temp.lowerdecomposition()
        temp.upperdecomposition()
        temp.normalise()
        inv = temp.retrieve()
        return inv
        
        
    def submatrix(self,currentrow,currentcol):
        sub = Matrix(self.rownum-1,self.colnum-1)
        temp = []
        count = 0
        for i in range(self.rownum):
	    if i != currentrow:
	       temp.append([])
	       for j in range(self.colnum):
		   if j != currentcol:
		      temp[count].append(self.matrix[i][j])
	       count+=1
        sub.matrix = temp
        return sub
		   
        
        
    def determinant(self):
        if self.rownum != self.colnum:
	   raise ValueError,'Expected square matrix  as argument'
	if self.rownum == 1 and self.colnum == 1:
	   return self.matrix[0][0]
	else:
	   result = 0
	   for j in range(self.colnum):
	       if j%2 == 0:
		  result += (self.matrix[0][j])*((self.submatrix(0,j)).determinant())
	       else:
		  result -= (self.matrix[0][j])*((self.submatrix(0,j)).determinant())
	return result
        
	    
	    
	       
	       
	    
        
        
    
        
        
        
        