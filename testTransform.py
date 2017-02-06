

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as glShaders
import numpy as np
import math
import shaderUtils
from PIL import Image
import ctypes
from pyrr import Matrix44

def main():

    if not glfw.init():
        print 'Could not initialize glfw'
        return
    
    glfw.window_hint( glfw.CONTEXT_VERSION_MAJOR, 3 )
    glfw.window_hint( glfw.CONTEXT_VERSION_MINOR, 3 )
    glfw.window_hint( glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE );

    window = glfw.create_window( 800, 600, "Test", None, None )

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current( window )
    
    #                      |    position  |     colors   |   texture coords |
    quadData = np.array( [ -0.5, -0.5, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0,
                            0.5, -0.5, 0.4, 0.0, 1.0, 0.0, 0.5, 0.0,
                            0.5,  0.5, 0.3, 0.0, 0.0, 1.0, 0.5, 1.0,
                           -0.5,  0.5, 0.9, 1.0, 1.0, 1.0, 0.0, 1.0 ], dtype = np.float32 )

    quadIndices = np.array( [ 0, 1, 2 ,
                              2, 3, 0 ], dtype = np.uint32 )
    
    shaderProgram = shaderUtils.Program( 'basicVertexShader.glsl',
                                         'basicFragmentShader.glsl' )

    # create a Vertex Buffer Object to store the vertices
    VBO = glGenBuffers( 1 )
    # create an element buffer object to store the indices to be used when drawing the quad
    EBO = glGenBuffers( 1 )
    # create a Vertex Array Object to store the configuration
    VAO = glGenVertexArrays( 1 )
    # set ths va0 as the current vao
    glBindVertexArray( VAO )
    
    # bind the vbo, which sets it as the current bound vbo
    glBindBuffer( GL_ARRAY_BUFFER, VBO )
    glBufferData( GL_ARRAY_BUFFER, quadData.itemsize * len( quadData ), quadData, GL_STATIC_DRAW )

    glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, EBO )
    glBufferData( GL_ELEMENT_ARRAY_BUFFER, quadIndices.itemsize * len( quadIndices ), quadIndices, GL_STATIC_DRAW )

    # related to the currently bound vbo, link the vertex data
    # vertices
    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p( 0 ) ) 
    glEnableVertexAttribArray( 0 )
    # color
    glVertexAttribPointer( 1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p( 12 ) ) 
    glEnableVertexAttribArray( 1 )
    # texture
    glVertexAttribPointer( 2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p( 24 ) ) 
    glEnableVertexAttribArray( 2 )

    glBindVertexArray( 0 )

    # use our texture
    texture = glGenTextures( 1 )
    glBindTexture( GL_TEXTURE_2D, texture )

    # set texture parameters
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )

    image = Image.open( 'res/container.jpg' )
    img_data = np.array( list( image.getdata() ), np.uint8 )
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data )

    #glBindTexture( GL_TEXTURE_2D, 0 )

    while not glfw.window_should_close( window ):
         
        glClearColor( 0.2, 0.3, 0.2, 1.0 )
        glClear( GL_COLOR_BUFFER_BIT )

        shaderProgram.use()

        timeVal = glfw.get_time()

        u_transform = glGetUniformLocation( shaderProgram.id, 'u_transform' )
        mat_translation = Matrix44( [  1.0,   0.0,  0.0,  0.0,
                                       0.0,   1.0,  0.0,  0.0,
                                       0.0,   0.0,  1.0,  0.0,
                                       0.5,  -0.5,  0.0,  1.0 ], dtype = np.float32 )
        theta = timeVal
        mat_rotation = Matrix44( [  math.cos( theta ),  math.sin( theta ),  0.0 , 0.0,
                                   -math.sin( theta ),  math.cos( theta ),  0.0 , 0.0,
                                         0.0        ,         0.0        ,  1.0 , 0.0,
                                         0.0        ,         0.0        ,  0.0 , 1.0 ], dtype = np.float32 )
        scale = 0.75 + 0.25 * math.sin( 2.0 * timeVal )
        mat_scaling = Matrix44( [ scale ,   0.0  ,  0.0  , 0.0,
                                   0.0  ,  scale ,  0.0  , 0.0,
                                   0.0  ,   0.0  , scale , 0.0,
                                   0.0  ,   0.0  ,  0.0  , 1.0 ], dtype = np.float32 )

        mat_transform = mat_scaling * mat_rotation * mat_translation
        #mat_transform = mat_translation * mat_rotation
        glUniformMatrix4fv( u_transform, 1, GL_FALSE, mat_transform )

        glBindVertexArray( VAO )
        glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_INT, None )        

        glUniformMatrix4fv( u_transform, 1, GL_FALSE, mat_scaling )
        glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_INT, None )        
        glBindVertexArray( 0 )

        shaderProgram.release()

        glfw.poll_events()
        glfw.swap_buffers( window )

    glfw.terminate()


if __name__ == '__main__':
    main() 

