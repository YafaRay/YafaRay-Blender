# SPDX-License-Identifier: GPL-2.0-or-later

import bpy


def scene_from_depsgraph(depsgraph):
    if bpy.app.version >= (2, 80, 0):
        return depsgraph.scene
    else:
        return depsgraph
