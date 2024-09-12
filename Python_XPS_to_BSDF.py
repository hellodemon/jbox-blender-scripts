import bpy

def convert_xps_to_principled_bsdf(obj):
    # Check if the object has any materials
    if not obj or not obj.data.materials:
        print(f"Object '{obj.name}' has no materials or no object selected.")
        return
    
    # Get the active material
    material = obj.active_material
    
    if not material:
        print(f"Object '{obj.name}' has no active material.")
        return
    
    # Ensure the material uses nodes
    if not material.use_nodes:
        print(f"Material '{material.name}' does not use nodes.")
        return
    
    # Access the node tree
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Find the XPS Shader node group
    xps_shader_group = None
    for node in nodes:
        if node.type == 'GROUP' and 'XPS Shader' in node.node_tree.name:
            xps_shader_group = node
            print(f"XPS Shader group found in '{obj.name}': {xps_shader_group.name}")
            break
    
    if not xps_shader_group:
        print(f"XPS Shader group not found in the material of '{obj.name}'.")
        return
    
    # Create a Principled BSDF node
    principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_bsdf.location = (xps_shader_group.location.x + 200, xps_shader_group.location.y)
    print(f"Created Principled BSDF: {principled_bsdf.name}")
    
    # Find or create a Material Output node
    output_node = next((n for n in nodes if n.type == 'OUTPUT_MATERIAL'), None)
    if not output_node:
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (principled_bsdf.location.x + 400, principled_bsdf.location.y)
        print(f"Created new Material Output: {output_node.name}")
    
    # Function to connect a node's output to another node's input
    def connect_node(from_node, from_socket, to_node, to_socket_name):
        try:
            to_socket = to_node.inputs[to_socket_name]
            links.new(from_node.outputs[from_socket], to_socket)
            print(f"Connected {from_node.name} {from_socket} to {to_node.name} {to_socket_name}")
        except Exception as e:
            print(f"Failed to connect {from_node.name} {from_socket} to {to_node.name} {to_socket_name}: {e}")
    
    # Find the Image Texture nodes that are directly connected to the XPS Shader group
    base_color_texture = None
    alpha_texture = None
    
    for link in xps_shader_group.inputs['Diffuse'].links:
        if link.from_node.type == 'TEX_IMAGE':
            base_color_texture = link.from_node
            print(f"Found Image Texture for Base Color: {base_color_texture.name}")
    
    for link in xps_shader_group.inputs['Alpha'].links:
        if link.from_node.type == 'TEX_IMAGE':
            alpha_texture = link.from_node
            print(f"Found Image Texture for Alpha: {alpha_texture.name}")
    
    # Connect the found Image Texture nodes to the Principled BSDF
    if base_color_texture:
        connect_node(base_color_texture, 'Color', principled_bsdf, 'Base Color')
    
    if alpha_texture:
        connect_node(alpha_texture, 'Alpha', principled_bsdf, 'Alpha')
    
    # Connect the Principled BSDF to the Material Output
    connect_node(principled_bsdf, 'BSDF', output_node, 'Surface')
    
    # Remove the old XPS Shader group node
    nodes.remove(xps_shader_group)
    print(f"Removed XPS Shader group and completed conversion for object: {obj.name}")

def convert_selected_objects():
    # Iterate through all selected objects in the context
    selected_objects = bpy.context.selected_objects
    
    for obj in selected_objects:
        if obj.type == 'MESH':  # Check if the object is a mesh
            print(f"Processing object: {obj.name}")
            convert_xps_to_principled_bsdf(obj)

# Convert shaders for all selected objects
convert_selected_objects()
