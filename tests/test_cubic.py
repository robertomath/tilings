import unittest

from tiling3 import cubic_tiling


class CubicTilingTest(unittest.TestCase):

    def setUp(self):
        self.tiling = cubic_tiling(1,8,2,8,3,8)
    
    def test_size(self):
        self.assertEqual(len(self.tiling.vertices), 8*7*6)
        self.assertEqual(len(self.tiling.edges), 8*7*5 + 8*6*6 + 7*7*6)
        self.assertEqual(len(self.tiling.faces), 8*6*5 + 7*7*5 + 7*6*6)
        self.assertEqual(len(self.tiling.volumes), 7*6*5)
