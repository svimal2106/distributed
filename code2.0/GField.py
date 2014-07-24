import string, random, os, os.path, cPickle
from LUT import LUT

# The following list of primitive polynomials are the Conway Polynomials
# taken from the list at
# http://www.math.rwth-aachen.de/~Frank.Luebeck/ConwayPol/cp2.html

gPrimitivePolys = {}
gPrimitivePolysCondensed = {
    1  : (1,0),
    2  : (2,1,0),
    3  : (3,1,0),
    4  : (4,1,0),
    5  : (5,2,0),
    6  : (6,4,3,1,0),
    7  : (7,1,0),
    8  : (8,4,3,2,0),
    9  : (9,4,0),
    10 : (10,6,5,3,2,1,0),
    11 : (11,2,0),
    12 : (12,7,6,5,3,1,0),
    13 : (13,4,3,1,0),
    14 : (14,7,5,3,0),
    15 : (15,5,4,2,0),
    16 : (16,5,3,2,0),
    17 : (17,3,0),
    18 : (18,12,10,1,0),
    19 : (19,5,2,1,0),
    20 : (20,10,9,7,6,5,4,1,0),
    21 : (21,6,5,2,0),
    22 : (22,12,11,10,9,8,6,5,0),
    23 : (23,5,0),
    24 : (24,16,15,14,13,10,9,7,5,3,0),
    25 : (25,8,6,2,0),
    26 : (26,14,10,8,7,6,4,1,0),
    27 : (27,12,10,9,7,5,3,2,0),
    28 : (28,13,7,6,5,2,0),
    29 : (29,2,0),
    30 : (30,17,16,13,11,7,5,3,2,1,0),
    31 : (31,3,0),
    32 : (32,15,9,7,4,3,0),
    33 : (33,13,12,11,10,8,6,3,0),
    34 : (34,16,15,12,11,8,7,6,5,4,2,1,0),
    35 : (35, 11, 10, 7, 5, 2, 0),
    36 : (36, 23, 22, 20, 19, 17, 14, 13, 8, 6, 5, 1, 0),
    37 : (37, 5, 4, 3, 2, 1, 0),
    38 : (38, 14, 10, 9, 8, 5, 2, 1, 0),
    39 : (39, 15, 12, 11, 10, 9, 7, 6, 5, 2 , 0),
    40 : (40, 23, 21, 18, 16, 15, 13, 12, 8, 5, 3, 1, 0),
    97 : (97,6,0),
    100 : (100,15,0)
    }
#generating actual primitives for GField using the above dictionary:
# e.g. if gPrimitivePolysCondensed[3] = (3,1,0) => the polynomial is x^3+x+1
# and this polynomial is stored as gPrimitivePolys[3]=[1,0,1,1]

for n in gPrimitivePolysCondensed.keys():
    gPrimitivePolys[n] = [0]*(n+1)
    if (n < 16):
        unity = 1
    else:
        unity = long(1)
    for index in gPrimitivePolysCondensed[n]:
        gPrimitivePolys[n][index] = unity
    gPrimitivePolys[n].reverse()
                
class GField:
	def __init__(self,n,useLUT):
		self.n = n
		self.generator = self.ConvertListToElement(gPrimitivePolys[n])
		
		if (useLUT == 1 or (useLUT == -1 and self.n < 10)): # use lookup table
			self.unity = 1
			self.Inverse = self.DoInverseForSmallField            
			self.PrepareLUT()
			self.Multiply = self.LUTMultiply
			self.Divide = self.LUTDivide
			self.Inverse = lambda x: self.LUTDivide(1,x)            
		elif (self.n < 15):
			self.unity = 1
			self.Inverse = self.DoInverseForSmallField            
			self.Multiply = self.DoMultiply
			self.Divide = self.DoDivide
		else: # Need to use longs for larger fields
			self.unity = long(1)
			self.Inverse = self.DoInverseForBigField            
			self.Multiply = lambda a,b: self.DoMultiply(long(a),long(b))
			self.Divide = lambda a,b: self.DoDivide(long(a),long(b))



	def PrepareLUT(self):
		fieldSize = 1 << self.n
		lutName = 'ffield.lut.' + `self.n`
		if (os.path.exists(lutName)):
			fd = open(lutName,'r')
			self.lut = cPickle.load(fd)
			fd.close()
		else:
			self.lut = LUT()
			self.lut.mulLUT = range(fieldSize)
			self.lut.divLUT = range(fieldSize)
			self.lut.mulLUT[0] = [0]*fieldSize
			self.lut.divLUT[0] = ['NaN']*fieldSize
			for i in range(1,fieldSize):
				self.lut.mulLUT[i] = map(lambda x: self.DoMultiply(i,x),
                                        range(fieldSize))
				self.lut.divLUT[i] = map(lambda x: self.DoDivide(i,x),
                                         range(fieldSize))
			fd = open(lutName,'w')
			cPickle.dump(self.lut,fd)
			fd.close()


	def LUTMultiply(self,i,j):
		return self.lut.mulLUT[i][j]

	def LUTDivide(self,i,j):
		return self.lut.divLUT[i][j]
        
	def Add(self,x,y):
		return x ^ y

	def Subtract(self,x,y):
		return self.Add(x,y)

	def DoMultiply(self,f,v):
		m = self.MultiplyWithoutReducing(f,v)
		return self.FullDivision(m,self.generator,self.FindDegree(m),self.n)[1]

	def DoDivide(self,f,v):
		return self.DoMultiply(f,self.Inverse(v))

	
	def ConvertListToElement(self,l):
		temp = map(lambda a, b: a << b, l, range(len(l)-1,-1,-1))
		return reduce(lambda a, b: a | b, temp)


	def MultiplyWithoutReducing(self,f,v):        
		result = 0
		mask = self.unity
		i = 0
		while (i <= self.n):
			if (mask & v): 
				result = result ^ f
			f = f << 1
			mask = mask << 1
			i = i + 1
		return result

	def FullDivision(self,f,v,fDegree,vDegree):
		result = 0
		i = fDegree
		mask = self.unity << i
		while (i >= vDegree):
			if (mask & f):
				result = result ^ (self.unity << (i - vDegree))
				f = self.Subtract(f, v << (i - vDegree))
			i = i - 1
			mask = mask >> self.unity
		return (result,f)

	def FindDegree(self,v):
		if (v):
			result = -1
			while(v):
				v = v >> 1
				result = result + 1
			return result
		else:
			return 0

	def DoInverseForSmallField(self,f):
		return self.ExtendedEuclid(1,f,self.generator,
                                   self.FindDegree(f),self.n)[1]

	def DoInverseForBigField(self,f):
		return self.ExtendedEuclid(self.unity,long(f),self.generator,
                                   self.FindDegree(long(f)),self.n)[1]

	def ExtendedEuclid(self,d,a,b,aDegree,bDegree):
		if (b == 0):
			return (a,self.unity,0)
		else:
			(floorADivB, aModB) = self.FullDivision(a,b,aDegree,bDegree)
			(d,x,y) = self.ExtendedEuclid(d, b, aModB, bDegree,
                                          self.FindDegree(aModB))
			return (d,y,self.Subtract(x,self.DoMultiply(floorADivB,y)))




