from Objects.Game3DObjects import *


class HitBrick(Brick):
    def __init__(self, position, width, height, textures, color, maxHit):
        super().__init__(position, width, height, color)
        self.maxHit = maxHit
        self.currentHits = 0
        self.textures = textures
        self.destroy = False
        self.animationStart = 0
        self.animationTime = 0
        self.animationDirection = 0

    def update(self):
        if self.collided:
            self.collided = False
            self.currentHits += 1
            if self.currentHits >= self.maxHit:
                self.destroy = True

    def updateAnimation(self, delta_time):
        self.animationTime += delta_time
        self.pos.z += 50.0 * self.animationDirection * delta_time

    def display(self, model_matrix, shader):
        if self.currentHits != 0:
            if self.currentHits > 3:
                index = 2
            else:
                index = self.currentHits - 1
            shader.set_using_tex(1.0)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.textures[index])
            shader.set_dif_tex(0)

        super().display(model_matrix, shader)
        shader.set_using_tex(0.0)

class OneHitBrick(HitBrick):
    def __init__(self, position, width, height, textures):
        super().__init__(position, width, height, textures, Color(0.15, 0.85, 0.10), 2)
        
class TwoHitBrick(HitBrick):
    def __init__(self, position, width, height, textures):
        super().__init__(position, width, height, textures, Color(0.80, 0.80, 0.10), 3)

class ThreeHitBrick(HitBrick):
    def __init__(self, position, width, height, textures):
        super().__init__(position, width, height, textures, Color(0.85, 0.15, 0.10), 4)
