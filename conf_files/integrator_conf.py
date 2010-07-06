''' When you write the configuration file the ordering is very much important '''
from  layout_code_2 import DrawPanel

#no common property here

'''name space region context label '''
panel_code = DrawPanel('render','PROPERTIES','WINDOW','render','Yafaray Integrator')
panel_code.set_file_name('properties_yaf_integrator.py')

''' each property consists of five parts  - context, name, type, do_implement, label'''

properties = []

''' common properties '''

properties.append(['scene','intg_light_method','enum',False,'Lighting Methods'])

panel_code.add_properties(properties)

panel_code.add_enum_values('intg_light_method',['Direct Lighting','Photon Mapping','Pathtracing', 'Debug','Bidirectional'])

panel_code.add_enum('intg_light_method', 'Direct Lighting', ['scene','intg_use_caustics','bool',False,'Use Caustics'])
panel_code.add_enum('intg_light_method', 'Direct Lighting', ['scene','intg_use_AO','bool',False,'Use AO'])

'''this is added for the new version '''
panel_code.add_enum('intg_use_caustics', 'True', ['scene','intg_photons','int',False,'Photons'])
panel_code.add_enum('intg_use_caustics', 'True', ['scene','intg_caustic_mix','int',False,'Caustic Mix'])
panel_code.add_enum('intg_use_caustics', 'True', ['scene','intg_caustic_depth','int',False,'Caustic Depth'])
panel_code.add_enum('intg_use_caustics', 'True', ['scene','intg_caustic_radius','float',False,'Caustic Radius'])

panel_code.add_enum('intg_use_AO', 'True', ['scene','intg_AO_samples','int',False,'AO Samples'])
panel_code.add_enum('intg_use_AO', 'True', ['scene','intg_AO_distance','float',False,'AO Distance'])
panel_code.add_enum('intg_use_AO', 'True', ['scene','intg_AO_color','color',False,'AO Color'])
''' bool addition end '''



panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_bounces','int',False,'Depth'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_photons','int',True,'Diff. Photons'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_diffuse_radius','float',False,'Diff. Radius'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_cPhotons','int',False,'Caus. Photons'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_caustic_radius','float',True,'Caus. Radius'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_search','int',False,'Search'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_caustic_mix','int',True,'Caus. Mix'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_final_gather','bool',False,'Final Gather'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_fg_bounces','int',False,'FG Bounces'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_fg_samples','int',False,'FG Samples'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_show_map','bool',False,'Show Map'])
panel_code.add_enum('intg_light_method', 'Photon Mapping', ['scene','intg_use_bg','bool',False,'Use Background'])


panel_code.add_enum('intg_light_method', 'Pathtracing', ['scene','intg_caustic_method','enum',False,'Caustic Method'])
'''the placement of this line may have to be changed '''
panel_code.add_enum_values('intg_caustic_method',['None','Path','Path+Photon','Photon'])


panel_code.add_enum('intg_light_method', 'Pathtracing', ['scene','intg_path_samples','int',False,'Path Samples'])
panel_code.add_enum('intg_light_method', 'Pathtracing', ['scene','intg_bounces','int',True,'Depth'])
panel_code.add_enum('intg_light_method', 'Pathtracing', ['scene','intg_no_recursion','bool',False,'No Recursion'])
panel_code.add_enum('intg_light_method', 'Pathtracing', ['scene','intg_use_bg','bool',True,'Use Background'])



panel_code.add_enum('intg_caustic_method', 'Photon', ['scene','intg_photons','int',True,'Photons'])
panel_code.add_enum('intg_caustic_method', 'Photon', ['scene','intg_caustic_mix','int',True,'Caus. Mix'])
panel_code.add_enum('intg_caustic_method', 'Photon', ['scene','intg_caustic_depth','int',True,'Caus. Depth'])
panel_code.add_enum('intg_caustic_method', 'Photon', ['scene','intg_caustic_radius','float',True,'Caus. Radius'])

panel_code.add_enum('intg_caustic_method', 'Path+Photon', ['scene','intg_photons','int',True,'Photons'])
panel_code.add_enum('intg_caustic_method', 'Path+Photon', ['scene','intg_caustic_mix','int',True,'Caus. Mix'])
panel_code.add_enum('intg_caustic_method', 'Path+Photon', ['scene','intg_caustic_depth','int',True,'Caus. Depth'])
panel_code.add_enum('intg_caustic_method', 'Path+Photon', ['scene','intg_caustic_radius','float',True,'Caus. Radius'])

panel_code.add_enum('intg_light_method', 'Debug', ['scene','intg_debug_type','enum',False,'Debug Type'])
panel_code.add_enum_values('intg_debug_type',['N','dPdU','dPdV','NU','NV','dSdU','dSdV'])
panel_code.add_enum('intg_light_method', 'Debug', ['scene','intg_show_perturbed_normals','bool',False,'Perturbed Normals'])



#for item in panel_code.enumerator:
#    print(item)

'''other settings '''
panel_code.add_additional_poll_text('context.scene.render')

panel_code.generate_code(20)