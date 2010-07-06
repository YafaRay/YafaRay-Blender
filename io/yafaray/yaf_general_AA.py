import bpy


class yafGeneralAA:
        def __init__(self, interface):
                self.yi = interface

        def getRenderCoords(self,scene):
            
            render = scene.render
            sizeX= int(render.resolution_x*render.resolution_percentage*0.01)
            sizeY= int(render.resolution_y*render.resolution_percentage*0.01)
                
            bStartX = 0
            bStartY = 0
            bsizeX = 0
            bsizeY = 0
                
            cam_data = None
            
            for item in bpy.context.selected_objects:
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
                
        def exportGeneralAA(self,scene):
        
            yi = self.yi
            render = scene.render
            
            print("INFO: Exporting Render Settings")
            
            [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY,cam_data] = self.getRenderCoords(scene)
                
            yi.paramsClearAll()
            yi.paramsSetString("type", "none")
            yi.createIntegrator("volintegr")
            
            yi.paramsSetString("camera_name", "cam")
            yi.paramsSetString("integrator_name", "default")
            yi.paramsSetString("volintegrator_name", "volintegr")

            yi.paramsSetFloat("gamma", scene.gs_gamma)
            yi.paramsSetInt("AA_passes", scene.AA_passes)
            yi.paramsSetInt("AA_minsamples", scene.AA_min_samples)
            yi.paramsSetInt("AA_inc_samples", scene.AA_inc_samples)
            yi.paramsSetFloat("AA_pixelwidth", scene.AA_pixelwidth)
            yi.paramsSetFloat("AA_threshold", scene.AA_threshold)
            yi.paramsSetString("filter_type", scene.AA_filter_type)
            
            yi.paramsSetInt("xstart", bStartX)
            yi.paramsSetInt("ystart", bStartY)
            
            # no border when rendering to view
            if render.use_border and cam_data :
                yi.paramsSetInt("width", bsizeX)
                yi.paramsSetInt("height", bsizeY)
            else:
                yi.paramsSetInt("width", sizeX)
                yi.paramsSetInt("height", sizeY)
            
            yi.paramsSetBool("clamp_rgb", scene.gs_clamp_rgb)
            yi.paramsSetBool("show_sam_pix", scene.gs_show_sam_pix)
            yi.paramsSetInt("tile_size",scene.gs_tile_size)
            yi.paramsSetBool("premult", scene.gs_premult)
            
            if scene.gs_tile_order =="Linear" :
                yi.paramsSetString("tiles_order", "linear")
            elif scene.gs_tile_order =="Random":
                yi.paramsSetString("tiles_order", "random")
                
            yi.paramsSetBool("z_channel", True)
            yi.paramsSetBool("drawParams", scene.gs_draw_params)
            yi.paramsSetString("customString", scene.gs_custom_string)
            
            if scene.gs_auto_threads:
                yi.paramsSetInt("threads", -1)
            else:
                yi.paramsSetInt("threads", scene.gs_threads)

            yi.paramsSetString("background_name", "world_background")