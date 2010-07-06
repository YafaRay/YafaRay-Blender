''' When you write the configuration file the ordering is very much important '''
from  layout_code_2 import DrawPanel

#no common property here

'''name space region context label '''
panel_code = DrawPanel('general_settings','PROPERTIES','WINDOW','render','General Settings')
panel_code.set_file_name('properties_yaf_general_settings.py')

''' each property consists of five parts  - context, name, type, do_implement, label'''

properties = []

''' common properties '''

properties.append(['scene','gs_ray_depth','int',False,'Ray Depth'])
properties.append(['scene','gs_shadow_depth','int',False,'Shadow Depth'])
properties.append(['scene','gs_threads','int',False,'Threads'])
properties.append(['scene','gs_gamma','float',False,'Gamma'])
properties.append(['scene','gs_gamma_input','float',False,'Gamma Input'])
properties.append(['scene','gs_tile_size','int',False,'Tile Size'])
properties.append(['scene','gs_tile_order','enum',False,'Tile order'])
properties.append(['scene','gs_auto_threads','bool',False,'Auto Threads'])
properties.append(['scene','gs_clay_render','bool',False,'Clay Render'])
properties.append(['scene','gs_draw_params','bool',False,'Draw Params'])

panel_code.add_enum('gs_draw_params', 'True', ['scene','gs_custom_string','string',False,'Custom String'])

properties.append(['scene','gs_auto_save','bool',False,'Auto Save'])
properties.append(['scene','gs_auto_alpha','bool',False,'Auto Alpha'])
properties.append(['scene','gs_premult','bool',False,'Premult'])

properties.append(['scene','gs_transp_shad','bool',False,'Transp. Shadow'])
properties.append(['scene','gs_clamp_rgb','bool',False,'Clamp RGB'])
properties.append(['scene','gs_show_sam_pix','bool',False,'Show Sam Pix'])



panel_code.add_properties(properties)

panel_code.add_enum_values('gs_tile_order',['Linear', 'Random'])

''' add constraints '''
panel_code.prop_data['gs_ray_depth'] = {'default' : 2}
panel_code.prop_data['gs_shadow_depth'] = {'default' : 2}
panel_code.prop_data['gs_threads'] = {'default' : 1}
panel_code.prop_data['gs_gamma'] = {'default' : 1.8}
panel_code.prop_data['gs_gamma_input'] = {'default' : 1.8}
panel_code.prop_data['gs_tile_size'] = {'default' : 32}

panel_code.generate_code(8)