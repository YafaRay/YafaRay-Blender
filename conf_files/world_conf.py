from  layout_code_2 import DrawPanel

#no common property here

'''name space region context label '''
panel_code = DrawPanel('world','PROPERTIES','WINDOW','world','YafaRay Background')
panel_code.set_file_name('properties_yaf_world.py')

''' each property consists of five parts  - context, name, type, do_implement, label'''

properties = []

''' common properties '''

properties.append(['world','bg_type','enum',False,'Yafaray Background'])
properties.append(['world','bg_power','float',False,'Multiplier for Background Color'])
panel_code.add_properties(properties)

panel_code.add_enum_values('bg_type',['Gradient','Texture','Sunsky','Darktide\'s Sunsky','Single Color'])


''' if false context is scene'''

panel_code.add_enum('bg_type', 'Single Color', ['world','horizon_color','color',True,'Color'])

panel_code.add_enum('bg_type', 'Gradient', ['world','horizon_color','color',True,'Horizon Color'])
panel_code.add_enum('bg_type', 'Gradient', ['world','ambient_color','color',True,'Horizon Ground Color'])
panel_code.add_enum('bg_type', 'Gradient', ['world','zenith_color','color',True,'Zenith Color'])
panel_code.add_enum('bg_type', 'Gradient', ['world','bg_zenith_ground_color','color',False,'Zenith Ground Color'])



panel_code.add_enum('bg_type', 'Texture', ['world','bg_use_IBL','bool',False,'Use IBL'])
panel_code.add_enum('bg_type', 'Texture', ['world','bg_IBL_samples','int',False,'IBL Samples'])
panel_code.add_enum('bg_type', 'Texture', ['world','bg_rotation','int',False,'Rotation'])


panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_turbidity','float',False,'Turbidity'])

panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_a_var','float',False,'HorBrght'])
panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_b_var','float',False,'HorSprd'])
panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_c_var','float',False,'SunBrght'])
panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_d_var','float',False,'SunSize'])
panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_e_var','float',False,'Backlight'])

panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_from','point',False,'From'])
panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_add_sun','bool',False,'Add Sun'])
panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_sun_power','float',False,'Sun Power'])
panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_background_light','bool',False,'Skylight'])
panel_code.add_enum('bg_type', 'Sunsky', ['world','bg_light_samples','int',False,'Samples'])


panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_turbidity','int',True,'Turbidity'])

panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_a_var','float',True,'Brightness of horizon gradient'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_b_var','float',True,'Luminance of horizon'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_c_var','float',True,'Solar region intensity'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_d_var','float',True,'Width of circumsolar region'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_e_var','float',True,'Backscattered light'])

panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_from','point',True,'From'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_dsaltitude','float',False,'Altitude'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_add_sun','bool',True,'Add Sun'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_sun_power','float',True,'Sun Power'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_background_light','bool',True,'Add Skylight'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_dsnight','bool',False,'Night'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_dsbright','float',False,'Sky Brightness'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['world','bg_light_samples','int',True,'Samples'])

''' other settings '''
panel_code.add_additional_poll_text('context.world')

panel_code.poll_unreg_module.append('properties_world')
panel_code.poll_unreg_module.append('properties_texture')

panel_code.builtin_module_and_class_reg.append(['properties_world','WORLD_PT_preview'])
panel_code.builtin_module_and_class_reg.append(['properties_world','WORLD_PT_context_world'])

panel_code.prop_prereq['zenith_color'] = ['blend_sky',True]
panel_code.prop_prereq['ambient_color'] = ['use_sky_real',True]

panel_code.generate_code(context = 'World', break_value = 15)

