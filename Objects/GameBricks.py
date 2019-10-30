from Objects.Game3DObjects import *

class OneHitBrick(Brick):
    def __init__(self, position, width, height, color):
        super().__init__(position, width, height, color)
        self.hitCount = 1
        self.currentHits = 0

    def update(self):
        if self.collided:
            self.currentHits += 1
            self.collided = False

    def display(self, model_matrix, shader, tex_id):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        super().display(model_matrix, shader)