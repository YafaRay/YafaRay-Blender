def computeSceneSize(render):
    sizeX = int(render.resolution_x * render.resolution_percentage * 0.01)
    sizeY = int(render.resolution_y * render.resolution_percentage * 0.01)
    return [sizeX, sizeY]


def getRenderCoords(scene):
    render = scene.render
    [sizeX, sizeY] = computeSceneSize(render)

    bStartX = 0
    bStartY = 0
    bsizeX = 0
    bsizeY = 0

    cam_data = None

    if len(scene.objects):
        for item in scene.objects:
            if item.type == 'CAMERA':
                cam_data = item.data
                break

    # Shift only available if camera is selected
    if not cam_data:
        shiftX = 0
        shiftY = 0

    else:
        # Sanne: get lens shift
        #camera = self.scene.objects.camera.getData()
        maxsize = max(sizeX, sizeY)
        shiftX = int(cam_data.shift_x * maxsize)
        shiftY = int(cam_data.shift_y * maxsize)

    # no border when rendering to view
    if render.use_border and  cam_data:
        minX = render.border_min_x * sizeX
        minY = render.border_min_y * sizeY
        maxX = render.border_max_x * sizeX
        maxY = render.border_max_y * sizeY
        bStartX = int(minX)
        bStartY = int(sizeY - maxY)
        bsizeX = int(maxX - minX)
        bsizeY = int(maxY - minY)

    # Sanne: add lens shift
    bStartX += shiftX
    bStartY -= shiftY

    return [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY,cam_data]

def exportAA(yi, scene):
    yi.paramsSetInt("AA_passes", scene.AA_passes)
    yi.paramsSetInt("AA_minsamples", scene.AA_min_samples)
    yi.paramsSetInt("AA_inc_samples", scene.AA_inc_samples)
    yi.paramsSetFloat("AA_pixelwidth", scene.AA_pixelwidth)
    yi.paramsSetFloat("AA_threshold", scene.AA_threshold)
    yi.paramsSetString("filter_type", scene.AA_filter_type)



def exportRenderSettings(yi, scene):
    yi.printInfo("Exporting Render Settings")

    render = scene.render

    [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, cam_data] = getRenderCoords(scene)

    #yi.paramsClearAll()
    #yi.paramsSetString("type", "none")
    #yi.createIntegrator("volintegr")

    yi.paramsSetString("camera_name", "cam")
    yi.paramsSetString("integrator_name", "default")
    yi.paramsSetString("volintegrator_name", "volintegr")

    yi.paramsSetFloat("gamma", scene.gs_gamma)

    exportAA(yi, scene)
    
    yi.paramsSetInt("xstart", bStartX)
    yi.paramsSetInt("ystart", bStartY)
    
    # no border when rendering to view
    if render.use_border and cam_data:
        yi.paramsSetInt("width", bsizeX)
        yi.paramsSetInt("height", bsizeY)
    else:
        yi.paramsSetInt("width", sizeX)
        yi.paramsSetInt("height", sizeY)

    yi.paramsSetBool("clamp_rgb", scene.gs_clamp_rgb)
    yi.paramsSetBool("show_sam_pix", scene.gs_show_sam_pix)
    yi.paramsSetBool("premult", scene.gs_premult)

    yi.paramsSetInt("tile_size",scene.gs_tile_size)
    yi.paramsSetString("tiles_order", scene.gs_tile_order)

    yi.paramsSetBool("z_channel", scene.gs_z_channel)
    yi.paramsSetBool("drawParams", scene.gs_draw_params)
    yi.paramsSetString("customString", scene.gs_custom_string)

    if scene.gs_auto_threads:
        yi.paramsSetInt("threads", -1)
    else:
        yi.paramsSetInt("threads", scene.gs_threads)

    yi.paramsSetString("background_name", "world_background")
