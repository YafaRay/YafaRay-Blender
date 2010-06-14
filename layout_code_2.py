from copy import deepcopy

class DrawPanel(object):

    '''Generates a panel generating code with user settings'''
       
    def __init__(self,panel,space_type = '',region_type = '',context_name = '',label_name = ''):
        
        self.panel_name  = panel
        self.space       = space_type
        self.region      = region_type
        self.context     = context_name
        self.label       = label_name
        
        #self.row         = []
        #self.column      = []
        self.properties  = []
        self.enumerator  = {}
        self.enum_values = {}
        self.prop_data   = {}
        
        self.prop_ui_data     = {}
        self.prop_implemented = {}
        
        self.poll_text   = "True "
        self.address_to_save = '/home/shuvro/Desktop/Blender/install/linux2/.blender/scripts/ui/panel_code_yafaray.py'
        
        #self.flag = False
        self.COMPAT_ENGINES = ['YAF_RENDER_ENGINE']
    
    def set_file_name(self,file_name):
        self.address_to_save = file_name
    
    def add_additional_poll_text(self,poll_string = ""):
        self.poll_text = poll_string

    def add_properties(self,list_properties):
        '''assign those properties that are general to the context '''
        self.properties = deepcopy(list_properties)
    
    def add_property(self,context,property_name,data_type,is_implemented,label):
        '''assign a property that is general to the context '''
        self.properties.append([context,property_name,data_type,is_implemented,label])
        
    def add_enum_values(self,enum_name,value_list):
        '''add all possible values for a specific enum '''
        self.enum_values[enum_name] = deepcopy(value_list)
    
    def add_enum(self,enum_name,enum_value,enum_prop_list):
        
        '''enum_name       :=  enum name
            enum_value     :=  a specific value of an enum; if it's true enum_prop_list will be displayed in the UI.
            enum_prop_list :=  a list of props and their types; these properties will be displayed if value of enum_name is enum_value
        '''
        
        '''search whether this enum is assigned previously, if not assign '''
        if (enum_name,enum_value) not in self.enumerator.keys():
            self.enumerator[(enum_name,enum_value)] = []
            
        self.enumerator[(enum_name,enum_value)].append(deepcopy(enum_prop_list))
        
        #self.enumerator[(enum_name,enum_value)] = deepcopy(enum_prop_list)
    
    def add_tab(self,num_tab):
        
        string = ""
        for i in range(0,num_tab):
            string += '\t'
        return string
    
    ''' Adds extra parameters to newly created properties if provided '''
    def append_add_prop(self,prop_name,tab_num = 2):
        
        string = ""    
        if prop_name in self.prop_data.keys():
            
            prop_dict = self.prop_data[prop_name]
            for name,value in prop_dict.items():
                
                string += ",\n" + self.add_tab(tab_num)
                string += name + ' = '
                if isinstance(value,str):
                    string += '"' + value + '"'
                else:
                    string += str(value)
        return string
    
    ''' Adds extra UI parameters if provided '''
    def append_ui_prop(self,prop_name):
        
        string = ""
        if prop_name in self.prop_ui_data.keys():
            
            prop_ui_dict = self.prop_ui_data[prop_name]
            for name, value in prop_ui_dict.items():
                string += ', ' + name + '= '
                if isinstance(value,str):
                    string += '"' + value + '"'
                else:
                    string += str(value)
        return string
            
    def create_property(self, prop_context, prop_name, prop_type):
        
        string = ""
        
        if prop_type == "bool" :
            string += 'BoolProperty(attr="' + prop_name + '"'
            string += self.append_add_prop(prop_name)
            string += ')'
        
        elif prop_type == "int" :
            string += 'IntProperty(attr="' + prop_name + '"'
            string += self.append_add_prop(prop_name)
            string += ')'
        
        elif prop_type == "float" :
            string += 'FloatProperty(attr="' + prop_name + '"'
            string += self.append_add_prop(prop_name)
            string += ')'
        
        elif prop_type == "int_vector" :
            string += 'IntVectorProperty(attr="' + prop_name + '"'
            string += self.append_add_prop(prop_name)
            string += ')'
        
        elif prop_type == "float_vector" :
            string += 'FloatVectorProperty(attr="' + prop_name + '"'
            string += self.append_add_prop(prop_name)
            string += ')'
          
        elif prop_type == "enum" :
            print("In the enum block ")
            string += 'EnumProperty(attr="' + prop_name + '",\n'
            string += self.add_tab(1) + 'items = (\n'
            string += self.add_tab(2) + '("' + prop_name + '","' + prop_name + '",""),\n'
            for item in self.enum_values[prop_name]:
                ''' to enhance enum edit here '''  
                string += self.add_tab(2) + '("' + item + '","' + item + '",""),\n'
            string += ')'
            string += self.append_add_prop(prop_name,3)
            string += ',default="'+ item + '")'
        
        #print(string)   
        self.file.write(string + '\n\n')
        
            
    
    def add_properties_rna(self,properties):
       
        #print(properties)
        for prop_context, prop_name, prop_type, prop_implemented,prop_label in properties:
            
            ''' add new properties here if needed. If a label info is added in the property
                specification data this portion and consequent parts may change
            '''
            
            ''' construct nested dict prop_implemented with this if clause '''
            if prop_name not in self.prop_implemented.keys():
                self.prop_implemented[prop_name] = prop_implemented
                print(prop_name)
            
            if not self.prop_implemented[prop_name]:
                #print(prop_name)
                self.create_property(prop_context,prop_name, prop_type)
                self.prop_implemented[prop_name] = True
            
            if prop_type == "enum" :
                self.extract_properties_enum(prop_name)
        
    

    
    def extract_properties_enum(self,prop_name):
        print("prop name :" + prop_name)
        values   = self.enum_values[prop_name]
        
        print(str(values))
                
        for value in values:
            if (prop_name,value) in self.enumerator:
                enum_value_props = self.enumerator[(prop_name,value)]
                if enum_value_props:
                    self.add_properties_rna(enum_value_props)
            else :
                print("enum with no associated property")
                            
    
    def draw_header_poll(self):
        
        '''define header '''
        string  = 'class YAF_PT_' + self.panel_name +'(bpy.types.Panel):\n\n'
        string += '\tbl_label = \'' + self.label + '\'\n'
        string += '\tbl_space_type = \'' + self.space + '\'\n'
        string += '\tbl_region_type = \'' + self.region + '\'\n'
        string += '\tbl_context = \'' + self.context + '\'\n'
        string += '\tCOMPAT_ENGINES =' + str(self.COMPAT_ENGINES) + '\n\n\n'
        
        '''poll function started '''
        string += '\tdef poll(self, context):\n\n'
        string += '\t\tengine = context.scene.render.engine\n'
        string += '\t\treturn ' + '(' + self.poll_text + ' and  (engine in self.COMPAT_ENGINES) ) \n'
        
        self.file.write(string)
    
    def add_props(self,prop_list,tab_count,break_column = 4):
        
        i =  0
        
        for prop_context, prop_name, prop_type, prop_implemented, prop_label in prop_list:
            
            string = ""
            print("info : " + prop_context + "  " + prop_name + "  " + prop_type + "  " + str(prop_implemented) + "i  " + str(i))
            
            ''' update prop_ui_data nested dict or create new if not exists '''
            if prop_name not in self.prop_ui_data.keys():
                
                if prop_type == "enum":
                    self.prop_ui_data[prop_name] = {'text' : ""}
                else:
                    self.prop_ui_data[prop_name] = {'text' : prop_label}
            
            else:
                
                if prop_type == "enum":
                    self.prop_ui_data[prop_name].update(text="")
                else:
                    self.prop_ui_data[prop_name].update(text = prop_label)
                
            
            if i == break_column :
                i = 0
                ''' creates a new column '''
                string += self.add_tab(tab_count) + 'col = split.column()\n'
                
            ''' add property '''
            if prop_type == "enum" :
                string += "\n" + self.add_tab(tab_count) + 'col.label(text="' + prop_name + '")\n'
                string += self.add_tab(tab_count) + 'col.prop(context.'+ prop_context + ',"' +  prop_name + '"' + self.append_ui_prop(prop_name) +')\n'
            else:
                string += self.add_tab(tab_count) + 'col.prop(context.'+ prop_context + ',"' +  prop_name + '"' + self.append_ui_prop(prop_name) + ')\n'
                #,text="'+ prop_name + '"
            
            #print("before write : " + string)
            self.file.write(string)

            ''' if the property is enum type handle that '''
            if prop_type == "enum":
                self.handle_enum(prop_name,prop_context,tab_count)
            i = i + 1            
        

    def handle_enum(self,enum_name,enum_context,num_tab):
        
        prop_list = []
        values = self.enum_values[enum_name]
        for item in values :
            
            string = ""
            ''' watch this line. there might be a error here. '''
            if (enum_name,item) in self.enumerator:
                string += "\n" + self.add_tab(num_tab) + 'if context.' + enum_context + "." + enum_name + ' == \'' + str(item) + '\':\n'
                self.file.write(string)
                prop_list = self.enumerator[(enum_name,item)]
            
                if prop_list:
                    print(prop_list)
                    #self.flag = True
                    self.add_props(prop_list,num_tab +  1)
        
        self.file.write("\n")
        
    def draw_register_unregister(self):
            
        string =  "classes = [" + 'YAF_PT_' + self.panel_name +"]\n\n"
        string += "def register():\n"
        string += "\tregister = bpy.types.register\n"
        string += "\tfor cls in classes:\n"
        string += self.add_tab(2) + "register(cls)\n\n\n"
        string += "def unregister():\n"
        string += "\tunregister = bpy.types.unregister\n"
        string += "\tfor cls in classes:\n"
        string += self.add_tab(2) + "unregister(cls)\n\n\n"
        string += 'if __name__ == "__main__":\n'
        string += self.add_tab(1) + "register()\n"
        
        self.file.write(string)
    
    
    def generate_code(self):

        self.file = open(self.address_to_save,'w')
        
        string = "import bpy\n\n\n"
        string += 'FloatProperty = bpy.types.Scene.FloatProperty\n'
        string += 'IntProperty = bpy.types.Scene.IntProperty\n'
        string += 'BoolProperty = bpy.types.Scene.BoolProperty\n'
        string += 'CollectionProperty = bpy.types.Scene.CollectionProperty\n'
        string += 'EnumProperty = bpy.types.Scene.EnumProperty\n'
        string += 'FloatVectorProperty = bpy.types.Scene.FloatVectorProperty\n'
        string += 'IntVectorProperty = bpy.types.Scene.IntVectorProperty\n\n\n'
        
        self.file.write(string)
        string = ""
        
        self.add_properties_rna(self.properties)
        self.draw_header_poll()
        
        ''' draw method started '''
        ''' common parts '''
        
        string = '\n\n\tdef draw(self, context):\n\n'
        string += '\t\tlayout = self.layout\n'
        #string += '\t\t' + self.panel_name + ' = context.'+ self.panel_name + '\n\n'
        
        ''' some config '''
        string += '\t\tsplit = layout.split()\n'
        string += '\t\tcol = split.column()\n\n'
        self.file.write(string)
        
        self.add_props(self.properties,2)
        self.draw_register_unregister()
        
        
        self.file.close()



if __name__  == '__main__' :
    
    panel_code = DrawPanel('lamp','PROPERTIES','WINDOW','data','Lamp')
    panel_code.set_file_name('panel_code.py')
    
    ''' each property consists of five parts  - context, name, type, do_implement label'''
    
    properties = []

    
    properties.append(['scene','lamp_type','enum',False,'Light Type'])
    properties.append(['lamp','color','bpy_prop_array',True,'Color'])
    properties.append(['lamp','energy','float',True,'Power'])
    
    panel_code.add_properties(properties)
    
    panel_code.add_enum_values('lamp_type',['Area','Directional','MeshLight','Point','Sphere','Spot','Sun'])
    
    panel_code.add_enum('lamp_type', 'Area', ['lamp','shadow_ray_samples','int',True,'Samples'])
    panel_code.add_enum('lamp_type', 'Area', ['lamp','size','float',True,'SizeX'])
    panel_code.add_enum('lamp_type', 'Area', ['lamp','size_y','float',True,'SizeY'])
    panel_code.add_enum('lamp_type', 'Area', ['scene','create_geometry','bool',False,'Create Geometry'])
    
    
    panel_code.add_enum('lamp_type', 'Directional', ['scene','infinite','bool',False,'Infinite'])
    panel_code.add_enum('lamp_type', 'Directional', ['lamp','shadow_soft_size','float',True,'Radius']) #radius
    
    ''' we are keeping no option for MeshLight and Point here '''
    
    panel_code.add_enum('lamp_type', 'Sphere', ['lamp','shadow_soft_size','float',True,'Radius'])
    panel_code.add_enum('lamp_type', 'Sphere', ['lamp','shadow_ray_samples','int',True,'Samples'])
    panel_code.add_enum('lamp_type', 'Sphere', ['scene','create_geometry','bool',False,'Create Geometry'])
    
    panel_code.add_enum('lamp_type', 'Spot', ['lamp','spot_blend','float',True,'Blend']) #blend
    panel_code.add_enum('lamp_type', 'Spot', ['lamp','spot_size','int',True,'Cone Angle']) #cone_angle
    panel_code.add_enum('lamp_type', 'Spot', ['scene','spot_soft_shadows','bool',False,'Soft Shadow'])
    panel_code.add_enum('lamp_type', 'Spot', ['scene','shadow_fuzzyness','float',False,'Shadow Fuzzyness'])
    panel_code.add_enum('lamp_type', 'Spot', ['scene','photon_only','bool',False,'Photon Only'])
    panel_code.add_enum('lamp_type', 'Spot', ['lamp','shadow_ray_samples','int',True,'Samples'])
    
    
    panel_code.add_enum('lamp_type', 'Sun', ['scene','angle','int',False,'Angle'])
    panel_code.add_enum('lamp_type', 'Sun', ['lamp','shadow_ray_samples','int',True,'Samples'])
    
    ''' add constraints '''
    panel_code.prop_data['angle'] = {'min' : 0, 'max' : 80}
    
    panel_code.add_additional_poll_text('context.lamp')
    

    panel_code.generate_code()
    