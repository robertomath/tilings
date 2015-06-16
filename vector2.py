from math import sqrt


class Vector2():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector2(%f, %f)"%(self.x, self.y)
        
    def __hash__(self):
        return hash((Vector2, self.x, self.y))
        
    def __getitem__(self, n):
        if n == 1:
            return self.x
        elif n == 2:
            return self.y
        else:
            raise IndexError("Vector2 has components 1, 2 only.")

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, s):
        return Vector2(self.x*s, self.y*s)

    def __div__(self, s):
        return Vector2(self.x/s, self.y/s)
    
    def norm(self):
        return sqrt(self.x*self.x + self.y*self.y)
    
    def distance(self, other):
        return (self-other).norm()
