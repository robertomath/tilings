from math import sin, cos

from vector3 import Vector3


class Matrix3():

    def __init__(self, l):
        ((a,b,c),(d,e,f),(g,h,i)) = l
        self.array = ((a,b,c),(d,e,f),(g,h,i))

    def __getitem__(self, (r, s)):
        return self.array[r-1][s-1]

    def __add__(self, other):
        return Matrix3([[self[(i,j)]+other[(i,j)] for j in [1,2,3]] for i in [1,2,3]])

    def __mul__(self, other):
        "Matrix multiplication"
        return Matrix3([[sum(self[(i,k)]*other[(k,j)] for k in [1,2,3]) for j in [1,2,3]] for i in [1,2,3]])

    def __call__(self, other):
        "Matrix acting on a vector"
        [a,b,c] = [sum(self[(i,j)]*other[j] for j in [1,2,3]) for i in [1,2,3]]
        return Vector3(a,b,c)


def rotate_x(theta):
    return Matrix3([[1,0,0],[0,cos(theta),sin(theta)],[0,-sin(theta),cos(theta)]])

def rotate_y(theta):
    return Matrix3([[cos(theta),0,sin(theta)],[0,1,0],[-sin(theta),0,cos(theta)]])

def rotate_z(theta):
    return Matrix3([[cos(theta),sin(theta),0],[-sin(theta),cos(theta),0],[0,0,1]])

