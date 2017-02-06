



import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as glShaders
import numpy as np
import math
import shaderUtils
from PIL import Image
import ctypes
import pyrr
import mat3d

window = None

def initGLFW():
    global window

    if not glfw.init():
        print 'Could not initialize glfw'
        return
    
    glfw.window_hint( glfw.CONTEXT_VERSION_MAJOR, 3 )
    glfw.window_hint( glfw.CONTEXT_VERSION_MINOR, 3 )
    glfw.window_hint( glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE );

    window = glfw.create_window( 800, 600, "Test MPV transformation", None, None )

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current( window )


def main():
    
    initGLFW()

##    #                      |    position  |     colors   |   texture coords |
##    vertices = np.array( [ -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
##                            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 0.5, 0.0,
##                            0.5,  0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 1.0,
##                           -0.5,  0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0 ], dtype = np.float32 )

    #                       |    position   | texture coords |
    vertices = np.array( [  -0.5, -0.5, -0.5,  0.0, 0.0,
                             0.5, -0.5, -0.5,  1.0, 0.0,
                             0.5,  0.5, -0.5,  1.0, 1.0,
                             0.5,  0.5, -0.5,  1.0, 1.0,
                            -0.5,  0.5, -0.5,  0.0, 1.0,
                            -0.5, -0.5, -0.5,  0.0, 0.0,

                            -0.5, -0.5,  0.5,  0.0, 0.0,
                             0.5, -0.5,  0.5,  1.0, 0.0,
                             0.5,  0.5,  0.5,  1.0, 1.0,
                             0.5,  0.5,  0.5,  1.0, 1.0,
                            -0.5,  0.5,  0.5,  0.0, 1.0,
                            -0.5, -0.5,  0.5,  0.0, 0.0,

                            -0.5,  0.5,  0.5,  1.0, 0.0,
                            -0.5,  0.5, -0.5,  1.0, 1.0,
                            -0.5, -0.5, -0.5,  0.0, 1.0,
                            -0.5, -0.5, -0.5,  0.0, 1.0,
                            -0.5, -0.5,  0.5,  0.0, 0.0,
                            -0.5,  0.5,  0.5,  1.0, 0.0,

                             0.5,  0.5,  0.5,  1.0, 0.0,
                             0.5,  0.5, -0.5,  1.0, 1.0,
                             0.5, -0.5, -0.5,  0.0, 1.0,
                             0.5, -0.5, -0.5,  0.0, 1.0,
                             0.5, -0.5,  0.5,  0.0, 0.0,
                             0.5,  0.5,  0.5,  1.0, 0.0,

                            -0.5, -0.5, -0.5,  0.0, 1.0,
                             0.5, -0.5, -0.5,  1.0, 1.0,
                             0.5, -0.5,  0.5,  1.0, 0.0,
                             0.5, -0.5,  0.5,  1.0, 0.0,
                            -0.5, -0.5,  0.5,  0.0, 0.0,
                            -0.5, -0.5, -0.5,  0.0, 1.0,

                            -0.5,  0.5, -0.5,  0.0, 1.0,
                             0.5,  0.5, -0.5,  1.0, 1.0,
                             0.5,  0.5,  0.5,  1.0, 0.0,
                             0.5,  0.5,  0.5,  1.0, 0.0,
                            -0.5,  0.5,  0.5,  0.0, 0.0,
                            -0.5,  0.5, -0.5,  0.0, 1.0 ], dtype = np.float32 )
    
    glEnable( GL_DEPTH_TEST )

    shaderProgram = shaderUtils.Program( 'shaders/basicVertexShaderMPV.glsl',
                                         'shaders/basicFragmentShaderMPV.glsl' )

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
    glBufferData( GL_ARRAY_BUFFER, vertices.itemsize * len( vertices ), vertices, GL_STATIC_DRAW )

    # related to the currently bound vbo, link the vertex data
    # vertices
    glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p( 0 ) ) 
    glEnableVertexAttribArray( 0 )
    # texture
    glVertexAttribPointer( 1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p( 12 ) ) 
    glEnableVertexAttribArray( 1 )

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
        glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        shaderProgram.use()

        u_matModel = glGetUniformLocation( shaderProgram.id, 'u_matModel' )
        mat_model = mat3d.rotx( 50 * math.sin( glfw.get_time() ) )
        mat_model = mat_model * mat3d.roty( 50 * math.cos( glfw.get_time() ) )
        glUniformMatrix4fv( u_matModel, 1, GL_FALSE, mat_model )
        
        u_matView = glGetUniformLocation( shaderProgram.id, 'u_matView' )
        mat_view = pyrr.matrix44.create_from_translation( np.array( [ 0.0, 0.0, -5.0 ] , dtype=np.float32 ) )
        glUniformMatrix4fv( u_matView, 1, GL_FALSE, mat_view )

        u_matProjection = glGetUniformLocation( shaderProgram.id, 'u_matProjection' )
        mat_projection = mat3d.makePerspectiveMatrix( 45., 800. / 600, 0.1, 100.0 )
        glUniformMatrix4fv( u_matProjection, 1, GL_FALSE, mat_projection )

        glBindVertexArray( VAO )
        glDrawArrays( GL_TRIANGLES, 0, 36 ) 

        shaderProgram.release()

        glfw.poll_events()
        glfw.swap_buffers( window )

    glfw.terminate()


if __name__ == '__main__':
    main() 

