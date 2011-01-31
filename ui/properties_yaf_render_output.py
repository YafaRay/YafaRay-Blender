import bpy
from yafaray.ui.properties_yaf_render_control import YafarayRenderButtonsPanel

class YAFRENDER_PT_output(YafarayRenderButtonsPanel, bpy.types.Panel):

    bl_label = "Output Options"

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        file_format = rd.file_format

        layout.prop(rd, "filepath", text="")

        split = layout.split()
        col = split.column()
        col.prop(rd, "file_format", text="")
        col.row().prop(rd, "color_mode", text="Color", expand=True)

        col = split.column()
        col.prop(rd, "use_file_extension")
        col.prop(rd, "use_overwrite")
        col.prop(rd, "use_placeholder")

        if file_format in ('AVI_JPEG', 'JPEG'):
            split = layout.split()
            split.prop(rd, "file_quality", slider=True)

        if file_format == 'PNG':
            split = layout.split()
            split.prop(rd, "file_quality", slider=True, text="Compression")

        elif file_format == 'MULTILAYER':
            split = layout.split()

            col = split.column()
            col.label(text="Codec:")
            col.prop(rd, "exr_codec", text="")
            col = split.column()

        elif file_format == 'OPEN_EXR':
            split = layout.split()

            col = split.column()
            col.label(text="Codec:")
            col.prop(rd, "exr_codec", text="")

            subsplit = split.split()
            col = subsplit.column()
            col.prop(rd, "use_exr_half")
            col.prop(rd, "exr_zbuf")

            col = subsplit.column()
            col.prop(rd, "exr_preview")

        elif file_format == 'JPEG2000':
            split = layout.split()
            col = split.column()
            col.label(text="Depth:")
            col.row().prop(rd, "jpeg2k_depth", expand=True)

            col = split.column()
            col.prop(rd, "jpeg2k_preset", text="")
            col.prop(rd, "jpeg2k_ycc")

        elif file_format in ('CINEON', 'DPX'):

            split = layout.split()
            split.label("FIXME: hard coded Non-Linear, Gamma:1.0")
            '''
            col = split.column()
            col.prop(rd, "use_cineon_log", text="Convert to Log")

            col = split.column(align=True)
            col.active = rd.use_cineon_log
            col.prop(rd, "cineon_black", text="Black")
            col.prop(rd, "cineon_white", text="White")
            col.prop(rd, "cineon_gamma", text="Gamma")
            '''

        elif file_format == 'TIFF':
            split = layout.split()
            split.prop(rd, "use_tiff_16bit")

        elif file_format == 'QUICKTIME_CARBON':
            split = layout.split()
            split.operator("scene.render_data_set_quicktime_codec")

        elif file_format == 'QUICKTIME_QTKIT':
            split = layout.split()
            col = split.column()
            col.prop(rd, "quicktime_codec_type", text="Video Codec")
            col.prop(rd, "quicktime_codec_spatial_quality", text="Quality")

            # Audio
            col.prop(rd, "quicktime_audiocodec_type", text="Audio Codec")
            if rd.quicktime_audiocodec_type != 'No audio':
                split = layout.split()
                col = split.column()
                if rd.quicktime_audiocodec_type == 'LPCM':
                    col.prop(rd, "quicktime_audio_bitdepth", text="")

                col = split.column()
                col.prop(rd, "quicktime_audio_samplerate", text="")

                split = layout.split()
                col = split.column()
                if rd.quicktime_audiocodec_type == 'AAC':
                    col.prop(rd, "quicktime_audio_bitrate")

                subsplit = split.split()
                col = subsplit.column()

                if rd.quicktime_audiocodec_type == 'AAC':
                    col.prop(rd, "quicktime_audio_codec_isvbr")

                col = subsplit.column()
                col.prop(rd, "quicktime_audio_resampling_hq")


