# SPDX-License-Identifier: GPL-2.0-or-later

# TODO: Use Blender enumerators if any
import bpy
import libyafaray4_bindings

yaf_logger = libyafaray4_bindings.Logger()
yaf_logger.set_console_verbosity_level(yaf_logger.log_level_from_string("debug"))
yaf_logger.set_log_verbosity_level(yaf_logger.log_level_from_string("debug"))


class RenderEngine(bpy.types.RenderEngine):
    # These members are used by blender to set up the
    # RenderEngine; define its internal name, visible name and capabilities.
    bl_idname = 'YAFARAY4_RENDER'
    bl_label = "YafaRay v4 Render"
    bl_use_preview = True  # Render engine supports being used for rendering previews of materials, lights and worlds
    bl_use_shading_nodes_custom = False  # Expose Blender shading nodes in the node editor user interface
    bl_use_shading_nodes = True  # Expose Blender shading nodes in the node editor user interface

    # Init is called whenever a new render engine instance is created. Multiple
    # instances may exist at the same time, for example for a viewport and final
    # render.
    def __init__(self):
        self.yaf_logger = yaf_logger
        print("__init__", self)

    # When the render engine instance is destroy, this is called. Clean up any
    # render engine data here, for example stopping running render threads.
    def __del__(self):
        print("__del__", self)

    # Blender callback. Export scene data for render
    def update(self, bl_data=None, bl_depsgraph=None):
        self.update_stats("", "Setting up render")
        print("update", self, bl_data, bl_depsgraph)

    # Blender callback. Render scene into an image
    # This is the method called by Blender for both final renders (F12) and
    # small preview for materials, world and lights.
    def render(self, bl_depsgraph):
        self.update_stats("", "Done!")
        print("render", self, bl_depsgraph)

    # Blender callback. Perform finishing operations after all view layers in a frame were rendered
    def render_frame_finish(self):
        print("render_frame_finish", self)

    # Blender callback. Draw render image
#    def draw(self, bl_context, bl_depsgraph):
#        print("draw", self, bl_context, bl_depsgraph)

    # Blender callback. Bake passes
        # Parameters
        #     pass_type (enum in Bake Pass Type Items) – Pass, Pass to bake
        #     pass_filter (int in [0, inf]) – Pass Filter, Filter to combined, diffuse, glossy and transmission passes
        #     width (int in [0, inf]) – Width, Image width
        #     height (int in [0, inf]) – Height, Image height

#    if bpy.app.version >= (2, 80, 0):
#        def bake(self, bl_depsgraph, bl_object, bl_pass_type, bl_pass_filter, bl_width, bl_height):
#            print("bake", self, bl_depsgraph, bl_object, bl_pass_type, bl_pass_filter, bl_width, bl_height)

    # Blender callback. Update on data changes for viewport render
    # For viewport renders, this method gets called once at the start and
    # whenever the scene or 3D viewport changes. This method is where data
    # should be read from Blender in the same thread. Typically a render
    # thread will be started to do the work while keeping Blender responsive.

    if bpy.app.version >= (2, 80, 0):
        def view_update(self, bl_context, bl_depsgraph):
            print("view_update", self, bl_context, bl_depsgraph)

    # Blender callback. Draw viewport render
    # For viewport renders, this method is called whenever Blender redraws
    # the 3D viewport. The renderer is expected to quickly draw the render
    # with OpenGL, and not perform other expensive work.
    # Blender will draw overlays for selection and editing on top of the

    if bpy.app.version >= (2, 80, 0):
        def view_draw(self, bl_context, bl_depsgraph):
            print("view_draw", self, bl_context, bl_depsgraph)

    # Blender callback. Compile shader script node
    #def update_script_node(self, bl_node=None):
    #    print("update_script_node", self, bl_node)

    # Blender callback. Update the render passes that will be generated
    def update_render_passes(self, bl_scene=None, bl_renderlayer=None):
        print("update_render_passes", self, bl_scene, bl_renderlayer)


classes = (
    RenderEngine,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on
    register()

