from matrix import Matrix
m = Matrix(4,4)
#m.display()
#rep = m.replicate()

#rep.display()
tr = m.replicate()
#tr.display()
tr.setrow(0,[1.0,2.0,4.0,8.0])
tr.setrow(1,[1.0,3.0,9.0,27.0])
tr.setrow(2,[1.0,4.0,16.0,64.0])
tr.setrow(3,[1.0,5.0,25.0,125.0])
tr.display()

#tr.setrow(3,[2,3,4])
#tr.appendidentity()
##tr.matrix[0].append(3)
#tr.display()
#tr.lowerdecomposition()
##tr.swaprows(1,3)
#tr.display()
#tr.upperdecomposition()
#tr.display()
inv = tr.inverse()
inv.display()
print inv.determinant()
print tr.determinant()
