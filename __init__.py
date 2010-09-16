import sys, os, threading, time

PLUGIN_PATH = os.path.join(__path__[0], 'bin', 'plugins')
BIN_PATH = os.path.join(__path__[0], 'bin')

sys.path.append(BIN_PATH)

if sys.platform == 'win32':
    # preload some dlls so users do not have to mess about with path
    import ctypes
    # for dll in ['Iex','Half','IlmThread','IlmImf','mingwm10',
                # 'libfreetype-6','iconv','libxml2','libtiff-3',
                # 'libyafaraycore', 'libyafarayplugin']:
    for dll in ['zlib1','libxml2','pthreadVC2','yafaraycore','yafarayplugin']:
        try:
            ctypes.cdll.LoadLibrary(os.path.join(BIN_PATH, dll))
        except Exception as e:
            print("ERROR: Failed to load library " + dll + ", " + repr(e));

import bpy

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
    import io, ui, op
    io.register()
    for submodule in [ui, op]:
        for element in dir(submodule):
            try:
                 getattr(getattr(submodule, element), 'register')()
            except AttributeError as e:
                 pass

    return
"""
    try:
        import io, ui, op
    except:
        print("Could not import subpackages, delay loading...")
        def delayload():
            time.sleep(1)
            print("trying to register again...")
            register()
        t = threading.Thread(target=delayload)
        t.start()
        return

    io.register()
    for submodule in [ui, op]:
        for element in dir(submodule):
            try:
                getattr(getattr(submodule, element), 'register')()
            except AttributeError as e:
                pass
"""
    
def unregister():
    pass
"""
    import io, ui, op
    io.unregister()
    for submodule in [ui, op]:
        for element in dir(submodule):
            try:
                getattr(getattr(submodule, element), 'unregister')()
            except AttributeError:
                pass
"""    
if __name__ == '__main__':
    register()