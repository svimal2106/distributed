class LUT:
    """
    Lookup table used to speed up some finite field operations.
    """
    pass


class FElement:
    """
    This class provides field elements which overload the
    +,-,*,%,//,/ operators to be the appropriate field operation.
    Note that before creating FElement objects you must first
    create an FField object.  For example,
    
>>> import ffield
>>> F = FField(5)
>>> e1 = FElement(F,7)
>>> e1
x^2 + x^1 + 1
>>> e2 = FElement(F,19)
>>> e2
x^4 + x^1 + 1
>>> e3 = e1 + e2
>>> e3
x^4 + x^2
>>> e4 = e3 / e2
>>> e4
x^4 + x^3
>>> e4 * e2 == (e3)
1
    
    """
    
    def __init__(self,field,e):
        """
        The constructor takes two arguments, field, and e where
        field is an FField object and e is an integer representing
        an element in FField.

        The result is a new FElement instance.
        """
        self.f = e
        self.field = field
        
    def __add__(self,other):
        assert self.field == other.field
        return FElement(self.field,self.field.Add(self.f,other.f))

    def __mul__(self,other):
        assert self.field == other.field
        return FElement(self.field,self.field.Multiply(self.f,other.f))

    def __mod__(self,o):
        assert self.field == o.field
        return FElement(self.field,
                        self.field.FullDivision(self.f,o.f,
                                                self.field.FindDegree(self.f),
                                                self.field.FindDegree(o.f))[1])

    def __floordiv__(self,o):
        assert self.field == o.field
        return FElement(self.field,
                        self.field.FullDivision(self.f,o.f,
                                                self.field.FindDegree(self.f),
                                                self.field.FindDegree(o.f))[0])

    def __div__(self,other):
        assert self.field == other.field
        return FElement(self.field,self.field.Divide(self.f,other.f))

    def __str__(self):
        return self.field.ShowPolynomial(self.f)

    def __repr__(self):
        return self.__str__()

    def __eq__(self,other):
        assert self.field == other.field
        return self.f == other.f
