from math import floor, ceil

from vector2 import Vector2


class Tiling2():
    """
    Base class for a 3D tiling.
    """
    
    def __init__(self, v=None, e=None, f=None):
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
            
    def minx(self):
        return min(v.x for v in self.vertices)
    
    def maxx(self):
        return max(v.x for v in self.vertices)
    
    def miny(self):
        return min(v.y for v in self.vertices)
    
    def maxy(self):
        return max(v.y for v in self.vertices)
    
    def deform(self, h):
        """
        Applies an arbitrary function h to the vertices.
        """
        v = dict((a,h(a)) for a in self.vertices)
        e = dict((a,frozenset(v[i] for i in a)) for a in self.edges)
        f = dict((a,frozenset(e[i] for i in a)) for a in self.faces)
        return Tiling2(frozenset(v.itervalues()),frozenset(e.itervalues()),frozenset(f.itervalues()))
            
    def translate(self, offset):
        return self.deform(lambda x: x+offset)
            
    def scale(self, scalar):
        return self.deform(lambda x: x*scalar)

    def sort_out_duplicates(self, epsilon=0.000001):
        """
        Replace very close vertices by the same vertex.

        This is more efficient than before: we sort by x
        coordinate. In groups where the x coordinates are close, we
        sort by y coordinate. Consecutive pairs where that is also
        close are identified.
        """
        lx = sorted(self.vertices, key=lambda v:v.x)
        d = {}
        i1 = 0
        while i1 < len(lx):
            i2 = i1+1
            while i2 < len(lx) and abs(lx[i2-1].x-lx[i2].x) < epsilon:
                i2 += 1
            ly = sorted(lx[i1:i2], key=lambda v:v.y)
            for j in xrange(1,len(ly)):
                if abs(ly[j-1].y-ly[j].y) < epsilon:
                    d[ly[j]] = d.get(ly[j-1],ly[j-1])
            i1 = i2
        return self.deform(lambda v: d.get(v,v))            

    def union(self, other, epsilon=0.000001):
        u = Tiling2(self.vertices.union(other.vertices),
                    self.edges.union(other.edges),
                    self.faces.union(other.faces))
        return u.sort_out_duplicates(epsilon)

    def clip(self, minx, maxx, miny, maxy):
        """
        Take only the structure that intersects the box with given
        coordinates.
        """
        newv = set(v for v in self.vertices if minx <= v.x <= maxx and miny <= v.y <= maxy)
        newe = set(e for e in self.edges if any(v in newv for v in e))
        newf = set(f for f in self.faces if any(e in newe for e in f))
        return Tiling2(newv, newe, newf)

    def write_eps(self, f, psbox, geobox):
        (gminx, gmaxx, gminy, gmaxy) = geobox
        (pminx, pmaxx, pminy, pmaxy) = psbox
        def coords(v):
            x = (v.x-gminx)*(pmaxx-pminx)/(gmaxx-gminx) + pminx
            y = (v.y-gminy)*(pmaxy-pminy)/(gmaxy-gminy) + pminy
            return "%f %f"%(x,y)
        f.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        f.write("%%%%BoundingBox: %d %d %d %d\n"%psbox)
        for (v1,v2) in self.edges:
            f.write("newpath " + coords(v1) + " moveto " + coords(v2) + " lineto stroke\n")

def big_union2(tilings, epsilon=0.000001):
    v = set()
    e = set()
    f = set()
    for t in tilings:
        v.update(t.vertices)
        e.update(t.edges)
        f.update(t.faces)
    return Tiling2(v,e,f).sort_out_duplicates(epsilon)


