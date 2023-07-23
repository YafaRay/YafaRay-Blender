# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import mathutils


def multiply_matrix4x4_vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    if bpy.app.version >= (2, 80, 0):
        for i in range(4):
            result[i] = vector @ matrix[i]  # use reverse vector multiply order, API changed with rev. 38674
    else:
        for i in range(4):
            result[i] = vector * matrix[i]  # use reverse vector multiply order, API changed with rev. 38674

    return result
