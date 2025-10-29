from errno import EEXIST
from os import makedirs, path
import os

import numpy as np
from plyfile import PlyData, PlyElement

def mkdir_p(folder_path):
    # Creates a directory. equivalent to using mkdir -p on the command line
    try:
        makedirs(folder_path)
    except OSError as exc: # Python >2.5
        if exc.errno == EEXIST and path.isdir(folder_path):
            pass
        else:
            raise


def save_ply(self, path):
    mkdir_p(os.path.dirname(path))

    xyz = self._xyz.detach().cpu().numpy()
    normals = np.zeros_like(xyz)
    f_dc = self._features_dc.detach().transpose(1, 2).flatten(start_dim=1).contiguous().cpu().numpy()
    f_rest = self._features_rest.detach().transpose(1, 2).flatten(start_dim=1).contiguous().cpu().numpy()
    opacities = self._opacity.detach().cpu().numpy()
    scale = self._scaling.detach().cpu().numpy()
    rotation = self._rotation.detach().cpu().numpy()

    dtype_full = [(attribute, 'f4') for attribute in self.construct_list_of_attributes()]

    elements = np.empty(xyz.shape[0], dtype=dtype_full)
    attributes = np.concatenate((xyz, normals, f_dc, f_rest, opacities, scale, rotation), axis=1)
    elements[:] = list(map(tuple, attributes))
    el = PlyElement.describe(elements, 'vertex')
    PlyData([el]).write(path)