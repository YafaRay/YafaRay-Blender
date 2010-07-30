from  layout_code_2 import DrawPanel


'''name space region context label '''
panel_code = DrawPanel('material','PROPERTIES','WINDOW','material','Yafaray Integrator')
panel_code.set_file_name('properties_yaf_material.py')


''' each property consists of five parts  - context, name, type, do_implement, label'''
properties = []


''' common properties '''
properties.append(['material','mat_type','enum',False,'Material Types'])
panel_code.add_properties(properties)

panel_code.add_enum_values('mat_type',['shinydiffusemat', 'glossy','coated_glossy', 'glass', 'blend'])

panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_color','color',False,'Color'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_mirror_color','color',False,'Mirror Color'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_diffuse_reflect','float',False,'Diffuse Reflection'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_mirror_strength','float',False,'Mirror Strength'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_transparency','float',False,'Transparency'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_translucency','float',False,'Translucency'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_transmit_filter','float',False,'Transmit Filter'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_emit','float',False,'Emit'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_fresnel_effect','bool',False,'Fresnel Effect'])
panel_code.add_enum('mat_type', 'shinydiffusemat', ['material','mat_brdf_type','enum',False,'BRDF Type'])

panel_code.add_enum_values('mat_brdf_type',['Oren-Nayar','Normal(Lambert)'])

panel_code.add_enum('mat_type', 'glossy', ['material','mat_diff_color','color',False,'Diffuse Color'])
panel_code.add_enum('mat_type', 'glossy', ['material','mat_glossy_color','color',False,'Glossy Color'])
panel_code.add_enum('mat_type', 'glossy', ['material','mat_diffuse_reflect','float',True,'Diffuse Reflection'])
panel_code.add_enum('mat_type', 'glossy', ['material','mat_glossy_reflect','float',False,'Glossy Reflection'])
panel_code.add_enum('mat_type', 'glossy', ['material','mat_exponent','float',False,'Exponent'])
panel_code.add_enum('mat_type', 'glossy', ['material','mat_sigma','float',False,'Sigma'])
panel_code.add_enum('mat_type', 'glossy', ['material','mat_as_diffuse','bool',False,'As Diffuse'])
panel_code.add_enum('mat_type', 'glossy', ['material','mat_anisotropic','bool',False,'Anisotropic Color'])
panel_code.add_enum('mat_type', 'glossy', ['material','mat_brdf_type','enum',True,'BRDF Type'])



panel_code.add_enum('mat_type', 'coated_glossy', ['material','mat_diff_color','color',True,'Diffuse Color'])
panel_code.add_enum('mat_type', 'coated_glossy', ['material','mat_glossy_color','color',True,'Glossy Color'])
panel_code.add_enum('mat_type', 'coated_glossy', ['material','mat_diffuse_reflect','float',True,'Diffuse Reflection'])
panel_code.add_enum('mat_type', 'coated_glossy', ['material','mat_glossy_reflect','float',True,'Glossy Reflection'])
panel_code.add_enum('mat_type', 'coated_glossy', ['material','mat_exponent','float',True,'Exponent'])
panel_code.add_enum('mat_type', 'coated_glossy', ['material','mat_as_diffuse','bool',True,'As Diffuse'])
panel_code.add_enum('mat_type', 'coated_glossy', ['material','mat_anisotropic','bool',True,'Anisotropic Color'])
panel_code.add_enum('mat_type', 'coated_glossy', ['material','mat_ior','float',False,'IOR'])


panel_code.add_enum('mat_type', 'glass', ['material','mat_absorp_color','color', False,'Absorption Color'])
panel_code.add_enum('mat_type', 'glass', ['material','mat_absorp_distance','float', False,'Absorption Distance'])
panel_code.add_enum('mat_type', 'glass', ['material','mat_filter_color','color', False,'Filter Color'])
panel_code.add_enum('mat_type', 'glass', ['material','mat_mirror_color','color', True,'Absorption Color'])
panel_code.add_enum('mat_type', 'glass', ['material','mat_ior','float', True,'IOR'])
panel_code.add_enum('mat_type', 'glass', ['material','mat_transmit_filter','float', True,'Transmit Filter'])
panel_code.add_enum('mat_type', 'glass', ['material','mat_dispersion_power','float', False,'Dispersion Power'])
panel_code.add_enum('mat_type', 'glass', ['material','mat_fake_shadows','bool', False,'Fake Shadows'])

#needs manual tuning later
#panel_code.add_enum('mat_type', 'blend', ['material','mat_mat1','enum', True,'Material 1'])
#panel_code.add_enum('mat_type', 'blend', ['material','mat_mat2','enum', True,'Material 2'])
panel_code.add_enum('mat_type', 'blend', ['material','mat_blend_value','float', False,'Blend Value'])


panel_code.add_additional_poll_text('context.material')
    
panel_code.poll_unreg_module.append('properties_material')
    
    
panel_code.generate_code(context = 'Material', break_value = 20)




