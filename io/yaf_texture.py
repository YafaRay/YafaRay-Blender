import bpy
import re
import os
#import yafrayinterface

def noise2string(ntype):

	if ntype == 'BLENDER_ORIGINAL'  :  return "blender"
	elif ntype == 'ORIGINAL_PERLIN' :  return "stdperlin"
	elif ntype == 'IMPROVED_PERLIN' :  return "newperlin"
	elif ntype == 'VORONOI_F1'      :  return "voronoi_f1"
	elif ntype == 'VORONOI_F2'      :  return "voronoi_f2"
	elif ntype == 'VORONOI_F3'      :  return "voronoi_f3"
	elif ntype == 'VORONOI_F4'      :  return "voronoi_f4"
	elif ntype == 'VORONOI_F2_F1'   :  return "voronoi_f2f1"
	elif ntype == 'VORONOI_CRACKLE' :  return "voronoi_crackle"
	elif ntype == 'CELL_NOISE'      :  return "cellnoise"
	return "newperlin"

#this function is tested under linux
def get_image_filename(filepath):
	path = filepath.replace('//',os.path.expanduser('~')+'/',1)
	return os.path.abspath(path)

class yafTexture:
	def __init__(self, interface):
		self.yi = interface
	
	def writeTexture(self,scene,tex):
		
		name = tex.name
		yi = self.yi
		yi.paramsClearAll()
		
		if tex.yaf_tex_type == 'BLEND' :
			
			yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type BLEND")
			yi.paramsSetString("type", "blend")
			stype = "lin"
			if tex.progression   == 'LINEAR'           :    stype = "lin"
			elif tex.progression == 'QUADRATIC'        :	stype = "quad"
			elif tex.progression == 'EASING'           :	stype = "ease"
			elif tex.progression == 'DIAGONAL'         :	stype = "diag"
			elif tex.progression == 'SPHERICAL'        :	stype = "sphere"
			elif tex.progression == 'QUADRATIC_SPHERE' :	stype = "halo"
			yi.paramsSetString("stype", stype)
		
		
		elif tex.yaf_tex_type == 'CLOUDS':
			
			yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type CLOUDS")
			yi.paramsSetString("type", "clouds")
			
			noise_size = tex.noise_scale
			if  noise_size > 0: noise_size = 1.0/noise_size
			
			yi.paramsSetFloat("size", noise_size)
			
			if tex.noise_type == 'HARD_NOISE' :
				hard = True
			else:
				hard = False
		
			yi.paramsSetBool("hard", hard)
			yi.paramsSetInt("depth", tex.noise_depth)
		
		
		elif tex.yaf_tex_type == 'WOOD':
			
			yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type WOOD")
			yi.paramsSetString("type", "wood")
			
			yi.paramsSetInt("depth", 0)
			
			turb       = 0.0
			noise_size = 0.25
			hard       = True
			
			if tex.wood_type == 'BANDNOISE' or tex.wood_type == 'RINGNOISE':
				
				turb = tex.turbulence
				noise_size = tex.noise_scale
				
				if  noise_size > 0:
					noise_size = 1.0/noise_size
				if tex.noise_type == 'SOFT_NOISE' :
					hard = False
		
			yi.paramsSetFloat("turbulence", turb)
			yi.paramsSetFloat("size", noise_size)
			yi.paramsSetBool("hard", hard )
			
			ts = "bands"
			
			if tex.wood_type == 'RINGS' or tex.wood_type == 'RINGNOISE':
				ts = "rings"
			
			yi.paramsSetString("wood_type", ts )
			yi.paramsSetString("noise_type", noise2string(tex.noise_basis) )
			
			# shape parameter
			
			if tex.noise_basis == 'SAW'  :
				ts="saw"
			elif tex.noise_basis == 'TRI':
				ts="tri"
			else:
				ts = "sin"

			yi.paramsSetString("shape", ts )
		
		elif tex.yaf_tex_type == 'MARBLE':
			
			yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type MARBLE")
			yi.paramsSetString("type", "marble")
			
			yi.paramsSetInt("depth", tex.noise_depth)
			yi.paramsSetFloat("turbulence", tex.turbulence)
			
			noise_size = tex.noise_scale
			if  noise_size > 0:
				noise_size = 1.0/noise_size
			
			if tex.noise_type == 'HARD_NOISE' :
				hard = True
			else:
				hard = False
				
			yi.paramsSetFloat("size", noise_size)
			yi.paramsSetBool("hard", hard )
			
			sharp = 4.0
			if tex.marble_type == 'SOFT':
				sharp = 2.0
			elif tex.marble_type == 'SHARP':
				sharp = 4.0
			elif tex.marble_type == 'SHARPER':
				sharp = 8.0
			
			yi.paramsSetFloat("sharpness", sharp)
			yi.paramsSetString("noise_type", noise2string(tex.noise_basis) )
			
			if tex.noisebasis_2 == 'SAW'  :
				ts="saw"
			elif tex.noisebasis_2 == 'TRI':
				ts="tri"
			else:
				ts = "sin"
			
			yi.paramsSetString("shape", ts)
		
		elif tex.yaf_tex_type == 'VORONOI':
			
			yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type VORONOI")
			yi.paramsSetString("type", "voronoi")
			
			if tex.color_mode == 'POSITION':
				ts = "col1" 
			elif tex.color_mode  == 'POSITION_OUTLINE':
				ts = "col2"
			elif tex.color_mode  == 'POSITION_OUTLINE_INTENSITY':
				ts = "col3"
			else:
				ts = "int"
		
			yi.paramsSetString("color_type", ts)
			
			yi.paramsSetFloat("weight1", tex.weight_1)
			yi.paramsSetFloat("weight2", tex.weight_2)
			yi.paramsSetFloat("weight3", tex.weight_3)
			yi.paramsSetFloat("weight4", tex.weight_4)
			
			yi.paramsSetFloat("mk_exponent", tex.minkovsky_exponent)
			yi.paramsSetFloat("intensity", tex.noise_intensity)
			
			noise_size = tex.noise_scale
			if  noise_size > 0:
				noise_size = 1.0/noise_size
			yi.paramsSetFloat("size", noise_size)
			
			ts = "actual"
			if tex.distance_metric == 'DISTANCE_SQUARED':
				ts = "squared"
			elif tex.distance_metric == 'MANHATTAN':
				ts = "manhattan"
			elif tex.distance_metric == 'CHEBYCHEV':
				ts = "chebychev"
			elif tex.distance_metric == 'MINKOVSKY_HALF':
				ts = "minkovsky_half"
			elif tex.distance_metric == 'MINKOVSKY_FOUR':
				ts = "minkovsky_four"
			elif tex.distance_metric == 'MINKOVSKY':
				ts = "minkovsky"
			
			yi.paramsSetString("distance_metric", ts)
		
		elif tex.yaf_tex_type == 'MUSGRAVE':
			
			yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type MUSGRAVE")
			yi.paramsSetString("type", "musgrave")
			
			ts = "fBm"
			if tex.musgrave_type == 'MULTIFRACTAL'  :
				ts = "multifractal"
			elif tex.musgrave_type == 'RIDGED_MULTIFRACTAL':
				ts = "ridgedmf"
			elif tex.musgrave_type == 'HYBRID_MULTIFRACTAL':
				ts = "hybridmf"
			elif tex.musgrave_type == 'HETERO_TERRAIN':
				ts = "heteroterrain"
			
			yi.paramsSetString("musgrave_type", ts)
			yi.paramsSetString("noise_type", noise2string(tex.noise_basis))
			yi.paramsSetFloat("H", tex.dimension_max)
			yi.paramsSetFloat("lacunarity", tex.lacunarity)
			yi.paramsSetFloat("octaves", tex.octaves)

			noise_size = tex.noise_scale
			if  noise_size > 0:
				noise_size = 1.0/noise_size
			yi.paramsSetFloat("size", noise_size)
			
			yi.paramsSetFloat("intensity", tex.offset)
		
		elif tex.yaf_tex_type == 'DISTORTED_NOISE':
			
			yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type DISTORTED NOISE")
			yi.paramsSetString("type", "distorted_noise")
			
			yi.paramsSetFloat("distort", tex.distortion)
			
			noise_size = tex.noise_scale
			if  noise_size > 0:
				noise_size = 1.0/noise_size
			yi.paramsSetFloat("size", noise_size)
			
			yi.paramsSetString("noise_type1", noise2string(tex.noise_basis))
			yi.paramsSetString("noise_type2", noise2string(tex.noise_distortion))
		
		elif tex.yaf_tex_type == 'IMAGE':
			
			ima = tex.tex_file_name
			#print(str(ima))
			if ima is not None:
				#get image full path
				imagefile = get_image_filename(ima.filepath)
			import os
			if tex.tex_file_name != "" and not os.path.exists(tex.tex_file_name):
				yi.printInfo("Exporter: No valid texture image supplied.")
				return False
			
			
			yi.printInfo("Exporter: Creating Texture: \"" + name + "\" type IMAGE: " + tex.tex_file_name)

			yi.paramsSetString("type", "image")
			yi.paramsSetString("filename", tex.tex_file_name)
				#yi.paramsSetString("filename", imagefile)

			yi.paramsSetBool("use_alpha", tex.use_alpha)
			yi.paramsSetBool("calc_alpha", tex.use_calculate_alpha)
			yi.paramsSetBool("normalmap", tex.use_normal_map)
						
			# repeat
			repeat_x = 1
			repeat_y = 1
				
			if tex.extension == 'REPEAT':
				repeat_x = tex.repeat_x
				repeat_y = tex.repeat_y
				
			yi.paramsSetInt("xrepeat", repeat_x)
			yi.paramsSetInt("yrepeat", repeat_y)
						
			# clipping
			ext = tex.extension
				
			#print tex.getExtend()
			if ext == 'EXTEND':
				yi.paramsSetString("clipping", "extend")
			elif ext == 'CLIP':
				yi.paramsSetString("clipping", "clip")
			elif ext == 'CLIP_CUBE':
				yi.paramsSetString("clipping", "clipcube")
			elif ext == "CHECKER": #Blender.Texture.ExtendModes.CHECKER:
				yi.paramsSetString("clipping", "checker")
				yi.paramsSetBool("even_tiles", tex.checker_even)
				yi.paramsSetBool("odd_tiles", tex.checker_odd)
			else:
				yi.paramsSetString("clipping", "repeat")
				
			# crop min/max
			yi.paramsSetFloat("cropmin_x", tex.crop_min_x)
			yi.paramsSetFloat("cropmin_y", tex.crop_min_y) 
			yi.paramsSetFloat("cropmax_x", tex.crop_max_x)
			yi.paramsSetFloat("cropmax_y", tex.crop_max_y)
				
			# rot90 flag
			#if tex.rot90 != 0:
			yi.paramsSetBool("rot90", tex.use_flip_axis)
		yi.createTexture(name)
	
	def createTextures(self,yi,scene):
		#alternative option: bpy.data.textures
		#objects = scene.objects
		#for item in objects:
		#	for index in range(16):
		#		if not item.active_material.texture_slots[index]:
		#			break
		#		elif item.active_material.use_textures[index]:
		#			tex = item.active_material.texture_slots[index].texture
		#			self.writeTexture(scene, tex)
		textures = bpy.data.textures
		for tex in textures:
			self.writeTexture(scene,tex)
			
