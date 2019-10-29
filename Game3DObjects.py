from Base3DObjects import *

class Brick(Cube):
    def __init__(self, position, width, height, color):
        super().__init__()
        self.pos = position
        self.w = width
        self.h = height
        self.l = 5
        self.color = color

    def display(self, model_matrix, shader):
        shader.set_mat_diffuse(self.color.x, self.color.y, self.color.z)
        model_matrix.push_matrix()
        model_matrix.add_translation(self.pos.x, self.pos.y, self.pos.z)
        model_matrix.add_scale(self.w, self.h, self.l)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader)
        model_matrix.pop_matrix()

class Ball(Sphere):
    def __init__(self, position, size, color=Point(1.0, 0.874, 0.0)):
        super().__init__(12, 24)
        self.pos = position
        self.size = size
        self.color = color
        self.shininess = 50.0

    def display(self, model_matrix, shader):
        shader.set_mat_diffuse(self.color.x, self.color.y, self.color.z)
        model_matrix.push_matrix()
        model_matrix.add_translation(self.pos.x, self.pos.y, self.pos.z)
        model_matrix.add_scale(self.size, self.size, self.size)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader)
        model_matrix.pop_matrix()

    def update(self, platform_motion, shooting, delta_time):
        if shooting and not self.shot:
            self.motion = Vector(platform_motion.x, 1) * self.speed # Find way to affect ball if shot of moving platform
            self.shot = True
        
        if self.shot:
            self.position += self.motion * delta_time