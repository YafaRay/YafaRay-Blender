import bpy

class YafCameraProperties(object):
    class _type(object):
        pass
    l = ["orthographic", "perspective", "architecture", "angular"]
    for t in l:
       setattr(_type, t, t)
    
    class bokeh_type(object):
        pass
    l = ["ring","hexagon","pentagon","square","triangle","disk1","disk2"]
    for t in l:
        setattr(bokeh_type, t, t)

def yaf_register_camera_types():
    bpy.types.Camera.EnumProperty(attr="YF_type", name="type", description="type",
                                  items=(
                                            (YafCameraProperties._type.orthographic,"orthographic","orthographic"),
                                            (YafCameraProperties._type.perspective,"perspective","perspective"),
                                            (YafCameraProperties._type.architecture,"architecture","architecture"),
                                            (YafCameraProperties._type.angular,"angular","angular"),
                                        ),
                                  default=YafCameraProperties._type.orthographic)
    bpy.types.Camera.FloatProperty(attr="YF_aperture", name="aperture size", description="aperture size", default=0.0)
    bpy.types.Camera.EnumProperty(attr="YF_bokeh_type", name="bokeh type", description="bokeh type",
                                  items=(
                                            (YafCameraProperties.bokeh_type.ring,"ring","ring"),
                                            (YafCameraProperties.bokeh_type.hexagon,"hexagon","hexagon"),
                                            (YafCameraProperties.bokeh_type.pentagon,"pentagon","pentagon"),
                                            (YafCameraProperties.bokeh_type.square,"square","square"),
                                            (YafCameraProperties.bokeh_type.triangle,"triangle","triangle"),
                                            (YafCameraProperties.bokeh_type.disk1,"disk1","disk1"),
                                            (YafCameraProperties.bokeh_type.disk2,"disk2","disk2"),
                                        ),
                                  default=YafCameraProperties.bokeh_type.ring)
    bpy.types.Camera.FloatProperty(attr="YF_bokeh_rotation", name="bokeh rotation", description="bokeh rotation", default=0.0, min=0.0, max=180.0, soft_min=0.0, soft_max=180.0)
    bpy.types.Camera.BoolProperty(attr="YF_circular", name="circular", description="circular", default=True)
    bpy.types.Camera.BoolProperty(attr="YF_mirrored", name="mirrored", description="mirrored", default=False)
    bpy.types.Camera.FloatProperty(attr="YF_max_angle", name="max angle", description="max angle", default=0.0, min=0.0, max=180.0, soft_min=0.0, soft_max=180.0)
    bpy.types.Camera.FloatProperty(attr="YF_angle", name="angle", description="angle", default=0.0, min=0.0, max=180.0, soft_min=0.0, soft_max=180.0)
