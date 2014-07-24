#import ffield
import GField
import genericmatrix
import math

class RScode:
	def __init__(self,n,k,FieldSize=-1,shouldUseLUT=-1):
		
		if (FieldSize < 0):
			FieldSize = int(math.ceil(math.log(n)/math.log(2)))
		
		self.field = GField.GField(FieldSize,useLUT=shouldUseLUT)
		self.n = n
		self.k = k
		self.fieldSize = 2**FieldSize
		self.CreateEncoderMatrix()
		self.encoderMatrix.Transpose()
		self.encoderMatrix.LowerGaussianElim()
		self.encoderMatrix.UpperInverse()
		self.encoderMatrix.Transpose()

	def CreateEncoderMatrix(self):
		self.encoderMatrix = genericmatrix.GenericMatrix((self.n,self.k),0,1,self.field.Add,self.field.Subtract,self.field.Multiply,self.field.Divide)
		self.encoderMatrix[0,0] = 1
		for i in range(0,self.n):
			term = 1
			for j in range(0, self.k):
				self.encoderMatrix[i,j] = term
				term = self.field.Multiply(term,i)
	def show(self):
		print ('RScode('+`self.n`+','+`self.k`+')'+' over GF(2^'+`self.field.n`+')\n' +`self.encoderMatrix`+'\n')

	def Encode(self,inplist):
		try:
			if(len(inplist)!=self.k):
				raise invalidlist
			else:
				result =  list(self.encoderMatrix.LeftMulColumnVec(inplist))
				#print inplist, "-->" ,result
				return result
		except invalidlist:
			print "invalid input data length. it should be k=",k

	def modifyencoder(self,firstk):
		assert (len(firstk)==self.k)
		new_encoderMatrix = genericmatrix.GenericMatrix(
            (self.k,self.k),0,1,self.field.Add,self.field.Subtract,
            self.field.Multiply,self.field.Divide)
		for i in range(self.k):
			new_encoderMatrix.SetRow(i,self.encoderMatrix.GetRow(firstk[i]))
		self.decoderMatrix = new_encoderMatrix.Inverse()

	def Decode(self,unErasedTerms):
		return self.decoderMatrix.LeftMulColumnVec(unErasedTerms)

		
