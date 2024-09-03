
from OpenGL.GL import *
import cv2
# Compile shaders and link them
def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def create_shader_program(vertex_path, fragment_path):

    with open(vertex_path, 'r') as file:
        vertex_source = file.read().rstrip()

    with open(fragment_path, 'r') as file:   
        fragment_source = file.read().rstrip()

    vertex = compile_shader(vertex_source, GL_VERTEX_SHADER)
    fragment = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(program))
    glDeleteShader(vertex)
    glDeleteShader(fragment)
    return program

# Function to load a texture using OpenCV
def load_texture(path, width = 256, height = 256):
    image = cv2.imread(path)
    if image is None:
        raise Exception(f"Failed to load image at {path}")
    
    # Ensure the image has 3 channels (RGB)
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 0)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    image = cv2.resize(image, (width, height))

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)  # Unbind texture after configuration
    return texture

