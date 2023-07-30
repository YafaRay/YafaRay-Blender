# SPDX-License-Identifier: GPL-2.0-or-later

import bpy


class RenderPresetsBase:
    name: bpy.props.StringProperty(name="Name", description="Name of the preset, used to make the path name",
                                    maxlen=64, default="")
    remove_active: bpy.props.BoolProperty(default=False, options={'HIDDEN'})
