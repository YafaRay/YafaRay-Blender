# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# TODO: Use Blender enumerators if any
import bpy
import os
import threading
import time
import libyafaray4_bindings
import traceback
import datetime
import platform
import tempfile

from .. import YAF_ID_NAME
from .. import YAFARAY_BLENDER_VERSION
from .object import Object
from .light import Light
from .world import World
from .integrator import Integrator
from .film import Film
from . import scene
from .texture import Texture
from .material import Material
from .scene import Scene
from ..ot import presets
# from pprint import pprint
# from pprint import pformat
from ..util.io import scene_from_depsgraph
from .. import global_vars

#
yaf_logger = libyafaray4_bindings.Logger()
yaf_logger.setConsoleVerbosityLevel(yaf_logger.logLevelFromString("debug"))
yaf_logger.setLogVerbosityLevel(yaf_logger.logLevelFromString("debug"))
# yaf_logger.setConsoleLogColorsEnabled(True)
yaf_logger.enablePrintDateTime(True)


# yaf_main_scene = libyafaray4_bindings.Scene(yaf_logger, "Blender Main Scene")
# yaf_preview_scene = libyafaray4_bindings.Scene(yaf_logger, "Blender Preview Scene")
#
# yaf_main_surface_integrator_param_map = libyafaray4_bindings.ParamMap()
# yaf_main_surface_integrator_param_map.setString("type", "directlighting")
# yaf_main_surface_integrator = libyafaray4_bindings.SurfaceIntegrator(yaf_logger, "Blender Main SurfaceIntegrator", yaf_main_surface_integrator_param_map)
# yaf_preview_surface_integrator_param_map = libyafaray4_bindings.ParamMap()
# yaf_preview_surface_integrator_param_map.setString("type", "directlighting")
# yaf_preview_surface_integrator = libyafaray4_bindings.SurfaceIntegrator(yaf_logger, "Blender Preview SurfaceIntegrator", yaf_preview_surface_integrator_param_map)
#
# yaf_main_film_param_map = libyafaray4_bindings.ParamMap()
# yaf_main_film = libyafaray4_bindings.Film(yaf_logger, yaf_main_surface_integrator, "Blender Main Film", yaf_main_film_param_map)
# yaf_preview_film_param_map = libyafaray4_bindings.ParamMap()
# yaf_preview_film = libyafaray4_bindings.Film(yaf_logger, yaf_preview_surface_integrator, "Blender Preview Film", yaf_preview_film_param_map)

class RenderEngine(bpy.types.RenderEngine):
    bl_idname = YAF_ID_NAME
    bl_use_preview = True
    bl_label = "YafaRay v4 Render"
    prog = 0.0
    tag = ""
    global_vars.use_view_to_render = False
    global_vars.view_matrix = None

    def __init__(self):
        self.yaf_logger = yaf_logger
        self.scene = None
        self.integrator = None
        self.film = None
        self.is_preview = False

    # callback to export the scene
    def update_OLD_DELETE(self, bl_data, bl_depsgraph):
        self.scene = Scene(bl_depsgraph, self.yaf_logger)
        self.update_stats("", "Setting up render")

    def update_OLD_DELETE(self, bl_data, bl_depsgraph):
        self.scene = Scene(bl_depsgraph, self.yaf_logger)
        self.update_stats("", "Setting up render")
        if not self.is_preview:
            self.bl_scene.frame_set(self.bl_scene.frame_current)

        bl_render = self.bl_scene.render

        if bpy.data.filepath == "":
            render_filename = "render"
            render_path = tempfile.gettempdir() + "/temp_render/"
        else:
            render_filename = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
            render_path = "//" + render_filename + "_render/"

        render_filename += " - " + str(self.bl_scene.frame_current)

        if self.bl_scene.img_save_with_blend_file:
            bl_render.filepath = render_path
            render_path = bpy.path.abspath(render_path)
        else:
            render_path = bpy.path.abspath(bl_render.filepath)

        render_path = os.path.realpath(render_path)
        render_path = os.path.normpath(render_path)

        if not os.path.exists(render_path):
            os.mkdir(render_path)

        [self.size_x, self.size_y, self.border_start_x, self.border_start_y, self.border_size_x, self.border_size_y, cam_dummy] = get_render_coords(self.bl_scene)

        if bl_render.use_border:
            self.res_x = self.border_size_x
            self.res_y = self.border_size_y
        else:
            self.res_x = self.size_x
            self.res_y = self.size_y

        color_space = calc_color_space(self.bl_scene)
        gamma = calc_gamma(self.bl_scene)
        alpha_premultiply = calc_alpha_premultiply(self.bl_scene)

        if self.bl_scene.gs_type_render == "file":
            # self.setInterface(libyafaray4_bindings.Interface())
            self.yaf_scene.setInputColorSpace("LinearRGB",
                                              1.0)  # When rendering into Blender, color picker floating point data is already linear (linearized by Blender)
            self.define_image_output("blender_file_output", render_path, self.bl_scene, bl_render, color_space.blender, gamma.blender, alpha_premultiply.blender)
            if self.bl_scene.yafaray.logging.savePreset:
                presets.AddPresetBase.export_to_file(presets.YAFARAY_OT_presets_renderset, self.output_file)

        elif self.bl_scene.gs_type_render == "xml" or self.bl_scene.gs_type_render == "c" or self.bl_scene.gs_type_render == "python":
            self.output_file, self.output, self.file_type = self.decide_output_file_name(render_path, self.bl_scene.gs_type_render)
            # self.setInterface(libyafaray4_bindings.Interface(self.outputFile))

            input_color_values_color_space = "sRGB"
            input_color_values_gamma = 1.0

            if self.bl_scene.display_settings.display_device == "sRGB":
                input_color_values_color_space = "sRGB"

            elif self.bl_scene.display_settings.display_device == "XYZ":
                input_color_values_color_space = "XYZ"

            elif self.bl_scene.display_settings.display_device == "None":
                input_color_values_color_space = "Raw_Manual_Gamma"
                input_color_values_gamma = self.bl_scene.gs_gamma  # We only use the selected gamma if the output device is set to "None"

            self.yaf_scene.setInputColorSpace("LinearRGB",
                                              1.0)  # Values from Blender, color picker floating point data are already linear (linearized by Blender)
            self.define_image_output("xml_file_output", render_path, self.bl_scene, bl_render, color_space.blender, gamma.blender, alpha_premultiply.blender)
            # FIXME! self.yi.setXmlColorSpace(input_color_values_color_space, input_color_values_gamma)  #To set the XML interface to write the XML values with the correction included for the selected color space (and gamma if applicable)

        # else:

        # self.setInterface(libyafaray4_bindings.Interface())
        # self.yaf_scene.setInputColorSpace("LinearRGB", 1.0)    #When rendering into Blender, color picker floating point data is already linear (linearized by Blender)
        # if self.bl_scene.gs_secondary_file_output and not self.is_preview:
        #    self.defineImageOutput("blender_secondary_output", render_path, self.bl_scene, render, color_space.secondary_output, gamma.secondary_output, alpha_premultiply.secondary_output)
        #    if self.bl_scene.yafaray.logging.savePreset:
        #        presets.AddPresetBase.export_to_file(presets.YAFARAY_OT_presets_renderset, self.outputFile)

        self.export_scene()
        self.integrator = Integrator(self.yaf_logger)
        self.integrator.exportIntegrator(self.bl_scene, self.is_preview)
        self.integrator.exportVolumeIntegrator(self.bl_scene, self.yaf_scene)
        yaf_film_param_map = libyafaray4_bindings.ParamMap()
        yaf_film = libyafaray4_bindings.Film(yaf_logger, self.integrator.yaf_integrator, "Blender Main Film",
                                             yaf_film_param_map)
        self.film = Film(yaf_film, yaf_logger, self.is_preview)
        self.film.define_camera(self.bl_scene.camera, global_vars.use_view_to_render, bl_render.resolution_x, bl_render.resolution_y, bl_render.resolution_percentage, global_vars.view_matrix)
        # yaf_scene.defineLayers(self.yaf_scene, self.depsgraph)
        # yaf_scene.exportRenderSettings(self.yaf_scene, self.depsgraph, render_path, render_filename)

        # self.yaf_scene.setupRender()

    def create_cameras(self, bl_scene):

        self.yaf_logger.printInfo("Exporting Cameras")

        render = bl_scene.render

        class CameraData:
            def __init__(self, camera, camera_name, view_name):
                self.camera = camera
                self.camera_name = camera_name
                self.view_name = view_name

        cameras = []

        render_use_multiview = render.use_multiview

        if global_vars.use_view_to_render or not render_use_multiview:
            cameras.append(CameraData(bl_scene.camera, bl_scene.camera.name, ""))
        else:
            camera_base_name = bl_scene.camera.name.rsplit('_', 1)[0]

            for view in render.views:
                if view.use and not (
                        render.views_format == "STEREO_3D" and view.name != "left" and view.name != "right"):
                    cameras.append(CameraData(bl_scene.objects[camera_base_name + view.camera_suffix],
                                              camera_base_name + view.camera_suffix, view.name))

        for cam in cameras:
            pass

    # callback to render scene
    def render(self, depsgraph):
        self.bl_depsgraph = depsgraph
        self.bl_scene = scene_from_depsgraph(depsgraph)
        self.bl_use_postprocess = False

        if self.bl_scene.gs_type_render == "file":
            self.yaf_logger.printInfo("Exporter: Rendering to file {0}".format(self.output_file))
            self.update_stats("YafaRay Rendering:", "Rendering to {0}".format(self.output_file))
            self.yaf_scene.render(0, 0)
            result = self.begin_result(0, 0, self.res_x, self.res_y)
            result.layers[0].load_from_file(self.output_file)
            # lay.passes["Depth"].load_from_file("{0} (Depth).{1}".format(self.output, self.file_type)) #FIXME? Unfortunately I cannot find a way to load the exported images back to the appropiate passes in Blender. Blender probably needs to improve their API to allow per-pass loading of files. Also, Blender does not allow opening multi layer EXR files with this function.
            self.end_result(result)

        elif self.bl_scene.gs_type_render == "xml":
            self.yaf_logger.printInfo("Exporter: Writing XML to file {0}".format(self.output_file))
            self.yaf_scene.render(0, 0)

        else:
            def progress_callback(*args):
                steps_total, steps_done, tag = args
                self.update_stats("YafaRay Render: ", "{0}".format(tag))
                # Now, Blender use same range to YafaRay
                if steps_total > 0:
                    self.update_progress(steps_done / steps_total)
                else:
                    self.update_progress(0.0)

            def update_blender_result(x, y, w, h, view_name, tiles, callback_name):
                # print(x, y, w, h, view_name, tiles, callback_name, scene.render.use_multiview)
                if self.bl_scene.render.use_multiview:
                    blender_result_buffers = self.begin_result(x, y, w, h, "", view_name)
                else:
                    blender_result_buffers = self.begin_result(x, y, w, h)
                for tile in tiles:
                    tile_name, tile_bitmap = tile
                    print("tile_name:", tile_name, " tile_bitmap:", tile_bitmap, " blender_result_buffers:",
                          blender_result_buffers)
                    try:
                        blender_result_buffers.layers[0].passes[0].rect = tile_bitmap
                    except:
                        print("Exporter: Exception while rendering in " + callback_name + " function:")
                        traceback.print_exc()
                self.end_result(blender_result_buffers)

            def highlight_callback(*args):
                view_name, area_id, x_0, y_0, x_1, y_1, tiles = args
                w = x_1 - x_0
                h = y_1 - y_0
                if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                    for view in self.bl_scene.render.views:
                        update_blender_result(x_0, y_0, w, h, view.name, tiles, "highlightCallback")
                else:  # Normal rendering
                    update_blender_result(x_0, y_0, w, h, view_name, tiles, "highlightCallback")

            def flush_area_callback(*args):
                # view_name, area_id, x_0, y_0, x_1, y_1, tiles = args
                area_id, x_0, y_0, x_1, y_1, tiles = args
                view_name = "test"
                w = x_1 - x_0
                h = y_1 - y_0
                if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                    for view in self.bl_scene.render.views:
                        update_blender_result(x_0, y_0, w, h, view.name, tiles, "flushAreaCallback")
                else:  # Normal rendering
                    update_blender_result(x_0, y_0, w, h, view_name, tiles, "flushAreaCallback")

            def flush_callback(*args):
                w, h, tiles = args
                view_name = "test"
                if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                    for view in self.bl_scene.render.views:
                        update_blender_result(0, 0, w, h, view.name, tiles, "flushCallback")
                else:  # Normal rendering
                    update_blender_result(0, 0, w, h, view_name, tiles, "flushCallback")

            return

            self.film.yaf_film.setFlushAreaCallback(flush_area_callback)
            self.film.yaf_film.setFlushCallback(flush_callback)
            self.film.yaf_film.setHighlightAreaCallback(highlight_callback)
            # Creating RenderControl #
            render_control = libyafaray4_bindings.RenderControl()
            # Creating RenderMonitor #
            render_monitor = libyafaray4_bindings.RenderMonitor(progress_callback)
            render_control.setForNormalStart()
            scene_modified_flags = self.yaf_scene.checkAndClearModifiedFlags()
            self.yaf_scene.preprocess(render_control, scene_modified_flags)
            self.integrator.yaf_integrator.preprocess(render_monitor, render_control, self.yaf_scene)
            self.integrator.yaf_integrator.render(render_control, render_monitor, self.film.yaf_film)
            return  # FIXME!!!
            t = threading.Thread(target=self.yaf_integrator, args=(self.yaf_scene, progressCallback,))
            t.start()

            while t.is_alive() and not self.test_break():
                time.sleep(0.2)

            if t.is_alive():
                self.update_stats("",
                                  "Aborting, please wait for all pending tasks to complete (progress in console log)...")
                self.yaf_scene.cancelRendering()
                t.join()

        # self.yaf_scene.clearAll()
        # self.yaf_scene.clearOutputs()
        # del self.yaf_scene
        self.update_stats("", "Done!")
        self.bl_use_postprocess = True


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


if __name__ == "__main__":  # only for live edit.
    import bpy

    bpy.utils.register_module(__name__)
