import bpy


class YAF_PT_object_light(bpy.types.Panel):

    bl_label = 'YafaRay Object Properties'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):

        engine = context.scene.render.engine
        return (context.object.type == 'MESH' and (engine in self.COMPAT_ENGINES))

    def draw(self, context):

        layout = self.layout
        split = layout.split()
        col = split.column()

        col.prop(context.object, "ml_enable", text = "Enable Meshlight", toggle = True)

        if context.object.ml_enable:
            col.template_color_wheel(context.object, "ml_color", True, False, False, False)  # prop(context.object,"ml_color", text= "Meshlight Color")
            col.prop(context.object, "ml_power", text = "Power")
            col.prop(context.object, "ml_samples", text = "Samples")
            col.prop(context.object, "ml_double_sided", text = "Double Sided")

        col.prop(context.object, "bgp_enable", text = "Enable Bgportallight", toggle = True)

        if context.object.bgp_enable:
            col.prop(context.object, "bgp_power", text = "Power")
            col.prop(context.object, "bgp_samples", text = "Samples")
            col.prop(context.object, "bgp_with_caustic", text = "With Caustic")
            col.prop(context.object, "bgp_with_diffuse", text = "With Diffuse")
            col.prop(context.object, "bgp_photon_only", text = "Photons Only")

        col.prop(context.object, "vol_enable", text = "Enable Volume", toggle = True)

        if context.object.vol_enable:
            col.prop(context.object, "vol_region", text = "Volume Region")

            if context.object.vol_region == 'ExpDensity Volume':
                col.prop(context.object, "vol_height", text = "Height")
                col.prop(context.object, "vol_steepness", text = "Steepness")

            if context.object.vol_region == 'Noise Volume':
                col.prop(context.object, "vol_sharpness", text = "Sharpness")
                col.prop(context.object, "vol_cover", text = "Cover")
                col.prop(context.object, "vol_density", text = "Density")

            col.prop(context.object, "vol_absorp", text = "Absroption")
            col.prop(context.object, "vol_scatter", text = "Scatter")
