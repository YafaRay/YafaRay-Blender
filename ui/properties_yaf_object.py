import bpy


class YAF_PT_object_light(bpy.types.Panel):
    bl_label = "YafaRay Object Properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):

        engine = context.scene.render.engine
        return (context.object.type == "MESH" and (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout
        ob = context.object

        layout.prop(ob, "ml_enable", toggle=True)

        if ob.ml_enable:
            col = layout.column(align=True)
            col.prop(ob, "ml_color")
            col.prop(ob, "ml_power")
            layout.prop(ob, "ml_samples")
            layout.prop(ob, "ml_double_sided")

        layout.prop(ob, "bgp_enable", toggle=True)

        if ob.bgp_enable:
            layout.prop(ob, "bgp_power")
            layout.prop(ob, "bgp_samples")
            split = layout.split()
            split.prop(ob, "bgp_with_diffuse")
            split.prop(ob, "bgp_with_caustic")
            layout.prop(ob, "bgp_photon_only")

        layout.prop(ob, "vol_enable", toggle=True)

        if ob.vol_enable:
            layout.separator()
            layout.prop(ob, "vol_region")
            layout.separator()
            col = layout.column(align=True)
            col.prop(ob, "vol_absorp", text="Absroption")
            col.prop(ob, "vol_scatter", text="Scatter")

            if ob.vol_region == "ExpDensity Volume":
                col = layout.column(align=True)
                col.prop(ob, "vol_height")
                col.prop(ob, "vol_steepness")

            if ob.vol_region == "Noise Volume":
                col = layout.column(align=True)
                col.prop(ob, "vol_sharpness")
                col.prop(ob, "vol_cover")
                col.prop(ob, "vol_density")
