# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

if bpy.app.version >= (2, 93, 0):
    from bpy.props import _PropertyDeferred


def replace_properties_with_annotations(class_to_decorate):
    # Replace class properties with annotations for Blender 2.80 and higher
    if bpy.app.version >= (2, 80, 0):
        properties_to_delete = []
        if not hasattr(class_to_decorate, '__annotations__'):
            class_to_decorate.__annotations__ = {}
        if bpy.app.version >= (2, 93, 0):
            property_filter = _PropertyDeferred
        else:
            property_filter = tuple

        for property_name, property_ in class_to_decorate.__dict__.items():
            if not property_name.startswith("__") and isinstance(property_, property_filter):
                # print("moving class_.__annotations__[", property_name, "] = ", property_, "")
                class_to_decorate.__annotations__[property_name] = property_
                properties_to_delete.append(property_name)
        for property_name in properties_to_delete:
            delattr(class_to_decorate, property_name)

    return class_to_decorate
