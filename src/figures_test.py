# Copyright (c) 2023 Ruiqi Chen
# Email: rchensix at alumni dot stanford dot edu
# MIT License.
# See LICENCE file for full license terms.

# This file contains the tests used to generate the meshes for the figures in
# the manuscript, as well as some miscellaneous meshes for testing.

import unittest

import numpy as np

import mesh_utils
import signed_distance
import tet_symmetry

class TestFigures(unittest.TestCase):
    def test_basic(self):
        '''Simple test with small N. Geometry is Schwarz-P.
        '''
        n = 4
        v = np.arange(-n // 2, n // 2) / n
        x, y, z = np.meshgrid(v, v, v, indexing='ij')
        data = np.cos(2.0 * np.pi * x) + np.cos(2.0 * np.pi * y) + \
               np.cos(2.0 * np.pi * z)
        ts = tet_symmetry.TetSymmetry(data, normal_to_face=True)
        # Evaluate numerical gradient on a tet face.
        face_center = np.mean(tet_symmetry.kUnitTetPts[1:], axis=0)
        n = np.array([1, 1, 1])
        step = 1e-3
        xvec = np.array([face_center[0], face_center[0] + step])
        yvec = np.array([face_center[1], face_center[1] + step])
        zvec = np.array([face_center[2], face_center[2] + step])
        xgrid, ygrid, zgrid = np.meshgrid(xvec, yvec, zvec, indexing='ij')
        vals = ts.EvaluateNaive(xgrid, ygrid, zgrid)
        grad = np.array([vals[1, 0, 0] - vals[0, 0, 0],
                         vals[0, 1, 0] - vals[0, 0, 0],
                         vals[0, 0, 1] - vals[0, 0, 0]])
        self.assertLess(grad.dot(n), 1e-6)

if __name__ == '__main__':
    unittest.main()