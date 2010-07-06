from  layout_code_2 import DrawPanel

#no common property here

'''name space region context label '''
panel_code = DrawPanel('world','PROPERTIES','WINDOW','world','YafaRay Background')
panel_code.set_file_name('properties_yaf_world.py')

''' each property consists of five parts  - context, name, type, do_implement, label'''

properties = []

''' common properties '''

properties.append(['scene','bg_type','enum',False,'Yafaray Background'])
properties.append(['scene','bg_power','float',False,'Multiplier for Background Color'])
panel_code.add_properties(properties)

panel_code.add_enum_values('bg_type',['Gradient','Texture','Sunsky','Darktide\'s Sunsky','Single Color'])


''' if false context is scene'''

panel_code.add_enum('bg_type', 'Single Color', ['world','horizon_color','color',True,'Color'])

panel_code.add_enum('bg_type', 'Gradient', ['world','horizon_color','color',True,'Horizon Color'])
panel_code.add_enum('bg_type', 'Gradient', ['world','ambient_color','color',True,'Horizon Ground Color'])
panel_code.add_enum('bg_type', 'Gradient', ['world','zenith_color','color',True,'Zenith Color'])
panel_code.add_enum('bg_type', 'Gradient', ['scene','bg_zenith_ground_color','color',False,'Zenith Ground Color'])



panel_code.add_enum('bg_type', 'Texture', ['scene','bg_use_IBL','bool',False,'Use IBL'])
panel_code.add_enum('bg_type', 'Texture', ['scene','bg_IBL_samples','int',False,'IBL Samples'])
panel_code.add_enum('bg_type', 'Texture', ['scene','bg_rotation','int',False,'Rotation'])


panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_turbidity','float',False,'Turbidity'])

panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_a_var','int',False,'HorBrght'])
panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_b_var','int',False,'HorSprd'])
panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_c_var','int',False,'SunBrght'])
panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_d_var','int',False,'SunSize'])
panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_e_var','int',False,'Backlight'])

panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_from','point',False,'From'])
panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_add_sun','bool',False,'Add Sun'])
panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_sun_power','float',False,'Sun Power'])
panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_background_light','bool',False,'Skylight'])
panel_code.add_enum('bg_type', 'Sunsky', ['scene','bg_light_samples','int',False,'Samples'])


panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_turbidity','int',True,'Turbidity'])

panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_a_var','int',True,'Brightness of horizon gradient'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_b_var','int',True,'Luminance of horizon'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_c_var','int',True,'Solar region intensity'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_d_var','int',True,'Width of circumsolar region'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_e_var','int',True,'Backscattered light'])

panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_from','point',True,'From'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_dsaltitude','int',False,'Altitude'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_add_sun','bool',True,'Add Sun'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_sun_power','float',True,'Sun Power'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_background_light','bool',True,'Add Skylight'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_dsnight','bool',False,'Night'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_dsbright','float',False,'Sky Brightness'])
panel_code.add_enum('bg_type', 'Darktide\'s Sunsky', ['scene','bg_light_samples','int',True,'Samples'])

''' other settings '''
panel_code.add_additional_poll_text('context.world')

panel_code.poll_unreg_module.append('properties_world')

panel_code.builtin_module_and_class_reg.append(['properties_world','WORLD_PT_preview'])
panel_code.builtin_module_and_class_reg.append(['properties_world','WORLD_PT_context_world'])

panel_code.prop_prereq['zenith_color'] = ['blend_sky',True]
panel_code.prop_prereq['ambient_color'] = ['real_sky',True]

panel_code.generate_code(15)

