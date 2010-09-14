import sys, os

PLUGIN_PATH = os.path.join(__path__[0], 'bin', 'plugins')
BIN_PATH = os.path.join(__path__[0], 'bin')

sys.path.append(BIN_PATH)

if sys.platform == 'win32':
    # preload some dlls so users do not have to mess about with path
    import ctypes
    for dll in ['zlib1','libxml2','pthreadVC2','yafaraycore','yafarayplugin']:
        try:
            ctypes.cdll.LoadLibrary(os.path.join(BIN_PATH, dll))
        except Exception as e:
            print("ERROR: Failed to load library " + dll + ", " + repr(e));

import bpy
import io, ui, op

bl_addon_info = {
    "name": "YafaRay Integration",
    "author": "Shuvro Sarker",
    "version": "0.1.2 alpha",
    "blender": (2, 5, 4),
    "category": "Render",
    "warning" : "VERY ALPHA!",
    "description": "YafaRay integration for blender 2.5. When activated, YafaRay will be available in the Render Engine dropdown"
    }

def register():
    io.register()
    for submodule in [ui, op]:
        for element in dir(submodule):
            try:
                getattr(getattr(submodule, element), 'register')()
            except AttributeError as e:
                pass
    
def unregister():
    io.unregister()
    for submodule in [ui, op]:
        for element in dir(submodule):
            try:
                getattr(getattr(submodule, element), 'unregister')()
            except AttributeError:
                pass
    
if __name__ == '__main__':
    register()