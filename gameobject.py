from pyrr import Vector3, Matrix44, Quaternion

from OpenGL.GL import *
import numpy as np


class Quad:
    def __init__(self, buffer_objects, texture):
        self.vao, self.vbo, self.ebo  = buffer_objects

        self.model = Matrix44.identity()
        self.viewMatrix = Matrix44.identity()

        self.SetPosition(Vector3((0, 0, 0)))
        self.SetRotation(Vector3((0, 0, 0)))
        self.SetScale(Vector3((1, 1, 1)))


        self.texture = texture

    def load_program(self, program):

        self.program = program

        self.model_loc = glGetUniformLocation(self.program, "model")
        self.view_loc = glGetUniformLocation(self.program, "view")
        self.projection_loc = glGetUniformLocation(self.program, "projection")
        self.modelView_loc = glGetUniformLocation(self.program, "modelView")

    def _update_modelview_matrix(self):

        modelMatrix = self.translationMatrix @ self.rotationMatrix @ self.scaleMatrix

        modelViewMatrix =  modelMatrix @ self.viewMatrix 

        modelViewMatrix[:3, :3] = np.identity(3)

        self.modelView = modelViewMatrix
    def Update(self, view, projection):
        self.viewMatrix = view
        self.projection = projection

        self._update_modelview_matrix()
        
    def Render(self):

        glUseProgram(self.program)

        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection)
        glUniformMatrix4fv(self.modelView_loc, 1, GL_FALSE, self.modelView)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    def SetPosition(self, pos):
        self.position = pos
        self.translationMatrix = Matrix44.from_translation(self.position)

    def SetRotation(self, rot):
        self.rotation = rot

        rotation_x_matrix = Matrix44.from_x_rotation(self.rotation.x)
        rotation_y_matrix = Matrix44.from_y_rotation(self.rotation.y)
        rotation_z_matrix = Matrix44.from_z_rotation(self.rotation.z)
        
        self.rotationMatrix = rotation_z_matrix @ rotation_y_matrix @ rotation_x_matrix

    def SetScale(self, scale):
        self.scale = scale
        self.scaleMatrix = Matrix44.from_scale(self.scale)
        

    def _update_model_matrix(self):
        # Translation matrix
        translation_matrix = Matrix44.from_translation(self.position)

        # Rotation matrices
        rotation_x_matrix = Matrix44.from_x_rotation(self.rotation.x)
        rotation_y_matrix = Matrix44.from_y_rotation(self.rotation.y)
        rotation_z_matrix = Matrix44.from_z_rotation(self.rotation.z)
        rotation_matrix = rotation_z_matrix @ rotation_y_matrix @ rotation_x_matrix

        # Scale matrix
        scale_matrix = Matrix44.from_scale(self.scale)

        # Combine all transformations: translation * rotation * scale
        self.model = translation_matrix @ rotation_matrix @ scale_matrix