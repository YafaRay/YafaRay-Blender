import bpy


class YAF_PT_strand_settings(bpy.types.Panel):
    bl_label = 'Strand Settings'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'particle'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(cls, context):

        psys = context.object.particle_systems
        engine = context.scene.render.engine
        return (psys and (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout

        yaf_mat = context.object.active_material
        if yaf_mat:
            tan = yaf_mat.strand

            split = layout.split()

            col = split.column()
            sub = col.column(align=True)
            sub.label(text="Size:")
            sub.prop(tan, "root_size", text="Root")
            sub.prop(tan, "tip_size", text="Tip")
            sub = col.column()
            col.prop(tan, "shape")
            col.prop(tan, "use_blender_units")

            col = split.column()
            col.label(text="Shading:")
            col.prop(tan, "width_fade")
            ob = context.object
            if ob and ob.type == 'MESH':
                col.prop_search(tan, "uv_layer", ob.data, "uv_textures", text="")
            else:
                col.prop(tan, "uv_layer", text="")
