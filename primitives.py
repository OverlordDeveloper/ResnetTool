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


    # Generate a buffer ID
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Texture coord attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)


    return VAO, VBO, EBO
