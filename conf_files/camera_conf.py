from  layout_code_2 import DrawPanel

#no common property here

panel_code = DrawPanel('camera','PROPERTIES','WINDOW','data','Camera')
panel_code.set_file_name('properties_yaf_camera.py')


''' each property consists of five parts  - context, name, type, do_implement, label'''
    
properties = []

''' common properties '''
properties.append(['camera','camera_type','enum',False,'Yafaray Camera'])
properties.append(['camera','color_data','point',False,'Yafaray Camera Point'])
panel_code.add_properties(properties)

panel_code.add_enum_values('camera_type',['angular','orthographic','perspective','architect'])

''' if false context is scene'''

panel_code.add_enum('camera_type', 'angular', ['camera','lens','float',True,'Angle'])
panel_code.add_enum('camera_type', 'angular', ['camera','max_angle','float',False,'Max Angle'])
panel_code.add_enum('camera_type', 'angular', ['camera','mirrored','bool',False,'Mirrored'])
panel_code.add_enum('camera_type', 'angular', ['camera','circular','bool',False,'Circular'])

panel_code.add_enum('camera_type', 'orthographic', ['camera','ortho_scale','float',True,'Scale'])

panel_code.add_enum('camera_type', 'perspective', ['camera','bokeh_type','enum',False,'Bokeh Type'])
panel_code.add_enum('camera_type', 'perspective', ['camera','aperture','float',False,'Aperture'])
panel_code.add_enum('camera_type', 'perspective', ['camera','dof_distance','float',True,'DOF distance'])
panel_code.add_enum('camera_type', 'perspective', ['camera','bokeh_rotation','float',False,'Bokeh Rotation'])
panel_code.add_enum('camera_type', 'perspective', ['camera','bokeh_bias','enum',False,'Bokeh Bias'])
panel_code.add_enum('camera_type', 'perspective', ['camera','lens','float',True,'Focal Length'])

''' default property is in last position '''
panel_code.add_enum_values('bokeh_type',['Disk2','Triangle','Square','Pentagon','Hexagon','Ring','Disk1'])
panel_code.add_enum_values('bokeh_bias',['Uniform','Center','Edge'])


panel_code.add_enum('camera_type', 'architect', ['camera','bokeh_type','enum',True,'Bokeh Type'])
panel_code.add_enum('camera_type', 'architect', ['camera','aperture','float',True,'Aperture'])
panel_code.add_enum('camera_type', 'architect', ['camera','dof_distance','float',True,'DOF distance'])
panel_code.add_enum('camera_type', 'architect', ['camera','bokeh_rotation','float',True,'Bokeh Rotation'])
panel_code.add_enum('camera_type', 'architect', ['camera','bokeh_bias','enum',True,'Bokeh Bias'])
panel_code.add_enum('camera_type', 'architect', ['camera','lens','float',True,'Focal Length'])

panel_code.add_additional_poll_text('context.camera')

panel_code.prop_prereq['lens']        = ['type','PERSP']
panel_code.prop_prereq['ortho_scale'] = ['type','ORTHO']

panel_code.poll_unreg_module.append('properties_data_camera')

#DATA_PT_context_camera
panel_code.builtin_module_and_class_reg.append(['properties_data_camera','DATA_PT_context_camera'])

panel_code.generate_code(context = 'Camera')