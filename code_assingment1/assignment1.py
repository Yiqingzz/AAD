# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.2,0.2,0.2)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    global geom1_params, cubes, cube_lines
    cubes = []
    cube_lines = []
    geom1_params = {
        "size": 1,
        "y": 10,
        "scale": 1,
    }
    geom1_params = Object.fromEntries(to_js(geom1_params))

    #create materials
    global material, line_material
    color = THREE.Color.new(255,255,255)
    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 0.8
    material.color = color

    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new(0.1,0.1,0.1)

    #generate boxes
    for a in range(1,geom1_params.y):
        j = a
        i = a
        
        for j in range(0, j + 1): 
            
            for i in range(0, i + 1):
                geom = THREE.BoxGeometry.new(geom1_params.size,geom1_params.size,geom1_params.size)
                geom.scale(geom1_params.scale * i * 0.1, geom1_params.scale * i * 0.1, geom1_params.scale * i * 0.1)
                geom.translate(-1/2 *((a-1)-2*i)*geom1_params.size,-geom1_params.size*a,-1/2 *((a-1)-2*j)*geom1_params.size)
                
                
                cube = THREE.Mesh.new(geom, material)
                cubes.append(cube)
                scene.add(cube)

                # draw the edge geometries of the cube
                edges = THREE.EdgesGeometry.new( cube.geometry )
                line = THREE.LineSegments.new( edges, line_material)
                cube_lines.append(line)
                scene.add( line )



    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'size', 1,10,1)
    param_folder.add(geom1_params, 'y', 1,50,1)
    param_folder.add(geom1_params, 'scale', 0,1,0.1)
    param_folder.open()
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
def update_cubes():
    global cubes, cube_lines, material, line_material
    # Make sure if at least one cube is already created and store inside the array "cubes"
    if len(cubes) != 0:
        # Check the amount of cubes inside the array "cubes"
        if len(cubes) != geom1_params.y: # if the amount is not the same as the slider, update the array
            for cube in cubes: scene.remove(cube)
            for line in cube_lines: scene.remove(line)
            cubes = []
            cube_lines = []

            for a in range(1,geom1_params.y):
                j = a
                i = a
                
                for j in range(0, j + 1): 
                    
                    for i in range(0, i + 1):
                        geom = THREE.BoxGeometry.new(geom1_params.size,geom1_params.size,geom1_params.size)
                        geom.scale(geom1_params.scale * i * 0.1, geom1_params.scale * i * 0.1, geom1_params.scale * i * 0.1)
                        geom.translate(-1/2 *((a-1)-2*i)*geom1_params.size,-geom1_params.size*a,-1/2 *((a-1)-2*j)*geom1_params.size)
                        
                        
                        cube = THREE.Mesh.new(geom, material)
                        cubes.append(cube)
                        scene.add(cube)

            

                        edges = THREE.EdgesGeometry.new( cube.geometry )
                        line = THREE.LineSegments.new( edges, line_material)
                        cube_lines.append(line)
                        scene.add( line )
        else: # if the amount doesn't change, only update the parameters of existing cubes
            for i in range(len(cubes)): 
                cube = cubes[i]
                line = cube_lines[i]
                geom = THREE.BoxGeometry.new(geom1_params.size,geom1_params.size,geom1_params.size)
                geom.scale(geom1_params.scale * 0.1, geom1_params.scale * 0.1, geom1_params.scale * 0.1)
                geom.translate(1/2 * geom1_params.size, 0, 1/2 * geom1_params.size)
                cube = THREE.Mesh.new(geom, material)
                cubes.append(cube)
                scene.add(cube)
                edges = THREE.EdgesGeometry.new( cube.geometry )
                line = THREE.LineSegments.new( edges, line_material)
                cube_lines.append(line)
                scene.add( line )
                for a in range(1,geom1_params.y):
                    j = a
                    i = a
                    
                    for j in range(0, j + 1): 
                       
                        for i in range(0, i + 1):
                            geom = THREE.BoxGeometry.new(geom1_params.size,geom1_params.size,geom1_params.size)
                            geom.scale(geom1_params.scale * i * 0.1, geom1_params.scale * i * 0.1, geom1_params.scale * i * 0.1)
                            geom.translate(-1/2 *((a-1)-2*i)*geom1_params.size,-geom1_params.size*a,-1/2 *((a-1)-2*j)*geom1_params.size)
                            
                            
                            cube = THREE.Mesh.new(geom, material)
                            cubes.append(cube)
                            scene.add(cube)
                            

                            edges = THREE.EdgesGeometry.new( cube.geometry )
                            line.geometry = edges

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_cubes()
    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()