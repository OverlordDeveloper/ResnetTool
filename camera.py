from pyrr import Vector3, matrix44, vector
import numpy as np
import pyrr


class Camera:
    def __init__(self, position=Vector3([0.0, 0.0, 3.0]), up=Vector3([0.0, 1.0, 0.0]), yaw=-90.0, pitch=0.0, speed=2.5, sensitivity=0.1, zoom=45.0):
        self.position = position
        self.up = up
        self.front = Vector3([0.0, 0.0, -1.0])
        self.right = Vector3()
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch
        self.speed = speed
        self.sensitivity = sensitivity
        self.zoom = zoom
        self.update_camera_vectors()

    def update_camera_vectors(self):
        # Calculate the new front vector
        front = Vector3()
        front.x = np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        front.y = np.sin(np.radians(self.pitch))
        front.z = np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))

        self.front = vector.normalize(front)

        # Also re-calculate the right and up vector

        self.right = vector.normalize(pyrr.vector3.cross(self.front, self.world_up))
        self.up = vector.normalize(pyrr.vector3.cross(self.right, self.front))

    def get_view_matrix(self):
        return matrix44.create_look_at(self.position, self.position + self.front, self.up)

    def process_keyboard(self, direction, delta_time):
        velocity = self.speed * delta_time
        if direction == 'FORWARD':
            self.position += self.front * velocity
        if direction == 'BACKWARD':
            self.position -= self.front * velocity
        if direction == 'LEFT':
            self.position -= self.right * velocity
        if direction == 'RIGHT':
            self.position += self.right * velocity


    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def process_mouse_scroll(self, yoffset):
        if self.zoom >= 1.0 and self.zoom <= 45.0:
            self.zoom -= yoffset
        if self.zoom <= 1.0:
            self.zoom = 1.0
        if self.zoom >= 45.0:
            self.zoom = 45.0
