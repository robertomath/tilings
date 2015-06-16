import unittest

from restrict32 import restrict32
from tiling3 import cubic_tiling
from vector2 import Vector2
from vector3 import Vector3


class CubicTilingTest(unittest.TestCase):

    def setUp(self):
        self.tiling = cubic_tiling(1,8,2,8,3,8)

    def type_tiling2(self, t):
        """
        Check that a 2D tiling is made of the things it is supposed to.
        """
        self.assertIsInstance(t.vertices, set, "vertices should form a set")
        for v in t.vertices:
            self.assertIsInstance(v, Vector2, "vertices should be 2-vectors")
        self.assertIsInstance(t.edges, set, "edges should form a set")
        for e in t.edges:
            self.assertIsInstance(e, frozenset, "edges should be frozensets")
            for v in e:
                self.assertIsInstance(v, Vector2, "edges should be made up of vertices")
        self.assertIsInstance(t.faces, set, "faces should form a set")
        for f in t.faces:
            self.assertIsInstance(f, frozenset, "faces should be frozensets")
            for e in f:
                self.assertIsInstance(e, frozenset, "faces should be made up of frozensets")
                for v in e:
                    self.assertIsInstance(v, Vector2, "faces should be made up of frozensets made up of vertices")

    def type_tiling3(self, t):
        """
        Check that a 3D tiling is made of the things it is supposed to.
        """
        self.assertIsInstance(t.vertices, set, "vertices should form a set")
        for v in t.vertices:
            self.assertIsInstance(v, Vector3, "vertices should be 3-vectors")
        self.assertIsInstance(t.edges, set, "edges should form a set")
        for e in t.edges:
            self.assertIsInstance(e, frozenset, "edges should be frozensets")
            for v in e:
                self.assertIsInstance(v, Vector3, "edges should be made up of vertices")
        self.assertIsInstance(t.faces, set, "faces should form a set")
        for f in t.faces:
            self.assertIsInstance(f, frozenset, "faces should be frozensets")
            for e in f:
                self.assertIsInstance(e, frozenset, "faces should be made up of frozensets")
                for v in e:
                    self.assertIsInstance(v, Vector3, "faces should be made up of frozensets made up of vertices")
        self.assertIsInstance(t.volumes, set, "volumes should form a set")
        for g in t.faces:
            self.assertIsInstance(g, frozenset, "volumes should be frozensets")
            for f in g:
                self.assertIsInstance(f, frozenset, "volumes should be made up of frozensets")
                for e in f:
                    self.assertIsInstance(e, frozenset, "volumes should be made up of frozensets made up of frozensets")
                    for v in e:
                        self.assertIsInstance(v, Vector3, "volumes should be made up of frozensets made up of frozensets made up of vertices")

    def test_type(self):
        self.type_tiling3(self.tiling)
                        
    def test_size(self):
        t = self.tiling
        self.assertEqual(len(t.vertices), 8*7*6)
        self.assertEqual(len(t.edges), 8*7*5 + 8*6*6 + 7*7*6)
        self.assertEqual(len(t.faces), 8*6*5 + 7*7*5 + 7*6*6)
        self.assertEqual(len(t.volumes), 7*6*5)

    def test_clip_type(self):
        self.type_tiling3(self.tiling.clip(2.5,7.5,2.5,7.5,2.5,7.5))
        
    def test_useless_clip(self):
        t1 = self.tiling
        t2 = self.tiling.clip(0,10,0,10,0,10)
        self.assertEqual(t1.vertices, t2.vertices)
        self.assertEqual(t1.edges, t2.edges)
        self.assertEqual(t1.faces, t2.faces)
        self.assertEqual(t1.volumes, t2.volumes)

    def test_restrict_type(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        self.type_tiling2(t)
        
    def test_restrict(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        self.assertEqual(len(t.vertices), 8*7)
        self.assertEqual(len(t.edges), 8*6 + 7*7)
        self.assertEqual(len(t.faces), 7*6)

    def test_restrict_then_clip_type(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        t = t.clip(1.5,8.5,1.5,8.5)
        self.type_tiling2(t)
        
    def test_restrict_then_useless_clip(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        t = t.clip(0,10,0,10)
        self.assertEqual(len(t.vertices), 8*7)
        self.assertEqual(len(t.edges), 8*6 + 7*7)
        self.assertEqual(len(t.faces), 7*6)
