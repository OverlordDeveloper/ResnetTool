import glfw
from OpenGL.GL import *
import numpy as np
import imgui
from imgui.integrations.glfw import GlfwRenderer
import cv2
from utils import create_shader_program, load_texture
from pyrr import Matrix44
from camera import Camera
from primitives import create_primitive_rectangle

Width = 800
Height = 600
def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

    Width = width
    Height = height
    

# Initialize the library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(Width, Height, "OpenGL with glfw", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# Make the window's context current
glfw.make_context_current(window)
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
# Initialize ImGui
imgui.create_context()
imgui_renderer = GlfwRenderer(window)

shader_program = create_shader_program('shaders/vertex.glsl', 'shaders/fragment.glsl')

rect_data = create_primitive_rectangle()

# Load a texture
texture1 = load_texture(rf"C:\Users\Horia\source\repos\PythonOpengl/bird.jpg")  # Replace with your texture path

def draw_rectangle(position):
    model = Matrix44.from_translation(position, dtype=np.float32)
    model_location = glGetUniformLocation(shader_program, "model")
    glUniformMatrix4fv(model_location, 1, GL_FALSE, model)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture1)
    glUseProgram(shader_program)
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

positions = [
        [0.0, 0.0, 0.0],   # Center
        [-0.75, 0.75, 0.0], # Top-left
        [0.75, 0.75, 0.0],  # Top-right
        [-0.75, -0.75, 0.0],# Bottom-left
        [0.75, -0.75, 0.0], # Bottom-right
    ]


camera = Camera()

last_x, last_y = 400, 300
first_mouse = True

def mouse_callback(window, xpos, ypos):
    global last_x, last_y, first_mouse
    if first_mouse:
        last_x, last_y = xpos, ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos  # Reversed since y-coordinates go from bottom to top

    last_x = xpos
    last_y = ypos

    camera.process_mouse_movement(xoffset, yoffset)

def scroll_callback(window, xoffset, yoffset):
    camera.process_mouse_scroll(yoffset)

glfw.set_cursor_pos_callback(window, mouse_callback)
glfw.set_scroll_callback(window, scroll_callback)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


# Main application loop
last_frame_time = 0.0

while not glfw.window_should_close(window):
    # Poll for and process events


        # Time management
    current_frame_time = glfw.get_time()
    delta_time = current_frame_time - last_frame_time
    last_frame_time = current_frame_time

    # Process input
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.process_keyboard("FORWARD", delta_time)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.process_keyboard("BACKWARD", delta_time)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.process_keyboard("LEFT", delta_time)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.process_keyboard("RIGHT", delta_time)


    glfw.poll_events()
    imgui_renderer.process_inputs()

    
    view = camera.get_view_matrix()
    projection = Matrix44.perspective_projection(camera.zoom, Width / Height, 0.1, 100.0)

    # Start a new ImGui frame
    imgui.new_frame()

    # ImGui controls
    imgui.begin("Control Panel")
    if imgui.button("Reload Texture"):
        texture1 = load_texture(rf"C:\Users\Horia\source\repos\PythonOpengl/bird.jpg")
    imgui.end()

    glUseProgram(shader_program)

    view_loc = glGetUniformLocation(shader_program, "view")
    projection_loc = glGetUniformLocation(shader_program, "projection")
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
    # Rendering
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for pos in positions:
        draw_rectangle(pos)

    # Render ImGui
    imgui.render()
    imgui_renderer.render(imgui.get_draw_data())

    # Swap front and back buffers
    glfw.swap_buffers(window)

# Clean up
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO, EBO])
glDeleteProgram(shader_program)

imgui_renderer.shutdown()
glfw.terminate()