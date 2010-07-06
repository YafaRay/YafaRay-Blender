''' When you write the configuration file the ordering is very much important '''
from  layout_code_2 import DrawPanel



'''name space region context label '''
panel_code = DrawPanel('AA_settings','PROPERTIES','WINDOW','render','AA Settings')
panel_code.set_file_name('properties_yaf_AA_settings.py')

''' each property consists of five parts  - context, name, type, do_implement, label'''

properties = []

''' common properties '''

properties.append(['scene','AA_min_samples','int',False,'AA Samples'])
properties.append(['scene','AA_inc_samples','int',False,'AA Inc. Samples'])
properties.append(['scene','AA_passes','int',False,'AA Passes'])
properties.append(['scene','AA_threshold','float',False,'AA Threshold'])
properties.append(['scene','AA_pixelwidth','float',False,'AA Pixelwidth'])
properties.append(['scene','AA_filter_type','enum',False,'AA Filter Type'])

panel_code.add_properties(properties)

panel_code.add_enum_values('AA_filter_type',['Box', 'Mitchell', 'Gauss'])

''' add constraints '''
panel_code.prop_data['AA_min_samples'] = {'default' : 1}
panel_code.prop_data['AA_inc_samples'] = {'default' : 1}
panel_code.prop_data['AA_passes'] = {'default' : 1}
panel_code.prop_data['AA_threshold'] = {'default' : 0.05}
panel_code.prop_data['AA_pixelwidth'] = {'default' : 1.5}

panel_code.generate_code(3)