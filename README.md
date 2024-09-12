
# JBOX'S *~ Quality of Life ~* Blender Scripts!

Because I *refuse* to make addons, you get **scripts** instead.

![alt text](https://i.imgur.com/hdfciML.png "hello there, nosy")

## 🪄 Multi-Selection Shader Properties Changer
This script lets you change the properties for the materials of multiple selected objects in your scene, such as specular, metallic, roughness & sheen.

### Requirements
- Blender **3.0** and **above**

### How to Use
- **Open** Blender
- **Open** your `.blend` project file
- **Select** every object you want to apply the script to
- **Navigate to your Scripts tab**
- **Click** `+New`
- **Paste** the script into the text editor
- **Run**

You're all set.

> [!TIP]  
> This script also works with **Subsurface, Anisotrophic, Clearcoat, IOR, Transmission, Alpha** And basically any setting on the **Principled BSDF shader** that has a slider.

 #### P.S For the Blender 4.0 Version
 You want to replace `"Specular"` with `"IOR"`, by-the-by.

 ### Script
```
import bpy
for mat in bpy.data.materials:
    if not mat.use_nodes:
        mat.specular_intensity = 0
        continue
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Specular"].default_value = 0
```

![alt text](https://i.imgur.com/hdfciML.png "hello there, nosy")

 ## 🎈 Multi-Selection Alpha Changer
This script lets you change the Alpha Mode for the materials of multiple selected objects in your scene.

### Requirements
- Blender **3.0** and **above**

### How to Use
- **Open** Blender
- **Open** your `.blend` project file
- **Select** every object you want to apply the script to
- **Navigate to your Scripts tab**
- **Click** `+New`
- **Paste** the script into the text editor
- **Run**

You're all set.

> [!TIP]  
> This script also works with Shadow Mode. Just change `slot.material.blend_method` **to** `slot.shadow.blend_method`

  ### Script
```
import bpy

# Check if the current context has selected objects
if bpy.context.selected_objects:
    for ob in bpy.context.selected_objects:
        for slot in ob.material_slots:
            if slot.material:
                slot.material.blend_method = 'OPAQUE'
else:
    print("No objects selected in the Blender scene.")
```

![alt text](https://i.imgur.com/hdfciML.png "hello there, nosy")

 ## 🎈 XPS Shader to Principled BSDF
 This script allows you to convert any object using the ~dreaded~ XPS Shader to a standard Principled BSDF shader. It also keeps your diffuse image texture connected to the base color node so you don't have to reapply it for every object. 
*Mazel tov.*

### Requirements
- Any Blender version that is **compatible** with *johnzero7's* [XPS Tools.](https://github.com/johnzero7/XNALaraMesh) This was primarily tested with Blender 3.6.2 because that's what I use to import models via XPS Tools.
- You will also need *johnzero7's* [XPS Tools](https://github.com/johnzero7/XNALaraMesh) as this is a script centered around `.xps`, `.mesh.ascii`, & `.mesh` files.

### How to Use
- **Open** Blender
- **Open** your `.blend` project file
- **Select** every object you want to apply the script to
- **Navigate to your Scripts tab**
- **Click** `Open`
- **Locate** `Python_XPS_to_BSDF.py`
- **Run**

You're all set.

> [!NOTE]  
> I wrote a tutorial on how to just convert entire maps formated for [XNALara to `.fbx` with Noesis](https://docs.google.com/document/d/1oSynsP2h4GyJX-zscrNznz7cLX4D7smfyjsD6iq3RO4/edit?usp=sharing), but I find this insanely more convenient for character models, props and maps than going through all the rigmarole. 
