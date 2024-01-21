# SPDX-License-Identifier: GPL-2.0-or-later

import math
import time

import bpy
import libyafaray4_bindings
import mathutils

from ..util.io import scene_from_depsgraph


def get_bb_corners(obj):
    bb = obj.bound_box  # look bpy.types.Object if there is any problem

    minimum = [1e10, 1e10, 1e10]
    maximum = [-1e10, -1e10, -1e10]

    for corner in bb:
        for i in range(3):
            if corner[i] < minimum[i]:
                minimum[i] = corner[i]
            if corner[i] > maximum[i]:
                maximum[i] = corner[i]

    return minimum, maximum


def export_object(depsgraph, scene_yafaray, logger, is_preview, obj):
    if obj.vol_enable:  # Volume region
        write_volume_object(depsgraph, scene_yafaray, logger, obj)

    elif obj.ml_enable:  # Mesh light
        write_mesh_light(depsgraph, scene_yafaray, logger, is_preview, obj)

    elif obj.bgp_enable:  # BGPortal Light
        write_bg_portal(depsgraph, scene_yafaray, logger, is_preview, obj)

    elif obj.particle_systems:  # Particle Hair system
        scene_blender = scene_from_depsgraph(depsgraph)
        write_particle_strands(scene_blender, scene_yafaray, logger, is_preview, obj)

    else:  # The rest of the object types
        matrix = obj.matrix_world.copy()
        if is_preview and bpy.data.scenes[0].yafaray.preview.enable:
            if "checkers" in obj.name and bpy.data.scenes[0].yafaray.preview.preview_background == "checker":
                export_mesh(depsgraph, scene_yafaray, logger, is_preview, obj, matrix)
            elif "checkers" not in obj.name:
                export_mesh(depsgraph, scene_yafaray, logger, is_preview, obj, matrix)
        else:
            export_mesh(depsgraph, scene_yafaray, logger, is_preview, obj, matrix)


def export_instance_base(depsgraph, scene_yafaray, logger, is_preview, obj):
    logger.print_info("Exporting Base Mesh: {0}".format(obj.name))
    # Create this geometry object as a base object for instances
    write_geometry(depsgraph, scene_yafaray, is_preview, obj.name, obj, None, obj.pass_index,
                   None, "normal", True)  # We want the vertices in object space


def export_instance(scene_yafaray, logger, obj_to_world_matrix, base_obj_name):
    obj_to_world = obj_to_world_matrix.to_4x4()
    # mat4.transpose() --> not needed anymore: matrix indexing changed with Blender rev.42816
    # o2w = get4x4Matrix(mat4)
    # yi.addInstance(base_obj_name, o2w)
    instance_id = scene_yafaray.createInstance()
    object_id = scene_yafaray.get_object_id(base_obj_name)
    logger.printVerbose(
        "Exporting Instance ID={0} of {1} [Object ID = {2}]".format(instance_id, base_obj_name, object_id))
    scene_yafaray.add_instance_object(instance_id, object_id)
    add_instance_matrix(scene_yafaray, logger, instance_id, obj_to_world, 0.0)
    return instance_id


def add_instance_matrix(scene_yafaray, logger, instance_id, obj_to_world_matrix, instance_time):
    logger.printVerbose("Adding matrix to Instance ID={0} at time {1}".format(instance_id, instance_time))
    # print(obj_to_world_matrix)
    obj_to_world = obj_to_world_matrix.to_4x4()
    scene_yafaray.add_instance_matrix(instance_id,
                                      obj_to_world[0][0], obj_to_world[0][1], obj_to_world[0][2], obj_to_world[0][3],
                                      obj_to_world[1][0], obj_to_world[1][1], obj_to_world[1][2], obj_to_world[1][3],
                                      obj_to_world[2][0], obj_to_world[2][1], obj_to_world[2][2], obj_to_world[2][3],
                                      obj_to_world[3][0], obj_to_world[3][1], obj_to_world[3][2], obj_to_world[3][3],
                                      instance_time)


def export_mesh(depsgraph, scene_yafaray, logger, is_preview, obj, matrix, obj_name=None):
    if obj_name is None:
        obj_name = obj.name

    logger.print_info("Exporting Mesh: {0}".format(obj_name))

    if is_preview and bpy.data.scenes[0].yafaray.preview.enable and "preview" in obj_name:
        mat_name = obj.active_material.name

        if bpy.data.scenes[0].yafaray.preview.preview_object != "" and \
                bpy.data.scenes[0].objects[bpy.data.scenes[0].yafaray.preview.preview_object].type == "MESH":
            custom_obj = bpy.data.scenes[0].objects[bpy.data.scenes[0].yafaray.preview.preview_object]
            preview_matrix = custom_obj.matrix_world.copy()
            preview_matrix[0][3] = 0
            preview_matrix[1][3] = 0
            preview_matrix[2][3] = 0
            write_geometry(depsgraph, scene_yafaray, is_preview, obj_name, custom_obj, preview_matrix, obj.pass_index,
                           mat_name)
        else:
            preview_matrix = obj.matrix_world.copy()
            preview_matrix[0][3] = 0
            preview_matrix[1][3] = 0
            preview_matrix[2][3] = 0

            write_geometry(depsgraph, scene_yafaray, is_preview, obj_name, obj, preview_matrix, obj.pass_index)
    else:
        write_geometry(depsgraph, scene_yafaray, is_preview, obj_name, obj, matrix, obj.pass_index)


def write_bg_portal(depsgraph, scene_yafaray, logger, is_preview, obj):
    logger.print_info("Exporting Background Portal Light: {0}".format(obj.name))
    param_map = libyafaray4_bindings.ParamMap()
    # param_map.set_int("obj_pass_index", obj.pass_index)
    param_map.set_string("type", "bgPortalLight")
    param_map.set_float("power", obj.bgp_power)
    param_map.set_int("samples", obj.bgp_samples)
    param_map.set_string("object_name", obj.name)
    param_map.set_bool("with_caustic", obj.bgp_with_caustic)
    param_map.set_bool("with_diffuse", obj.bgp_with_diffuse)
    param_map.set_bool("photon_only", obj.bgp_photon_only)
    scene_yafaray.export_light(obj.name)
    matrix = obj.matrix_world.copy()
    # Makes object invisible to the renderer (doesn't enter the kdtree)
    write_geometry(depsgraph, scene_yafaray, is_preview, obj.name, obj, matrix, obj.pass_index, None, "invisible")


def write_mesh_light(depsgraph, scene_yafaray, logger, is_preview, obj):
    logger.print_info("Exporting Meshlight: {0}".format(obj.name))
    mat_name = "ML_"
    mat_name += obj.name + "." + str(obj.__hash__())

    param_map = libyafaray4_bindings.ParamMap()
    param_map_list = libyafaray4_bindings.ParamMapList()
    param_map.set_string("type", "light_mat")
    param_map.set_bool("double_sided", obj.ml_double_sided)
    c = obj.ml_color
    param_map.set_color("color", c[0], c[1], c[2])
    param_map.set_float("power", obj.ml_power)
    scene_yafaray.create_material(mat_name, param_map, param_map_list)

    # Export mesh light
    param_map = libyafaray4_bindings.ParamMap()
    # param_map.set_int("obj_pass_index", obj.pass_index)
    param_map.set_string("type", "objectlight")
    param_map.set_bool("double_sided", obj.ml_double_sided)
    c = obj.ml_color
    param_map.set_color("color", c[0], c[1], c[2])
    param_map.set_float("power", obj.ml_power)
    param_map.set_int("samples", obj.ml_samples)
    param_map.set_string("object_name", obj.name)
    scene_yafaray.export_light(obj.name, param_map)

    matrix = obj.matrix_world.copy()
    write_geometry(depsgraph, scene_yafaray, is_preview, obj.name, obj, matrix, obj.pass_index, mat_name)


def write_volume_object(depsgraph, scene_yafaray, logger, obj):
    logger.print_info("Exporting Volume Region: {0}".format(obj.name))

    # me = obj.data  /* UNUSED */
    # me_materials = me.materials  /* UNUSED */
    scene_blender = scene_from_depsgraph(depsgraph)
    param_map = libyafaray4_bindings.ParamMap()
    param_map.set_int("obj_pass_index", obj.pass_index)

    if obj.vol_region == 'ExpDensity Volume':
        param_map.set_string("type", "ExpDensityVolume")
        param_map.set_float("a", obj.vol_height)
        param_map.set_float("b", obj.vol_steepness)

    elif obj.vol_region == 'Uniform Volume':
        param_map.set_string("type", "UniformVolume")

    elif obj.vol_region == 'Noise Volume':
        if not obj.active_material:
            logger.printError("Volume object ({0}) is missing the materials".format(obj.name))
        elif not obj.active_material.active_texture:
            logger.printError("Volume object's material ({0}) is missing the noise texture".format(obj.name))
        else:
            texture = obj.active_material.active_texture

            param_map.set_string("type", "NoiseVolume")
            param_map.set_float("sharpness", obj.vol_sharpness)
            param_map.set_float("cover", obj.vol_cover)
            param_map.set_float("density", obj.vol_density)
            param_map.set_string("texture", texture.name)

    elif obj.vol_region == 'Grid Volume':
        param_map.set_string("type", "GridVolume")

    param_map.set_float("sigma_a", obj.vol_absorp)
    param_map.set_float("sigma_s", obj.vol_scatter)
    param_map.set_int("attgridScale", scene_blender.world.v_int_attgridres)

    # Calculate BoundingBox: get the low corner (minx, miny, minz)
    # and the up corner (maxx, maxy, maxz) then apply object scale,
    # also clamp the values to min: -1e10 and max: 1e10

    if bpy.app.version >= (2, 80, 0):
        mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
    else:
        mesh = obj.to_mesh(scene_blender, True, 'RENDER')
    matrix = obj.matrix_world.copy()
    mesh.transform(matrix)

    vec = [j for v in mesh.vertices for j in v.co]

    param_map.set_float("minX", max(min(vec[0::3]), -1e10))
    param_map.set_float("minY", max(min(vec[1::3]), -1e10))
    param_map.set_float("minZ", max(min(vec[2::3]), -1e10))
    param_map.set_float("maxX", min(max(vec[0::3]), 1e10))
    param_map.set_float("maxY", min(max(vec[1::3]), 1e10))
    param_map.set_float("maxZ", min(max(vec[2::3]), 1e10))

    scene_yafaray.createVolumeRegion("VR.{0}-{1}".format(obj.name, str(obj.__hash__())), param_map)
    if bpy.app.version >= (2, 80, 0):
        pass  # FIXME BLENDER >= v2.80
    else:
        bpy.data.meshes.remove(mesh, do_unlink=False)


def write_geometry(depsgraph, scene_yafaray, is_preview, obj_name, obj, matrix, pass_index, obj_mat=None,
                   visibility="normal", is_base_object=False):
    is_smooth = False
    has_orco = False
    scene_blender = scene_from_depsgraph(depsgraph)

    if bpy.app.version >= (2, 80, 0):
        mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
        # test for UV Map after BMesh API changes
        uv_texture = mesh.uv_layers if 'uv_layers' in dir(mesh) else mesh.uv_textures
        # test for faces after BMesh API changes
        face_attr = 'polygons' if 'polygons' in dir(mesh) else 'loop_triangles'
        has_uv = False  # FIXME BLENDER >= v2.80 #len(uv_texture) > 0  # check for UV's

        if face_attr == 'loop_triangles':
            if not mesh.loop_triangles and mesh.polygons:
                # BMesh API update, check for tessellated faces, if needed calculate them...
                mesh.update(calc_edges=False, calc_edges_loose=False, calc_loop_triangles=True)

            if not mesh.loop_triangles:
                # if there are no faces, no need to write geometry, remove mesh data then...
                bpy.data.meshes.remove(mesh, do_unlink=False)
                return
        else:
            if not mesh.polygons:
                # if there are no faces, no need to write geometry, remove mesh data then...
                bpy.data.meshes.remove(mesh, do_unlink=False)
                return
    else:
        mesh = obj.to_mesh(scene_blender, True, 'RENDER')
        # test for UV Map after BMesh API changes
        uv_texture = mesh.tessface_uv_textures if 'tessface_uv_textures' in dir(mesh) else mesh.uv_textures
        # test for faces after BMesh API changes
        face_attr = 'faces' if 'faces' in dir(mesh) else 'tessfaces'
        has_uv = len(uv_texture) > 0  # check for UV's

        if face_attr == 'tessfaces':
            if not mesh.tessfaces and mesh.polygons:
                # BMesh API update, check for tessellated faces, if needed calculate them...
                mesh.update(calc_tessface=True)

            if not mesh.tessfaces:
                # if there are no faces, no need to write geometry, remove mesh data then...
                bpy.data.meshes.remove(mesh, do_unlink=False)
                return
        else:
            if not mesh.faces:
                # if there are no faces, no need to write geometry, remove mesh data then...
                bpy.data.meshes.remove(mesh, do_unlink=False)
                return

    if bpy.app.version >= (2, 80, 0):
        pass  # FIXME BLENDER >= v2.80
    else:
        # Check if the object has an orco mapped texture
        for mat in [mmat for mmat in mesh.materials if mmat is not None]:
            for m in [mtex for mtex in mat.texture_slots if mtex is not None]:
                if m.texture_coords == 'ORCO':
                    has_orco = True
                    break
            if has_orco:
                break

    # normalized vertex positions for orco mapping
    ov = []

    if has_orco:
        # Keep a copy of the untransformed vertex and bring them
        # into a (-1 -1 -1) (1 1 1) bounding box
        bb_min, bb_max = get_bb_corners(obj)

        delta = []

        for i in range(3):
            delta.append(bb_max[i] - bb_min[i])
            if delta[i] < 0.0001:
                delta[i] = 1

        # use untransformed mesh's vertices
        for v in mesh.vertices:
            norm_co = []
            for i in range(3):
                norm_co.append(2 * (v.co[i] - bb_min[i]) / delta[i] - 1)

            ov.append([norm_co[0], norm_co[1], norm_co[2]])

    # Transform the mesh after orcos have been stored and only if matrix exists
    if matrix is not None:
        mesh.transform(matrix)

    if is_preview:
        if "checker" in obj.name:
            # noinspection PyArgumentList
            matrix2 = mathutils.Matrix.Scale(4, 4)
            mesh.transform(matrix2)
        elif bpy.data.scenes[0].yafaray.preview.enable:
            # noinspection PyArgumentList
            matrix2 = mathutils.Matrix.Scale(bpy.data.scenes[0].yafaray.preview.obj_scale, 4)
            mesh.transform(matrix2)
            matrix2 = mathutils.Matrix.Rotation(bpy.data.scenes[0].yafaray.preview.rot_z, 4, 'Z')
            mesh.transform(matrix2)
        pass

    param_map = libyafaray4_bindings.ParamMap()

    param_map.set_string("type", "mesh")
    param_map.set_int("num_vertices", len(mesh.vertices))
    param_map.set_int("num_faces", len(getattr(mesh, face_attr)))
    param_map.set_bool("has_orco", has_orco)
    param_map.set_bool("has_uv", has_uv)
    param_map.set_bool("is_base_object", is_base_object)
    param_map.set_string("visibility", visibility)
    param_map.set_int("object_index", pass_index)
    param_map.set_bool("motion_blur_bezier", obj.motion_blur_bezier)
    object_id = scene_yafaray.create_object(obj_name, param_map)

    for ind, v in enumerate(mesh.vertices):
        if has_orco:
            scene_yafaray.add_vertex_with_orco(object_id, v.co[0], v.co[1], v.co[2], ov[ind][0], ov[ind][1],
                                               ov[ind][2])
        else:
            scene_yafaray.add_vertex(object_id, v.co[0], v.co[1], v.co[2])

    if scene_blender.adv_scene_mesh_tesselation == "triangles_only":
        triangles_only = True
    else:
        triangles_only = False

    for index, f in enumerate(getattr(mesh, face_attr)):
        if f.use_smooth:
            is_smooth = True

        if obj_mat:
            material_yafaray = obj_mat
        else:
            material_yafaray = get_face_material(mesh.materials, f.material_index, obj.material_slots)
        material_id = scene_yafaray.get_material_id(material_yafaray)
        if has_uv:
            if is_preview:
                co = uv_texture[0].data[index].uv
            else:
                co = uv_texture.active.data[index].uv

            uv0 = scene_yafaray.add_uv(object_id, co[0][0], co[0][1])
            uv1 = scene_yafaray.add_uv(object_id, co[1][0], co[1][1])
            uv2 = scene_yafaray.add_uv(object_id, co[2][0], co[2][1])

            if len(f.vertices) == 4:
                uv3 = scene_yafaray.add_uv(object_id, co[3][0], co[3][1])
                if triangles_only:
                    scene_yafaray.add_triangle_with_uv(object_id, f.vertices[0], f.vertices[1], f.vertices[2], uv0,
                                                       uv1, uv2, material_id)
                    scene_yafaray.add_triangle_with_uv(object_id, f.vertices[0], f.vertices[2], f.vertices[3], uv0,
                                                       uv2, uv3, material_id)
                else:
                    scene_yafaray.add_quad_with_uv(object_id, f.vertices[0], f.vertices[1], f.vertices[2],
                                                   f.vertices[3], uv0, uv1, uv2, uv3, material_id)
            else:
                scene_yafaray.add_triangle_with_uv(object_id, f.vertices[0], f.vertices[1], f.vertices[2], uv0,
                                                   uv1, uv2, material_id)
        else:
            if len(f.vertices) == 4:
                if triangles_only:
                    scene_yafaray.add_triangle(object_id, f.vertices[0], f.vertices[1], f.vertices[2], material_id)
                    scene_yafaray.add_triangle(object_id, f.vertices[0], f.vertices[2], f.vertices[3], material_id)
                else:
                    scene_yafaray.add_quad(object_id, f.vertices[0], f.vertices[1], f.vertices[2], f.vertices[3],
                                           material_id)
            else:
                scene_yafaray.add_triangle(object_id, f.vertices[0], f.vertices[1], f.vertices[2], material_id)

    auto_smooth_enabled = mesh.use_auto_smooth
    auto_smooth_angle = mesh.auto_smooth_angle

    if bpy.app.version >= (2, 80, 0):
        pass  # FIXME BLENDER >= v2.80
    else:
        bpy.data.meshes.remove(mesh, do_unlink=False)

    if obj.motion_blur_bezier:
        frame_current = scene_blender.frame_current
        for time_step in range(1, 3):
            scene_blender.frame_set(frame_current, 0.5 * time_step)
            mesh = scene_blender.objects[obj.name].to_mesh(scene_blender, True, 'RENDER')
            mesh.update(calc_tessface=True)
            if obj.matrix_world is not None:
                mesh.transform(obj.matrix_world)
            for ind, v in enumerate(mesh.vertices):
                if has_orco:
                    scene_yafaray.add_vertex_with_orcoTimeStep(object_id, v.co[0], v.co[1], v.co[2], ov[ind][0],
                                                               ov[ind][1], ov[ind][2], time_step)
                else:
                    scene_yafaray.add_vertexTimeStep(object_id, v.co[0], v.co[1], v.co[2], time_step)
            if bpy.app.version >= (2, 80, 0):
                pass  # FIXME BLENDER >= v2.80
            else:
                bpy.data.meshes.remove(mesh, do_unlink=False)
        scene_blender.frame_set(frame_current, 0.0)
    scene_yafaray.init_object(object_id, 0)

    if is_smooth and auto_smooth_enabled:
        scene_yafaray.smooth_object_mesh(object_id, math.degrees(auto_smooth_angle))
    elif is_smooth and obj.type == 'FONT':  # getting nicer result with smooth angle 60 degr. for text objects
        scene_yafaray.smooth_object_mesh(object_id, 60)
    elif is_smooth:
        scene_yafaray.smooth_object_mesh(object_id, 181)


def get_face_material(mesh_mats, mat_index, mat_slots):
    material_yafaray = "defaultMat"

    # if scene_blender.gs_clay_render:
    #    material_yafaray = materialMap["clay"]
    if len(mesh_mats) and mesh_mats[mat_index]:
        mat = mesh_mats[mat_index]
        material_yafaray = mat.name
    else:
        for mat_slots in [ms for ms in mat_slots]:
            if mat_slots.material is not None:
                material_yafaray = mat_slots.material.name

    return material_yafaray


def write_particle_strands(depsgraph, scene_yafaray, logger, is_preview, obj):
    render_emitter = False
    if not hasattr(obj, 'particle_systems'):
        return
    # Check for hair particles:
    for particle_system in obj.particle_systems:
        if bpy.app.version >= (2, 80, 0):
            continue  # FIXME BLENDER >= v2.80
        scene_blender = scene_from_depsgraph(depsgraph)
        for mod in [m for m in obj.modifiers if (m is not None) and (m.type == 'PARTICLE_SYSTEM')]:
            if (particle_system.settings.render_type == 'PATH') and mod.show_render \
                    and (particle_system.name == mod.particle_system.name):
                logger.print_info("Exporter: Creating Hair Particle System {!r}".format(particle_system.name))
                time_start = time.time()
                # TODO: clay particles uses at least materials thikness?
                if obj.active_material is not None:
                    obj_material = obj.active_material

                    if obj_material.strand.use_blender_units:
                        strand_start = obj_material.strand.root_size
                        strand_end = obj_material.strand.tip_size
                        strand_shape = obj_material.strand.shape
                    else:  # Blender unit conversion
                        strand_start = obj_material.strand.root_size / 100
                        strand_end = obj_material.strand.tip_size / 100
                        strand_shape = obj_material.strand.shape
                else:
                    obj_material = "default"  # No material assigned in blender, use default one
                    strand_start = 0.01
                    strand_end = 0.01
                    strand_shape = 0.0

                strand_id = 0
                matrix = obj.matrix_world.copy()
                for particle in particle_system.particles:
                    param_map = libyafaray4_bindings.ParamMap()
                    material_id = scene_yafaray.get_material_id(obj_material.name)
                    param_map.set_string("type", "curve")
                    param_map.set_float("strand_start", strand_start)
                    param_map.set_float("strand_end", strand_end)
                    param_map.set_float("strand_shape", strand_shape)
                    param_map.set_int("num_vertices", len(particle.hair_keys))
                    param_map.set_bool("motion_blur_bezier", obj.motion_blur_bezier)
                    strand_obj_id = scene_yafaray.create_object(obj.name + "_strand_" + str(strand_id), param_map)
                    for location in particle.hair_keys:
                        vertex = matrix * location.co  # use reverse vector multiply order, API changed with rev. 38674
                        scene_yafaray.add_vertex(strand_obj_id, vertex[0], vertex[1], vertex[2])

                    if obj.motion_blur_bezier:
                        frame_current = scene_blender.frame_current
                        for time_step in range(1, 3):
                            scene_blender.frame_set(frame_current, 0.5 * time_step)
                            matrix = obj.matrix_world.copy()
                            for location in particle.hair_keys:
                                # use reverse vector multiply order, API changed with rev. 38674
                                vertex = matrix * location.co
                                scene_yafaray.add_vertex_time_step(strand_obj_id, vertex[0], vertex[1], vertex[2],
                                                                   time_step)
                        scene_blender.frame_set(frame_current, 0.0)

                    scene_yafaray.init_object(strand_obj_id, material_id)
                    strand_id += 1
                    # TODO: keep object smooth
                    # yi.smoothMesh(0, 60.0)
                logger.print_info("Exporter: Particle creation time: {0:.3f}".format(time.time() - time_start))

                if particle_system.settings.use_render_emitter:
                    render_emitter = True
            else:
                export_mesh(depsgraph, scene_yafaray, logger, is_preview, obj, obj.matrix_world.copy())

    # We only need to render emitter object once
    if render_emitter:
        # ymat = materialMap["default"]  /* UNUSED */
        export_mesh(depsgraph, scene_yafaray, logger, is_preview, obj, obj.matrix_world.copy())
