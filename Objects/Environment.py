from Objects.Base3DObjects import *

# No need for inheritence here since every functions needs to be changed anyway
class Skysphere:
    def __init__(self, stacks = 128, slices = 256):
        vertex_array = []
        self.slices = slices
        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval

                vertex_array.append(sin(stack_angle) * cos(slice_angle))
                vertex_array.append(cos(stack_angle))
                vertex_array.append(sin(stack_angle) * sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append(stack_count / stacks)

                vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                vertex_array.append(cos(stack_angle + stack_interval))
                vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append((stack_count + 1) / stacks)

                self.vertex_count += 2
        
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        vertex_array = None

    def draw(self, sprite_shader):
        sprite_shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


class Sprite:
    def __init__(self):
        vertex_array = [-0.5, -0.5, 0.0, 0.0, 0.0,
                                -0.5, 0.5, 0.0, 0.0, 1.0,
                                0.5, 0.5, 0.0, 1.0, 1.0,
                                0.5, -0.5, 0.0, 1.0, 0.0,]
        
        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        vertex_array = None

    def draw(self, sprite_shader):
        sprite_shader.set_attribute_buffers_with_uv(self.vertex_buffer_id)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
