from Objects.Base3DObjects import *
from ojb_3D_loading import *
import random 

class Brick(Cube):
    def __init__(self, position, width, height, color):
        super().__init__()
        self.pos = position
        self.w = width
        self.h = height
        self.l = 1
        self.color = color
        self.collided = False

        self.corner_1 = Point(self.pos.x - self.w / 2, self.pos.y - self.h /2, 0)
        self.corner_2 = Point(self.pos.x - self.w / 2, self.pos.y + self.h /2, 0)
        self.corner_3 = Point(self.pos.x + self.w / 2, self.pos.y + self.h /2, 0)
        self.corner_4 = Point(self.pos.x + self.w / 2, self.pos.y - self.h /2, 0)

        self.sides = []
        self.sides.append(LineObstacle(self.corner_1, self.corner_2))
        self.sides.append(LineObstacle(self.corner_2, self.corner_3))
        self.sides.append(LineObstacle(self.corner_4, self.corner_3))
        self.sides.append(LineObstacle(self.corner_1, self.corner_4))

    def display(self, model_matrix, shader):
        shader.set_material_diffuse(self.color)
        model_matrix.push_matrix()
        model_matrix.add_translation(self.pos.x, self.pos.y, self.pos.z)
        model_matrix.add_scale(self.w, self.h, self.l)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader)
        model_matrix.pop_matrix()
        
    def collision(self, ball, delta_time):
        # Optimize to only check the sides facing the ball
        sidesToCheck = []
        if ball.pos.x < self.pos.x:
            sidesToCheck.append(self.sides[0])
        else:
            sidesToCheck.append(self.sides[2])

        if ball.pos.y < self.pos.y:
            sidesToCheck.append(self.sides[3])
        else:
            sidesToCheck.append(self.sides[1])

        # Check which of the two sides is closer to the ball
        # This is the case of a corner, so that the ball ricochets of the correct side
        distX = abs(sidesToCheck[0].point_1.x - ball.pos.x)
        distY = abs(sidesToCheck[1].point_1.y - ball.pos.y)
        
        # Reverse the array if other side is closer
        if distY > distX:
            sidesToCheck.reverse()
        
        # Check the sides in the order defined above
        for side in sidesToCheck:
            ball = side.collision(ball, delta_time)
            if ball.collided:
                self.collided = True
                ball.collided = False
                return ball
        return ball
        

class Ball(Sphere):
    def __init__(self, position, size, color=Color(1.0, 0.874, 0.0)):
        super().__init__(12, 24)
        self.pos = position
        self.size = size
        self.color = color
        self.shininess = 50.0
        self.radius = (self.size + 0.5) / 2
        self.shooting = False
        self.shot = False
        self.motion = Vector(0,0,0)
        self.collided = False
        self.speed = 10

    def display(self, model_matrix, shader):
        shader.set_material_diffuse(self.color)
        model_matrix.push_matrix()
        model_matrix.add_translation(self.pos.x, self.pos.y, self.pos.z)
        model_matrix.add_scale(self.size, self.size, self.size)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader)
        model_matrix.pop_matrix()

    def update(self, platform_position, delta_time):
        if self.shot:
            self.pos += self.motion * delta_time
        else:
            self.pos.x = platform_position.x
            if self.shooting:
                self.motion = Vector(random.uniform(-0.3, 0.3), 0.9, 0) * self.speed
                self.shot = True
                self.shooting = False

        
class LineObstacle(Line):
    def __init__(self, point_1, point_2):
        Line.__init__(self, point_1, point_2)
        self.normal_vector = Vector(-(self.point_2.y - self.point_1.y), self.point_2.x - self.point_1.x, 0)

    def pointInsideCircle(self, ball, point):
        distX = ball.pos.x - point.x
        distY = ball.pos.y - point.y
    
        length = sqrt(distX**2 + distY**2 )

        return length < ball.radius

    def pointInLineRange(self, point):
        if self.point_1.x < self.point_2.x:
                x_min, x_max = self.point_1.x, self.point_2.x
        else:
            x_min, x_max = self.point_2.x, self.point_1.x

        if self.point_1.y < self.point_2.y:
            y_min, y_max = self.point_1.y, self.point_2.y
        else:
            y_min, y_max = self.point_2.y, self.point_1.y

        return point.x >= x_min and point.x <= x_max and point.y >= y_min and point.y <= y_max

    def redirectBall(self, ball, point, corner = False):
        ball.collided = True
        vectorToPoint = point - ball.pos
        vecLength = vectorToPoint.length()
        vectorToPoint.normalize()
        ball.pos = ball.pos - vectorToPoint * (ball.radius - vecLength)
        if corner:
            ball.motion = self.reflectionFromCorner(ball, point)
        else:
            ball.motion = self.reflection(ball.motion)
            
        return ball

    def reflectionFromCorner(self, ball, point):
        vectorFromCorner = ball.pos - point
        vectorFromCorner.normalize()
        return vectorFromCorner * ball.speed
    

    def collision(self, ball, delta_time):
        distX = self.point_1.x - self.point_2.x
        distY = self.point_1.y - self.point_2.y

        length = sqrt(distX**2 + distY**2)
        
        dotproduct = ( ((ball.pos.x - self.point_1.x) * (self.point_2.x - self.point_1.x))
                     + ((ball.pos.y - self.point_1.y) * (self.point_2.y - self.point_1.y)) ) / length**2
        
        # Closest point on line from the balls' center
        closestPointOnLine = Point(self.point_1.x + dotproduct * (self.point_2.x - self.point_1.x), 
                                   self.point_1.y + dotproduct * (self.point_2.y - self.point_1.y), 0)

        # Check whether either end of line is inside the ball (check the corners)
        if self.pointInsideCircle(ball, self.point_1):
            return self.redirectBall(ball, self.point_1, True)
        elif self.pointInsideCircle(ball, self.point_2):
            return self.redirectBall(ball, self.point_2, True)
        
        # Check if the closest point on the line is already inside the ball
        if self.pointInsideCircle(ball, closestPointOnLine) and self.pointInLineRange(closestPointOnLine):
            return self.redirectBall(ball, closestPointOnLine)

        # Find the vector from the balls' center to the closest point on the line
        vector = Vector(ball.pos.x - closestPointOnLine.x, ball.pos.y - closestPointOnLine.y, 0)

        # If the points are the same we don't want to normalize
        if vector.length() == 0:
            closestPointOnCircle = closestPointOnLine
            traversal = Vector(0, 0, 0)
        else:
            vector.normalize()
            # Traversal is the vector that the ball's center must be moved along to push the ball back out of the line
            traversal = vector * ball.radius
            closestPointOnCircle = Point(ball.pos.x - traversal.x, ball.pos.y - traversal.y, 0)
       
        # Check whether the dotproduct is 0 to avoid division by zero
        normalDot = self.normal_vector.dot(ball.motion)
        if(normalDot == 0):
            t_hit = 0
        else:    
            t_hit = self.normal_vector.dot(self.point_2 - closestPointOnCircle) / normalDot

        # Check whether the hit is in this frame
        if t_hit > 0 and t_hit <= delta_time:
            # Point of hit
            p_hit = closestPointOnCircle + ball.motion * t_hit
            # Check if the point of hit is on the line (not just the equation of the line)
            if self.pointInLineRange(p_hit):
                # Mark that the ball collided
                ball.collided = True
                # Push ball out of line
                ball.pos = p_hit + traversal
                # Change it's motion vector
                ball.motion = self.reflection(ball.motion)
        return ball
    
    def reflection(self, c_motion):
        return c_motion - self.normal_vector * (c_motion.dot(self.normal_vector) / (self.normal_vector.dot(self.normal_vector))) * 2

class Platform:
    def __init__(self, position):
        self.container = load_obj_file(sys.path[0] + "/models/container/", "Container.obj")

        self.pos = position
        self.w = 4
        self.h = 3.26
        
        self.corner_1 = Point(self.pos.x - self.w / 2, self.pos.y - self.h /2, 0)
        self.corner_2 = Point(self.pos.x - self.w / 2, self.pos.y + self.h /2, 0)
        self.corner_3 = Point(self.pos.x + self.w / 2, self.pos.y + self.h /2, 0)
        self.corner_4 = Point(self.pos.x + self.w / 2, self.pos.y - self.h /2, 0)

        self.sides = []
        self.sides.append(LineObstacle(self.corner_1, self.corner_2))
        self.sides.append(LineObstacle(self.corner_2, self.corner_3))
        self.sides.append(LineObstacle(self.corner_4, self.corner_3))
        
    
    def display(self, model_matrix, shader):
        model_matrix.push_matrix()
        model_matrix.add_translation(self.pos.x + 0.02, self.pos.y, 0)
        model_matrix.add_rotate_x(-pi/2)
        model_matrix.add_scale(0.00563, 0.00563, 0.00563)
        shader.set_model_matrix(model_matrix.matrix)
        self.container.draw(shader)
        model_matrix.pop_matrix()

    def slide(self, x):
        self.pos.x += x
        
        self.corner_1 = Point(self.pos.x - self.w / 2, self.pos.y - self.h /2, 0)
        self.corner_2 = Point(self.pos.x - self.w / 2, self.pos.y + self.h /2, 0)
        self.corner_3 = Point(self.pos.x + self.w / 2, self.pos.y + self.h /2, 0)
        self.corner_4 = Point(self.pos.x + self.w / 2, self.pos.y - self.h /2, 0)

        self.sides[0] = LineObstacle(self.corner_1, self.corner_2)
        self.sides[1] = LineObstacle(self.corner_2, self.corner_3)
        self.sides[2] = LineObstacle(self.corner_4, self.corner_3)

    def collision(self, ball, delta_time):
        for side in self.sides:
            ball = side.collision(ball, delta_time)
            if ball.collided:
                self.collided = True
                ball.collided = False
                return ball
        return ball


class Wall(Cube):
    def __init__(self, position, width, height, color):
        super().__init__()
        self.pos = position
        self.w = width
        self.h = height
        self.l = 1
        self.color = color
    
    def display(self, model_matrix, shader):
        shader.set_material_diffuse(self.color)
        model_matrix.push_matrix()
        model_matrix.add_translation(self.pos.x, self.pos.y, self.pos.z)
        model_matrix.add_scale(self.w, self.h, self.l)
        shader.set_model_matrix(model_matrix.matrix)
        self.draw(shader)
        model_matrix.pop_matrix()
    

class Frame:
    def __init__(self, platform_position, width, height):
        self.corner_1 = Point(platform_position.x - width / 2, platform_position.y, 0)
        self.corner_2 = Point(platform_position.x - width / 2, platform_position.y + height, 0)
        self.corner_3 = Point(platform_position.x + width / 2, platform_position.y + height, 0)
        self.corner_4 = Point(platform_position.x + width / 2, platform_position.y, 0)

        self.sides = []
        self.sides.append(LineObstacle(self.corner_1, self.corner_2))
        self.sides.append(LineObstacle(self.corner_2, self.corner_3))
        self.sides.append(LineObstacle(self.corner_4, self.corner_3))

        self.walls = []
        wallwidth = 0.5
        wallcolor = Color(1.0, 0.84, 0.0)
        self.walls.append(Wall(Point(self.corner_1.x - wallwidth / 2, platform_position.y + height / 2, 0), wallwidth, height, wallcolor))
        self.walls.append(Wall(Point(self.corner_3.x + wallwidth / 2, platform_position.y + height / 2, 0), wallwidth, height, wallcolor))
        self.walls.append(Wall(Point(platform_position.x, self.corner_2.y + wallwidth / 2, 0), width + wallwidth * 2, wallwidth, wallcolor))

    def collision(self, ball, delta_time):
        for side in self.sides:
            ball = side.collision(ball, delta_time)
            if ball.collided:
                self.collided = True
                ball.collided = False
                return ball
        return ball
    
    def display(self, model_matrix, shader):
        for wall in self.walls:
            wall.display(model_matrix, shader)
        