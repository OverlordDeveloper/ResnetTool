import numpy as np
from OpenGL.GL import *

def create_primitive_rectangle():
        # Define the vertices and texture coordinates for a square
    vertices = np.array([
        # positions        # texture coords
        -0.5,  0.5, 0.0,   0.0, 1.0,
        -0.5, -0.5, 0.0,   0.0, 0.0,
        0.5, -0.5, 0.0,   1.0, 0.0,
        0.5,  0.5, 0.0,   1.0, 1.0,
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        2, 3, 0
    ], dtype=np.uint32)


     # Generate and bind a Vertex Array Object (VAO)
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Generate and bind a Vertex Buffer Object (VBO)
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Generate and bind an Element Buffer Object (EBO)
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Define the position attribute in the vertex shader
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Define the texture coordinate attribute in the vertex shader
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)


    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


    return VAO, VBO, EBO
