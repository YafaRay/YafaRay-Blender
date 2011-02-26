import bpy
from bpy.props import *
Object = bpy.types.Object

def register():
    print("Registering object properties")
    #TODO: update default values, edit description


    Object.ml_enable =      BoolProperty(attr="ml_enable",
                                            description = "Makes the mesh emit light")
                                            
    Object.ml_color =       FloatVectorProperty(attr="ml_color",
                                            description = "Color Settings", subtype = "COLOR",
                                            default = (0.7, 0.7, 0.7), # gris
                                            step = 1, precision = 2,
                                            min = 0.0, max = 1.0,
                                            soft_min = 0.0, soft_max = 1.0)

    Object.ml_power =       FloatProperty(attr="ml_power",
                                            description = "Intensity multiplier for color",
                                            min = 0,
                                            default = 1)
    Object.ml_samples =     IntProperty(attr="ml_samples",
                                            description = "Number of samples to be taken for direct lighting",
                                            min = 0, max = 512,
                                            default = 16)
    Object.ml_double_sided = BoolProperty(attr="ml_double_sided",
                                            description = "Emit light at both sides of every face")
    Object.bgp_enable =     BoolProperty(attr="bgp_enable",
                                            description = "BG Portal Light Settings")
    Object.bgp_power =      FloatProperty(attr="bgp_power",
                                            description = "Intensity multiplier for color",
                                            min = 0,
                                            default = 1)
    Object.bgp_samples =    IntProperty(attr="bgp_samples",
                                            description = "Number of samples to be taken for the light",
                                            min = 0, max = 512,
                                            default = 16)
    Object.bgp_with_caustic = BoolProperty(attr="bgp_with_caustic",
                                            description = "Allow BG Portal Light to shoot caustic photons",
                                            default = True)
    Object.bgp_with_diffuse = BoolProperty(attr="bgp_with_diffuse",
                                            description = "Allow BG Portal Light to shoot diffuse photons",
                                            default = True)
    Object.bgp_photon_only = BoolProperty(attr="bgp_photon_only",
                                            description = "Set BG Portal Light in photon only mode (no direct light contribution)",
                                            default = False)

    Object.vol_enable =     BoolProperty(attr="vol_enable",
                                            description="Makes the mesh a volume at its bounding box")
    Object.vol_region =     EnumProperty(
        description="Set the volume region",
        items = (
            ("ExpDensity Volume","ExpDensity Volume",""),
            ("Noise Volume","Noise Volume",""),
            ("Uniform Volume","Uniform Volume","")
            ),
        default="ExpDensity Volume",
        name = "Volume Type")
    Object.vol_height =     FloatProperty(attr="vol_height",
                                                description="",
                                                min = 0,
                                                default = 1.0)
    Object.vol_steepness =  FloatProperty(attr="vol_steepness",
                                                description="",
                                                min = 0,
                                                default = 1.0)
    Object.vol_sharpness =  FloatProperty(attr="vol_sharpness",
                                                description="",
                                                min = 1.0,
                                                default = 1.0)
    Object.vol_cover =      FloatProperty(attr="vol_cover",
                                                description="",
                                                min = 0.0, max = 1.0,
                                                default = 1)
    Object.vol_density =    FloatProperty(attr="vol_density",
                                                description="Overall density multiplier",
                                                min = 0.1,
                                                default = 1)
    Object.vol_absorp =     FloatProperty(attr="vol_absorp",
                                                description="Absorption coefficient",
                                                min = 0, max = 1,
                                                default = .1)
    Object.vol_scatter =    FloatProperty(attr="vol_scatter",
                                                description="Scattering coefficient",
                                                min = 0,max = 1,
                                                default = .1)
    
def unregister():
    print("Unregistering object properties")
    del Object.ml_enable
    del Object.ml_color
    del Object.ml_power
    del Object.ml_samples
    del Object.ml_double_sided
    del Object.bgp_enable
    del Object.bgp_power
    del Object.bgp_samples
    del Object.bgp_with_caustic
    del Object.bgp_with_diffuse
    del Object.bgp_photon_only
    del Object.vol_enable
    del Object.vol_region
    del Object.vol_height
    del Object.vol_steepness
    del Object.vol_sharpness
    del Object.vol_cover
    del Object.vol_density
    del Object.vol_absorp
    del Object.vol_scatter

