''' When you write the configuration file the ordering is very much important '''
from  layout_code_2 import DrawPanel

#no common property here

'''name space region context label '''
panel_code = DrawPanel('object_light','PROPERTIES','WINDOW','object','Object Light')
panel_code.set_file_name('properties_object_light.py')

''' each property consists of five parts  - context, name, type, do_implement, label'''

properties = []

''' common properties '''

properties.append(['scene','ml_enable','bool',False,'Enable Meshlight'])
properties.append(['scene','bgp_enable','bool',False,'Enable Bgportallight'])
properties.append(['scene','vol_enable','bool',False,'Enable Volume'])

panel_code.add_properties(properties)

panel_code.add_enum('ml_enable', 'True', ['scene','ml_color','color',False,'Meshlight Color'])
panel_code.add_enum('ml_enable', 'True', ['scene','ml_power','float',False,'Power'])
panel_code.add_enum('ml_enable', 'True', ['scene','ml_samples','int',False,'Samples'])
panel_code.add_enum('ml_enable', 'True', ['scene','ml_double_sided','bool',False,'Double Sided'])

panel_code.add_enum('bgp_enable', 'True', ['scene','bgp_power','float',False,'Power'])
panel_code.add_enum('bgp_enable', 'True', ['scene','bgp_samples','int',False,'Samples'])
panel_code.add_enum('bgp_enable', 'True', ['scene','bgp_with_caustic','bool',False,'With Caustic'])
panel_code.add_enum('bgp_enable', 'True', ['scene','bgp_with_diffuse','bool',False,'With Diffuse'])
panel_code.add_enum('bgp_enable', 'True', ['scene','bgp_photon_only','bool',False,'Photons Only'])


panel_code.add_enum('vol_enable', 'True', ['scene','vol_region','enum',False,'Volume Region'])
panel_code.add_enum('vol_enable', 'True', ['scene','vol_absorp','float',False,'Absroption'])
panel_code.add_enum('vol_enable', 'True', ['scene','vol_scatter','float',False,'Scatter'])

panel_code.add_enum_values('vol_region',['ExpDensity Volume','Noise Volume', 'Uniform Volume'])

panel_code.add_enum('vol_region', 'ExpDensity Volume', ['scene','vol_height','float',False,'Height'])
panel_code.add_enum('vol_region', 'ExpDensity Volume', ['scene','vol_steepness','float',False,'Steepness'])

panel_code.add_enum('vol_region', 'Noise Volume', ['scene','vol_sharpness','float',False,'Sharpness'])
panel_code.add_enum('vol_region', 'Noise Volume', ['scene','vol_cover','float',False,'Cover'])
panel_code.add_enum('vol_region', 'Noise Volume', ['scene','vol_density','float',False,'Density'])

'''other settings '''
#panel_code.add_additional_poll_text('context.scene.render')
panel_code.poll_unreg_module.append('properties_object')

panel_code.generate_code(20)
