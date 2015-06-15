from math import floor, ceil

from vector3 import Vector3


class Tiling3():
    """
    Base class for a 3D tiling.
    """
    
    def __init__(self, v=None, e=None, f=None, g=None):
        if v is None:
            self.vertices = set()
        else:
            self.vertices = set(v)
        if e is None:
            self.edges = set()
        else:
            self.edges = set(e)
        if f is None:
            self.faces = set()
        else:
            self.faces = set(f)
        if g is None:
            self.volumes = set()
        else:
            self.volumes = set(g)
            
    def minx(self):
        return min(v.x for v in self.vertices)
    
    def maxx(self):
        return max(v.x for v in self.vertices)
    
    def miny(self):
        return min(v.y for v in self.vertices)
    
    def maxy(self):
        return max(v.y for v in self.vertices)
    
    def minz(self):
        return min(v.z for v in self.vertices)
    
    def maxz(self):
        return max(v.z for v in self.vertices)

    def deform(self, h):
        """
        Applies an arbitrary function h to the vertices.
        """
        v = dict((a,h(a)) for a in self.vertices)
        e = dict((a,frozenset(v[i] for i in a)) for a in self.edges)
        f = dict((a,frozenset(e[i] for i in a)) for a in self.faces)
        g = dict((a,frozenset(f[i] for i in a)) for a in self.volumes)
        return Tiling3(frozenset(v.itervalues()),frozenset(e.itervalues()),frozenset(f.itervalues()),frozenset(g.itervalues()))
            
    def translate(self, offset):
        return self.deform(lambda x: x+offset)
            
    def scale(self, scalar):
        return self.deform(lambda x: x*scalar)

    def transform(self, matrix):
        return self.deform(matrix) # matrix action is overloaded function call

    def sort_out_duplicates(self, epsilon=0.000001):
        l = list(self.vertices)
        d = {}
        for (i,v1) in enumerate(l):
            for v2 in reversed(l[i+1:]):
                if v1.distance(v2) < epsilon:
                    d[v1] = v2
                    break
        return self.deform(lambda v: d.get(v,v))            

    def union(self, other, epsilon=0.000001):
        u = Tiling3(self.vertices.union(other.vertices),
                    self.edges.union(other.edges),
                    self.faces.union(other.faces),
                    self.volumes.union(other.volumes))
        return u.sort_out_duplicates(epsilon)

    def clip(self, minx, maxx, miny, maxy, minz, maxz):
        """
        Take only the structure that intersects the box with given
        coordinates.
        """
        newv = set(v for v in self.vertices if minx <= v.x <= maxx and miny <= v.y <= maxy and minz <= v.z <= maxz)
        newe = set(e for e in self.edges if any(v in newv for v in e))
        newf = set(f for f in self.faces if any(e in newe for e in f))
        newg = set(g for g in self.volumes if any(f in newf for f in g))
        return Tiling3(newv, newe, newf, newg)


def big_union3(tilings, epsilon=0.000001):
    v = set()
    e = set()
    f = set()
    g = set()
    for t in tilings:
        v.update(t.vertices)
        e.update(t.edges)
        f.update(t.faces)
        g.update(t.volumes)
    return Tiling3(v,e,f,g).sort_out_duplicates(epsilon)


def unit_cube():
    """
    A Tiling3 representing the unit cube. There should be some more
    conceptual (and less unsightly) way of producing it.
    """
    
    vertices = dict(((i,j,k),Vector3(i,j,k)) for i in [0,1] for j in [0,1] for k in [0,1])
    edges = dict([((None,j,k),frozenset([vertices[(0,j,k)],vertices[(1,j,k)]])) for j in [0,1] for k in [0,1]] +
                 [((i,None,k),frozenset([vertices[(i,0,k)],vertices[(i,1,k)]])) for i in [0,1] for k in [0,1]] +
                 [((i,j,None),frozenset([vertices[(i,j,0)],vertices[(i,j,1)]])) for i in [0,1] for j in [0,1]])
    faces = ([frozenset([edges[None,0,k], edges[0,None,k], edges[None,1,k], edges[1,None,k]]) for k in [0,1]] +
             [frozenset([edges[None,j,0], edges[0,j,None], edges[None,j,1], edges[1,j,None]]) for j in [0,1]] +
             [frozenset([edges[i,None,0], edges[i,0,None], edges[i,None,1], edges[i,1,None]]) for i in [0,1]])
    return Tiling3(vertices.itervalues(), edges.itervalues(), faces, [frozenset(faces)])


def cubic_tiling(minx,maxx,miny,maxy,minz,maxz):
    """
    A Tiling3 representing a cubic tiling.
    """
    minx = int(floor(minx))
    maxx = int(ceil(maxx))
    miny = int(floor(miny))
    maxy = int(ceil(maxy))
    minz = int(floor(minz))
    maxz = int(ceil(maxz))

    c = unit_cube()
    
    return big_union3(c.translate(Vector3(x,y,z))
                      for x in xrange(minx,maxx)
                      for y in xrange(miny,maxy)
                      for z in xrange(minz,maxz))
