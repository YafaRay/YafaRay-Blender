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
        ob = context.object

        split = layout.split()

        col = split.column()
        col.prop(context.object, "ml_enable", text = "Enable Meshlight", toggle = True)

        if ob.ml_enable:
            col.prop(ob, "ml_color", text = "Meshlight Color")
            col.prop(ob, "ml_power", text = "Power")
            col.prop(ob, "ml_samples", text = "Samples")
            col.prop(ob, "ml_double_sided", text = "Double Sided")

        col.prop(ob, "bgp_enable", text = "Enable Bgportallight", toggle = True)

        if ob.bgp_enable:
            col.prop(ob, "bgp_power", text = "Power")
            col.prop(ob, "bgp_samples", text = "Samples")
            col.prop(ob, "bgp_with_caustic", text = "With Caustic")
            col.prop(ob, "bgp_with_diffuse", text = "With Diffuse")
            col.prop(ob, "bgp_photon_only", text = "Photons Only")

        col.prop(ob, "vol_enable", text = "Enable Volume", toggle = True)

        if ob.vol_enable:
            col.prop(ob, "vol_region", text = "Volume Region")

            if ob.vol_region == 'ExpDensity Volume':
                col.prop(ob, "vol_height", text = "Height")
                col.prop(ob, "vol_steepness", text = "Steepness")

            if ob.vol_region == 'Noise Volume':
                col.prop(ob, "vol_sharpness", text = "Sharpness")
                col.prop(ob, "vol_cover", text = "Cover")
                col.prop(ob, "vol_density", text = "Density")

            col.prop(ob, "vol_absorp", text = "Absroption")
            col.prop(ob, "vol_scatter", text = "Scatter")
