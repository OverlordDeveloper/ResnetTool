from pyrr import Vector3, Matrix44, Quaternion

class Quad:
    def __init__(self, buffer_objects, texture):
        self.vao, self.vbo, self.ebo  = buffer_objects

        self.model = Matrix44.identity()

        self.position = Vector3((0, 0, 0))
        self.rotation = Vector3((0, 0, 0))
        self.scale = Vector3((1, 1, 1))

        self.texture = texture


    def SetPosition(self, pos):
        self.position = pos
        self.translation_matrix = Matrix44.from_translation(self.position)

        self.model = self.translation_matrix

    def SetRotation(self, rot):
        pass

    def SetScale(self, scale):
        pass
