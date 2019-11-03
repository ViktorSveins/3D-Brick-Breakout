
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time
from random import randint

from Shaders import *
from Matrices import *
from Objects.GameBricks import *
from Objects.Base3DObjects import *
from texture_loading import *
from Objects.Environment import *
from BezierMotion import *

import ojb_3D_loading

level = 0

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.sprite_shader = SpriteShader()
        self.sprite_shader.use()

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0.0, 4.0, 30), Point(0.0, 11.0, 0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 4
        
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.LEFT_key_down = False
        self.RIGHT_key_down = False
        self.SPACE_key_down = False
        self.pause_game = False

        self.texture_id01 = load_texture("/crack1.png")
        self.texture_id02 = load_texture("/crack2.png")
        self.texture_id03 = load_texture("/crack3.png")
        self.textures = [self.texture_id01, self.texture_id02, self.texture_id03]
        self.texture_galaxy = load_texture("/skydome.jpeg")
        
        global level
        level += 1
        self.brickArray = []
        self.brickAnimation = []
        self.animationDir = 1
        self.remakeStage()

        self.ballArray = []

        self.skydome = Skysphere()
        self.platform = Platform(Point(0, 0, 0))
        self.frame = Frame(self.platform.pos, 25, 21)

        self.ball = Ball(Point(self.platform.pos.x, self.platform.pos.y + self.platform.h / 2 + 0.5, 0), 0.5)
        self.ballArray.append(self.ball)

        # self.obj_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models/obj/", "eyeball.obj")
        # self.obj_model = ojb_3D_loading.load_obj_file(sys.path[0] + "/models/", "metallic_sphere.obj")

        self.pauseTime = 0.0

        # check framerate, use for optimizing
        self.fr_ticker = 0.0
        self.fr_sum = 0.0

        # Start intro with bezier motion
        self.intro = Intro()
        self.bezierPositions = [Point(0.0, 4.0, 30), Point(50.0, 20.0, 50.0), Point(50.0, 20.0, -100.0), Point(-100.0, 20.0, -100.0),
                                Point(-100.0, 20.0, 50.0), Point(-50.0, 2.0, 50.0), Point(100.0, 2.0, 50.0), Point(100.0, 2.0, -60.0),
                                Point(-120.0, 2.0, -60.0), Point(-30.0, 2.0, 30.0), Point(50.0, 20.0, 50.0), Point(0.0, 4.0, 30)]
        self.introLook = Intro()
        self.bezierLookPosit = [Point(0.0, 11.0, 0), Point(0.0, 11.0, 0), Point(0.0, 11.0, 0), Point(0.0, 11.0, 0), Point(0.0, 11.0, 0),
                                Point(0.0, 0.0, 0), Point(0.0, 0.0, 0), Point(0.0, 0.0, 0), Point(0.0, 0.0, 0), Point(0.0, 0.0, 0),
                                Point(0.0, 11.0, 0), Point(0.0, 11.0, 0)]
        self.lightPos = self.view_matrix.eye

        # Restart level
        self.restartBezierBase = [Point(0.0, 4.0, 30.0), Point(5.0, 100.0, 30.0), Point(5.0, 100.0, -100.0),
                                Point(-5.0, -100.0, -100.0), Point(-5.0, -50.0, 100.0), Point(0.0, 4.0, 30.0)]
        self.restartlevel = Motion(10.0)
        self.restartBezierMovement = []
        self.restartPlatform = Motion(10.0)
        self.restartPlatformBase= Point(0.0, 0.0, 0.0)
        self.restartPlatformMovement= []
        self.setRestart = False
        self.stageDrawn = False

        self.win = False
        self.lost = False
        self.lives = 3

        # Spotlight
        self.lightMotion = Motion(10.0)
        self.lightMotionArray = [Point(100.0, -100.0, 75), Point(100.0, 100.0, 75), Point(-100.0, 100.0, 75), Point(-100.0, -100.0, 75), Point(100.0, -100.0, 75)]
        self.spotlightPos = Point(100.0, -100.0, 75)
        self.spotlightColor = Color(0.9, 0.1, 0.1)

        ### used for testing here
        self.sphere = Sphere(24, 48)
        self.sprite = Sprite()
        self.texture_leaf_color = load_texture("/test_leaf_01.jpg")
        self.texture_leaf_alpha = load_texture("/test_leaf_01_alpha.jpg")

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        if self.pause_game:
            return

        if not self.intro.animationFinished:
            self.view_matrix.look(self.intro.bezierMotionAnimation(delta_time, self.bezierPositions), self.introLook.bezierMotionAnimation(delta_time, self.bezierLookPosit), Vector(0, 1, 0))
            self.lightPos = self.view_matrix.eye
            return

        if self.win:
            if not self.restartlevel.animationFinished:
                if self.view_matrix.eye.z <= 0 and not self.stageDrawn:
                    self.brickArray = []
                    self.remakeStage()
                self.restartAnimation(delta_time)
                return
            else:
                self.win = False
                self.restartlevel.animationFinished = False
                self.restartlevel.animationTime = 0.0
                self.setRestart = False
                self.restartBezierMovement = []
                self.restartPlatformMovement= []
        
        if self.lost:
            if not self.restartlevel.animationFinished:
                if self.view_matrix.eye.z <= 0 and not self.stageDrawn:
                    self.brickArray = []
                    self.remakeStage()
                self.restartAnimation(delta_time)
                return
            else:
                self.lost = False
                self.restartlevel.animationFinished = False
                self.restartlevel.animationTime = 0.0
                self.setRestart = False
                self.restartBezierMovement = []
                self.restartPlatformMovement= []
        
        
        
        self.spotlightPos = self.lightMotion.bezierMotionAnimation(delta_time, self.lightMotionArray)
        if self.lightMotion.animationFinished:
            self.lightMotion.animationTime = 0
            self.lightMotion.animationFinished = False

        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0

        self.angle += pi * delta_time
        # #     angle -= (2 * pi)

        tmpAnimList = []
        for brick in self.brickAnimation:
            brick.updateAnimation(delta_time)
            if brick.animationTime <= 4:
                tmpAnimList.append(brick)
        self.brickAnimation = tmpAnimList
        
        for ball in self.ballArray:
            ball.update(self.platform.pos, delta_time)

        tmpList = []
        for brick in self.brickArray:
            for i in range(len(self.ballArray)):
                self.ballArray[i] = brick.collision(self.ballArray[i], delta_time)
                brick.update()
            if brick.destroy:
                self.animationDir *= -1
                brick.animationDirection = self.animationDir
                self.brickAnimation.append(brick)
            else:
                tmpList.append(brick)

        self.brickArray = tmpList

        for i in range(len(self.ballArray)):
            self.ballArray[i] = self.platform.collision(self.ballArray[i], delta_time)
            self.ballArray[i] = self.frame.collision(self.ballArray[i], delta_time)

        if self.LEFT_key_down:
            self.platform.slide(-5 * delta_time)
            self.view_matrix.arcFollow(self.platform.pos.x, 30, Point(0, 11, 0), 15)
        if self.RIGHT_key_down:
            self.platform.slide(5 * delta_time)
            self.view_matrix.arcFollow(self.platform.pos.x, 30, Point(0, 11, 0), 15)
        if self.SPACE_key_down:
            self.ball.shooting = True
            
        

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        glClear(GL_COLOR_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        glClearColor(1.0, 1.0, 1.0, 1.0)
        
        self.model_matrix.load_identity()

        #### Skydome
        glDisable(GL_DEPTH_TEST)
        self.sprite_shader.use()
        self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.sprite_shader.set_view_matrix(self.view_matrix.get_matrix())

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_galaxy)
        self.sprite_shader.set_dif_tex(0)
        self.sprite_shader.set_alpha_tex(None)

        self.sprite_shader.set_opacity(1.0)

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)

        self.sprite_shader.set_model_matrix(self.model_matrix.matrix)
        self.skydome.draw(self.sprite_shader)
        self.model_matrix.pop_matrix()

        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)
        ##### Skydome ends

        self.shader.use()

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_eye_position(self.view_matrix.eye)

        self.shader.set_view_matrix((self.view_matrix.get_matrix()))

        # Light
        # self.shader.set_light_position(Point(0.0, 20.0, 10.0))
        self.shader.set_light_position(self.lightPos)
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(1.0, 1.0, 1.0)

        # SpotLight
        self.shader.set_spotlight_position(self.spotlightPos)
        self.shader.set_spotlight_diffuse(self.spotlightColor)
        self.shader.set_spotlight_specular(self.spotlightColor)


        self.shader.set_material_specular(Color(1.0, 1.0, 1.0))
        self.shader.set_material_shininess(5.0)
        
        self.frame.display(self.model_matrix, self.shader)
        self.platform.display(self.model_matrix, self.shader)
        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(0.014, 0, 0)
        # self.model_matrix.add_rotate_x(-pi/2)
        # self.model_matrix.add_scale(0.00345, 0.00345, 0.00345)
        # self.shader.set_model_matrix(self.model_matrix.matrix)
        # self.obj_model.draw(self.shader)
        # self.model_matrix.pop_matrix()

        # self.brickArray[0].set_vertices(self.shader)

        # self.brick.display(self.model_matrix, self.shader)


        self.shader.set_using_tex(1.0)        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id01)
        self.shader.set_dif_tex(0)
        for ball in self.ballArray:
            ball.display(self.model_matrix, self.shader)
        self.shader.set_using_tex(0.0)

        for brick in self.brickArray:
            brick.display(self.model_matrix, self.shader)

        for brick in self.brickAnimation:
            brick.display(self.model_matrix, self.shader)

        ####################
        # for i in range(8):
        #     self.model_matrix.push_matrix()
        #     self.model_matrix.add_rotate_x(self.angle * 0.74324 + i * pi / 4.0)
        #     self.model_matrix.add_translation(0.0, 5.0, 10.0)
        #     self.model_matrix.add_rotate_x(-(self.angle * 0.74324 + i * pi / 4.0))
        #     self.model_matrix.add_scale(3.0, 3.0, 3.0)
        #     self.shader.set_model_matrix(self.model_matrix.matrix)

        #     self.shader.set_material_diffuse(Color(1.0, 1.0, 1.0))
        #     self.sphere.draw(self.shader)
        #     self.model_matrix.pop_matrix()
        ####################

        ##### Adding to sprite shader how to draw with alpha image #####
        # glEnable(GL_BLEND)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        # self.sprite_shader.use()
        # self.sprite_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        # self.sprite_shader.set_view_matrix((self.view_matrix.get_matrix()))

        # glActiveTexture(GL_TEXTURE0)
        # glBindTexture(GL_TEXTURE_2D, self.texture_leaf_color)
        # self.sprite_shader.set_dif_tex(0)
        # glActiveTexture(GL_TEXTURE1)
        # glBindTexture(GL_TEXTURE_2D, self.texture_leaf_alpha)
        # self.sprite_shader.set_alpha_tex(1)

        # self.sprite_shader.set_opacity(0.8)

        # self.model_matrix.push_matrix()
        # self.model_matrix.add_translation(3.0, 6.0, 0.0)
        # self.model_matrix.add_scale(8.0, 8.0, 1.0)
        # self.sprite_shader.set_model_matrix(self.model_matrix.matrix)
        # self.sprite.draw(self.sprite_shader)
        # self.model_matrix.pop_matrix()

        # glDisable(GL_BLEND)

        pygame.display.flip()

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                        
                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True
                    if event.key == K_SPACE:
                        self.SPACE_key_down = True
                    if event.key == K_p:
                        self.pause_game = not self.pause_game
                    if event.key == K_u:
                        self.win = not self.win
                        self.stageDrawn = False #TODO move this
                        
                elif event.type == pygame.KEYUP:
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
                    if event.key == K_SPACE:
                        self.SPACE_key_down = False

            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def restartAnimation(self, delta_time):
        if not self.setRestart:
            self.restartBezierMovement.append(self.view_matrix.eye)
            for point in self.restartBezierBase:
                self.restartBezierMovement.append(point)

            self.restartPlatformMovement.append(self.platform.pos)
            self.restartPlatformMovement.append(self.restartPlatformBase)

            self.setRestart = True

        self.view_matrix.look(self.restartlevel.bezierMotionAnimation(delta_time, self.restartBezierMovement), Point(0.0, 11.0, 0), Vector(0, 1, 0))
        self.platform.pos = self.restartPlatform.bezierMotionAnimation(delta_time, self.restartPlatformMovement)

    def remakeStage(self):
        y_coord = 20
        for _ in range(level):
            for i in range(4):
                brick = ThreeHitBrick(Point((i * 3) + 1.5, y_coord, 0), 2.5, 0.5, self.textures)
                self.brickArray.append(brick)
            y_coord -= 0.75
        y_coord -= 1.0

        for _ in range(level):       
            for i in range(4):
                brick = TwoHitBrick(Point((i * 3) + 1.5, y_coord, 0), 2.5, 0.5, self.textures)
                self.brickArray.append(brick)
            y_coord -= 0.75
        y_coord -= 1.0
        
        for _ in range (level):
            for i in range(4):
                brick = OneHitBrick(Point((i * 3) + 1.5, y_coord, 0), 2.5, 0.5, self.textures)
                self.brickArray.append(brick)
            y_coord -= 0.75
        y_coord -= 1.0

        y_coord = 20
        for _ in range(level):
            for i in range(4):
                brick = ThreeHitBrick(Point((-i * 3) - 1.5, y_coord, 0), 2.5, 0.5, self.textures)
                self.brickArray.append(brick)
            y_coord -= 0.75
        y_coord -= 1.0

        for _ in range(level):       
            for i in range(4):
                brick = TwoHitBrick(Point((-i * 3) - 1.5, y_coord, 0), 2.5, 0.5, self.textures)
                self.brickArray.append(brick)
            y_coord -= 0.75
        y_coord -= 1.0
        
        for _ in range (level):
            for i in range(4):
                brick = OneHitBrick(Point((-i * 3) - 1.5, y_coord, 0), 2.5, 0.5, self.textures)
                self.brickArray.append(brick)
            y_coord -= 0.75

        self.stageDrawn = True

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()