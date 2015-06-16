import unittest

from restrict32 import restrict32
from tiling3 import cubic_tiling
from vector3 import Vector3


class CubicTilingTest(unittest.TestCase):

    def setUp(self):
        self.tiling = cubic_tiling(1,8,2,8,3,8)
    
    def test_size(self):
        t = self.tiling
        self.assertEqual(len(t.vertices), 8*7*6)
        self.assertEqual(len(t.edges), 8*7*5 + 8*6*6 + 7*7*6)
        self.assertEqual(len(t.faces), 8*6*5 + 7*7*5 + 7*6*6)
        self.assertEqual(len(t.volumes), 7*6*5)

    def test_useless_clip(self):
        t1 = self.tiling
        t2 = self.tiling.clip(0,10,0,10,0,10)
        self.assertEqual(t1.vertices, t2.vertices)
        self.assertEqual(t1.edges, t2.edges)
        self.assertEqual(t1.faces, t2.faces)
        self.assertEqual(t1.volumes, t2.volumes)

    def test_restrict(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        self.assertEqual(len(t.vertices), 8*7)
        self.assertEqual(len(t.edges), 8*6 + 7*7)
        self.assertEqual(len(t.faces), 7*6)

    def test_restrict_then_useless_clip(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5))).clip(0,10,0,10)
        self.assertEqual(len(t.vertices), 8*7)
        self.assertEqual(len(t.edges), 8*6 + 7*7)
        self.assertEqual(len(t.faces), 7*6)
