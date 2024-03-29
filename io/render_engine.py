# SPDX-License-Identifier: GPL-2.0-or-later

import array
import tempfile
import os
import threading
import time


# TODO: Use Blender enumerators if any
import bpy

from .integrator_exporter import export_integrator, export_volume_integrator

if bpy.app.version >= (2, 80, 0):
    import gpu
    from gpu_extras.presets import draw_texture_2d
import libyafaray4_bindings
from ..util.io import scene_from_depsgraph
from .scene_exporter import SceneExporter
from .film_exporter import FilmExporter

if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed,
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the
    # "libyafaray4_bindings" compiled module is installed on. Assuming that the YafaRay-Plugin exporter is installed
    # in a folder named "yafaray4" within the addons Blender directory
    # noinspection PyUnresolvedReferences
    from yafaray4 import global_vars
else:
    from .. import global_vars


logger_render = libyafaray4_bindings.Logger("")
logger_preview = libyafaray4_bindings.Logger("Preview")
scene_render = None #libyafaray4_bindings.Scene(logger_render, "Scene Render")
scene_preview = None #libyafaray4_bindings.Scene(logger_render, "Scene Preview")
surface_integrator_render = None  # libyafaray4_bindings.SurfaceIntegrator(logger, "SurfaceIntegrator1", param_map)
surface_integrator_preview = None
film_render = None  # libyafaray4_bindings.Film(logger, yaf_surface_integrator, "Film1", param_map)
film_view_3d = None
film_preview = None


class RenderEngine(bpy.types.RenderEngine):
    # These members are used by blender to set up the
    # RenderEngine; define its internal name, visible name and capabilities.
    bl_idname = 'YAFARAY4_RENDER'
    bl_label = "YafaRay v4 Render"
    bl_use_preview = True  # Render engine supports being used for rendering previews of materials, lights and worlds

    # Init is called whenever a new render engine instance is created. Multiple
    # instances may exist at the same time, for example for a viewport and final
    # render.
    def __init__(self):
        self.scene_data = None
        self.draw_data = None
        print("__init__", self)

    # When the render engine instance is destroy, this is called. Clean up any
    # render engine data here, for example stopping running render threads.
    def __del__(self):
        print("__del__", self)

    # Blender callback. Export scene data for render
    def update(self, bl_data=None, depsgraph=None):
        self.update_stats("", "Setting up render")
        print("update (is_preview=", self.is_preview, ")", self, bl_data, depsgraph)
        global scene_render
        global scene_preview
        if self.is_preview:
            scene_preview = libyafaray4_bindings.Scene(logger_preview, "Scene Preview")  # FIXME: this needs to be handled differently for scene reuse
            scene_yafaray = scene_preview
            logger = logger_preview
        else:
            scene_render = libyafaray4_bindings.Scene(logger_render, "Scene Render")  # FIXME: this needs to be handled differently for scene reuse
            scene_yafaray = scene_render
            logger = logger_render
        scene_exporter = SceneExporter(self.is_preview, depsgraph, scene_yafaray, logger)
        scene_exporter.export_scene()

    # Blender callback. Render scene into an image
    # This is the method called by Blender for both final renders (F12) and
    # small preview for materials, world and lights.
    def render(self, depsgraph):
        print("render", self, depsgraph)
        scene_blender = scene_from_depsgraph(depsgraph)
        if self.is_preview:
            scene_yafaray = scene_preview
            logger = logger_preview
        else:
            scene_yafaray = scene_render
            logger = logger_render
        scale = scene_blender.render.resolution_percentage / 100.0
        size_x = int(scene_blender.render.resolution_x * scale)
        size_y = int(scene_blender.render.resolution_y * scale)

        # Creating surface integrator #
        surface_integrator = export_integrator("SurfaceIntegrator1", scene_blender, logger)

        # Creating Film #
        film = FilmExporter("Film1", self, scene_blender, surface_integrator, logger, self.is_preview)
        param_map = libyafaray4_bindings.ParamMap()
        film.export_aa(scene_blender, param_map)
        film.export_render_settings(depsgraph, "", "")

        # Creating camera #
        film.define_camera(scene_blender.camera, scene_blender.render.resolution_x, scene_blender.render.resolution_y,
                           scene_blender.render.resolution_percentage, global_vars.use_view_to_render, global_vars.view_matrix)

        # Creating image output #
        # param_map.clear()
        # param_map.set_string("image_path", "./test01-output1.tga")
        # film.film_yafaray.create_output("output1_tga", param_map)

        if bpy.data.filepath == "":
            render_filename = "render"
            render_path = tempfile.gettempdir() + "/temp_render/"
        else:
            render_filename = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
            render_path = "//" + render_filename + "_render/"

        render_filename += " - " + str(scene_blender.frame_current)

        if scene_blender.img_save_with_blend_file:
            scene_blender.render.filepath = render_path
            render_path = bpy.path.abspath(render_path)
        else:
            render_path = bpy.path.abspath(scene_blender.render.filepath)

        render_path = os.path.realpath(render_path)
        render_path = os.path.normpath(render_path)

        if not os.path.exists(render_path):
            os.mkdir(render_path)

        color_space = film.calc_color_space(scene_blender)
        gamma = film.calc_gamma(scene_blender)
        alpha_premultiply = film.calc_alpha_premultiply(scene_blender)

        if scene_blender.gs_type_render == "file":
            # self.setInterface(libyafaray4_bindings.Interface())
            # self.yi.setInputColorSpace("LinearRGB", 1.0)    #When rendering into Blender, color picker floating point data is already linear (linearized by Blender)
            film.define_image_output("blender_file_output", render_path, scene_blender, scene_blender.render, color_space.blender, gamma.blender, alpha_premultiply.blender)
            if scene_blender.yafaray4.logging.save_preset:
                pass  # FIXME
                #yafaray_presets.YAF_AddPresetBase.export_to_file(yafaray_presets.YAFARAY_OT_presets_renderset, self.outputFile)

        elif scene_blender.gs_type_render == "xml" or scene_blender.gs_type_render == "c" or scene_blender.gs_type_render == "python":
            output_file, output, file_type = film.define_image_output(render_path, scene_blender.gs_type_render)
            # self.setInterface(libyafaray4_bindings.Interface(output_file))

            input_color_values_color_space = "sRGB"
            input_color_values_gamma = 1.0

            if scene_blender.display_settings.display_device == "sRGB":
                input_color_values_color_space = "sRGB"

            elif scene_blender.display_settings.display_device == "XYZ":
                input_color_values_color_space = "XYZ"

            elif scene_blender.display_settings.display_device == "None":
                input_color_values_color_space = "Raw_Manual_Gamma"
                input_color_values_gamma = scene_blender.gs_gamma  #We only use the selected gamma if the output device is set to "None"

            # self.yi.setInputColorSpace("LinearRGB", 1.0)    #Values from Blender, color picker floating point data are already linear (linearized by Blender)
            film.define_image_output("xml_file_output", render_path, scene_blender, scene_blender.render, color_space.blender, gamma.blender, alpha_premultiply.blender)
            #FIXME! self.yi.setXmlColorSpace(input_color_values_color_space, input_color_values_gamma)  #To set the XML interface to write the XML values with the correction included for the selected color space (and gamma if applicable)

        else:
            #self.setInterface(libyafaray4_bindings.Interface())
            #self.yi.setInputColorSpace("LinearRGB", 1.0)    #When rendering into Blender, color picker floating point data is already linear (linearized by Blender)
            if scene_blender.gs_secondary_file_output and not self.is_preview:
                film.define_image_output("blender_secondary_output", render_path, scene_blender, scene_blender.render, color_space.secondary_output, gamma.secondary_output, alpha_premultiply.secondary_output)
                if scene_blender.yafaray4.logging.save_preset:
                    pass  # FIXME
                    #yafaray_presets.YAF_AddPresetBase.export_to_file(yafaray_presets.YAFARAY_OT_presets_renderset, self.outputFile)

        # Creating RenderControl #
        render_control = libyafaray4_bindings.RenderControl()

        # Creating RenderMonitor #
        def monitor_callback(steps_total, steps_done, tag):
            # print("*PYTHON MONITOR CALLBACK*", steps_total, steps_done, tag)
            self.update_stats("YafaRay Render: ", "{0}".format(tag))
            # Now, Blender use same range to YafaRay
            if steps_total > 0:
                self.update_progress(steps_done / steps_total)
            else:
                self.update_progress(0.0)

        render_monitor = libyafaray4_bindings.RenderMonitor(monitor_callback)

        film.define_layers(depsgraph)
        render_control.set_for_normal_start()
        scene_modified_flags = scene_yafaray.check_and_clear_modified_flags()
        scene_yafaray.preprocess(render_control, scene_modified_flags)

        # Creating volume integrator #
        export_volume_integrator(surface_integrator, scene_blender.world, scene_yafaray, logger)

        # Preprocess integrator
        surface_integrator.preprocess(render_monitor, render_control, scene_yafaray)

        # Render
        t = threading.Thread(target=surface_integrator.render, args=(render_control, render_monitor, film.film_yafaray,))
        t.start()

        while t.is_alive() and not self.test_break():
            time.sleep(0.2)

        if t.is_alive():
            self.update_stats("",
                              "Aborting, please wait for all pending tasks to complete (progress in console log)...")
            render_control.cancel()
            t.join()

        #if self.is_preview:
        #    self.render_preview(scene_blender, size_x, size_y)
        #else:
        #    self.render_scene(scene_blender, size_x, size_y)
        if global_vars.use_view_to_render:
            global_vars.use_view_to_render = False
        self.update_stats("", "Done!")

    # In this example, we fill the preview renders with a flat green color.
    def render_preview(self, scene_blender, size_x, size_y):
        pixel_count = size_x * size_y

        # The framebuffer is defined as a list of pixels, each pixel
        # itself being a list of R,G,B,A values
        green_rect = [[0.0, 1.0, 0.6, 1.0]] * pixel_count

        # Here we write the pixel values to the RenderResult
        result = self.begin_result(0, 0, size_x, size_y)
        layer = result.layers[0].passes["Combined"]
        layer.rect = green_rect
        self.end_result(result)

    # In this example, we fill the full renders with a flat blue color.
    def render_scene(self, scene_blender, size_x, size_y):
        pixel_count = size_x * size_y

        # The framebuffer is defined as a list of pixels, each pixel
        # itself being a list of R,G,B,A values
        blue_rect = [[1.0, 0.8, 0.6, 1.0]] * pixel_count

        # Here we write the pixel values to the RenderResult
        result = self.begin_result(0, 0, size_x, size_y)
        layer = result.layers[0].passes["Combined"]
        layer.rect = blue_rect
        self.end_result(result)

    # Blender callback. Perform finishing operations after all view layers in a frame were rendered
    def render_frame_finish(self):
        print("render_frame_finish", self)

    # Blender callback. Draw render image
    #    def draw(self, bl_context, depsgraph):
    #        print("draw", self, bl_context, depsgraph)

    # Blender callback. Bake passes
    # Parameters
    #     pass_type (enum in Bake Pass Type Items) – Pass, Pass to bake
    #     pass_filter (int in [0, inf]) – Pass Filter, Filter to combined, diffuse, glossy and transmission passes
    #     width (int in [0, inf]) – Width, Image width
    #     height (int in [0, inf]) – Height, Image height

    #    if bpy.app.version >= (2, 80, 0):
    #        def bake(self, depsgraph, bl_object, bl_pass_type, bl_pass_filter, bl_width, bl_height):
    #            print("bake", self, depsgraph, bl_object, bl_pass_type, bl_pass_filter, bl_width, bl_height)

    # Blender callback. Update on data changes for viewport render
    # For viewport renders, this method gets called once at the start and
    # whenever the scene or 3D viewport changes. This method is where data
    # should be read from Blender in the same thread. Typically, a render
    # thread will be started to do the work while keeping Blender responsive.

    if bpy.app.version >= (2, 80, 0):
        def view_update(self, bl_context, depsgraph):
            print("view_update", self, bl_context, depsgraph)

            bl_region = bl_context.region
            bl_view3d = bl_context.space_data
            scene_blender = depsgraph.scene

            # Get viewport dimensions
            bl_dimensions = bl_region.width, bl_region.height

            if not self.scene_data:
                # First time initialization
                self.scene_data = []
                first_time = True

                # Loop over all datablocks used in the scene.
                for datablock in depsgraph.ids:
                    pass
            else:
                first_time = False

                # Test which datablocks changed
                for update in depsgraph.updates:
                    print("Datablock updated: ", update.id.name)

                # Test if any material was added, removed or changed.
                if depsgraph.id_type_updated('MATERIAL'):
                    print("Materials updated")

            # Loop over all object instances in the scene.
            if first_time or depsgraph.id_type_updated('OBJECT'):
                for instance in depsgraph.object_instances:
                    pass
    # We will not implement 3D viewport render in Blender 2.79b, not worth the effort at this stage
    # else:
    #     def view_update(self, bl_context):
    #          print("view_update", self, bl_context)

    # Blender callback. Draw viewport render
    # For viewport renders, this method is called whenever Blender redraws
    # the 3D viewport. The renderer is expected to quickly draw the render
    # with OpenGL, and not perform other expensive work.
    # Blender will draw overlays for selection and editing on top of the

    if bpy.app.version >= (2, 80, 0):
        def view_draw(self, bl_context, depsgraph):
            print("view_draw", self, bl_context, depsgraph)
            bl_region = bl_context.region
            scene_blender = depsgraph.scene

            # Get viewport dimensions
            bl_dimensions = bl_region.width, bl_region.height

            # Bind shader that converts from scene linear to display space,
            gpu.state.blend_set('ALPHA_PREMULT')
            self.bind_display_space_shader(scene_blender)

            if not self.draw_data or self.draw_data.dimensions != bl_dimensions:
                self.draw_data = CustomDrawData(bl_dimensions)

            self.draw_data.draw()

            self.unbind_display_space_shader()
            gpu.state.blend_set('NONE')

    # We will not implement 3D viewport render in Blender 2.79b, not worth the effort at this stage
    # else:
    #    def view_draw(self, bl_context):
    #        print("view_draw", self, bl_context)

    # Blender callback. Compile shader script node
    # def update_script_node(self, bl_node=None):
    #    print("update_script_node", self, bl_node)

    # Blender callback. Update the render passes that will be generated
    def update_render_passes(self, scene_blender=None, render_layer_blender=None):
        # print("update_render_passes", self, scene_blender, render_layer_blender)
        if scene_blender.yafaray4.passes.pass_enable:
            if render_layer_blender.use_pass_z:
                self.register_pass(scene_blender, render_layer_blender, 'Depth', 1, 'Z', 'VALUE')

            if render_layer_blender.use_pass_vector:
                self.register_pass(scene_blender, render_layer_blender, "Vector", 4, '', 'COLOR')

            if render_layer_blender.use_pass_normal:
                self.register_pass(scene_blender, render_layer_blender, "Normal", 3, '', 'COLOR')

            if render_layer_blender.use_pass_uv:
                self.register_pass(scene_blender, render_layer_blender, "UV", 3, '', 'COLOR')

            if render_layer_blender.use_pass_emit:
                self.register_pass(scene_blender, render_layer_blender, "Emit", 3, '', 'COLOR')

            if render_layer_blender.use_pass_mist:
                self.register_pass(scene_blender, render_layer_blender, "Mist", 1, 'Z', 'VALUE')

            if render_layer_blender.use_pass_ambient_occlusion:
                self.register_pass(scene_blender, render_layer_blender, 'AO', 3, '', 'COLOR')

            if render_layer_blender.use_pass_environment:
                self.register_pass(scene_blender, render_layer_blender, "Env", 3, '', 'COLOR')

            if render_layer_blender.use_pass_shadow:
                self.register_pass(scene_blender, render_layer_blender, "Shadow", 3, '', 'COLOR')

            if render_layer_blender.use_pass_object_index:
                self.register_pass(scene_blender, render_layer_blender, "IndexOB", 1, '', 'VALUE')

            if render_layer_blender.use_pass_material_index:
                self.register_pass(scene_blender, render_layer_blender, "IndexMA", 1, '', 'VALUE')

            if render_layer_blender.use_pass_diffuse_direct:
                self.register_pass(scene_blender, render_layer_blender, "DiffDir", 3, '', 'COLOR')

            if render_layer_blender.use_pass_diffuse_indirect:
                self.register_pass(scene_blender, render_layer_blender, "DiffInd", 3, '', 'COLOR')

            if render_layer_blender.use_pass_diffuse_color:
                self.register_pass(scene_blender, render_layer_blender, "DiffCol", 3, '', 'COLOR')

            if render_layer_blender.use_pass_glossy_direct:
                self.register_pass(scene_blender, render_layer_blender, "GlossDir", 3, '', 'COLOR')

            if render_layer_blender.use_pass_glossy_indirect:
                self.register_pass(scene_blender, render_layer_blender, "GlossInd", 3, '', 'COLOR')

            if render_layer_blender.use_pass_glossy_color:
                self.register_pass(scene_blender, render_layer_blender, "GlossCol", 3, '', 'COLOR')

            if render_layer_blender.use_pass_transmission_direct:
                self.register_pass(scene_blender, render_layer_blender, "TransDir", 3, '', 'COLOR')

            if render_layer_blender.use_pass_transmission_indirect:
                self.register_pass(scene_blender, render_layer_blender, "TransInd", 3, '', 'COLOR')

            if render_layer_blender.use_pass_transmission_color:
                self.register_pass(scene_blender, render_layer_blender, "TransCol", 3, '', 'COLOR')

            if render_layer_blender.use_pass_subsurface_direct:
                self.register_pass(scene_blender, render_layer_blender, "SubsurfaceDir", 3, '', 'COLOR')

            if render_layer_blender.use_pass_subsurface_indirect:
                self.register_pass(scene_blender, render_layer_blender, "SubsurfaceInd", 3, '', 'COLOR')

            if render_layer_blender.use_pass_subsurface_color:
                self.register_pass(scene_blender, render_layer_blender, "SubsurfaceCol", 3, '', 'COLOR')


class CustomDrawData:
    def __init__(self, dimensions):
        # Generate dummy float image buffer
        self.dimensions = dimensions
        width, height = dimensions

        pixels = width * height * array.array('f', [0.1, 0.2, 0.1, 1.0])
        # noinspection PyArgumentList
        pixels = gpu.types.Buffer('FLOAT', width * height * 4, pixels)

        # Generate texture
        # noinspection PyArgumentList
        self.texture = gpu.types.GPUTexture((width, height), format='RGBA16F', data=pixels)

        # Note: This is just a didactic example.
        # In this case it would be more convenient to fill the texture with:
        # self.texture.clear('FLOAT', value=[0.1, 0.2, 0.1, 1.0])

    def __del__(self):
        del self.texture

    def draw(self):
        # noinspection PyTypeChecker
        draw_texture_2d(self.texture, (0, 0), self.texture.width, self.texture.height)


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
