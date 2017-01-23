

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as glShaders
import numpy as np
import math
import shaderUtils

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
    
    vertices = np.array( [  0.0,  0.5, 0.0,
                            0.5, -0.5, 0.0,
                           -0.5, -0.5, 0.0 ], dtype = np.float32 )

    
    shaderProgram = shaderUtils.Program( 'basicVertexShader.glsl',
                                         'basicFragmentShader.glsl' )

    # create a Vertex Buffer Object to store the vertices
    VBO = glGenBuffers( 1 )
    # create a Vertex Array Object to store the configuration
    VAO = glGenVertexArrays( 1 )
    # set ths va0 as the current vao
    glBindVertexArray( VAO )
    
    # bind the vbo, which sets it as the current bound vbo
    glBindBuffer( GL_ARRAY_BUFFER, VBO )
    glBufferData( GL_ARRAY_BUFFER, 4 * len( vertices ), vertices, GL_STATIC_DRAW )

    # get the position attribute so that we link the vertices to this vertex attribute
    position = glGetAttribLocation( shaderProgram.id, 'position' )
    # related to the currently bound vbo, link the vertex data
    glVertexAttribPointer( position, 3, GL_FLOAT, GL_FALSE, 0, None ) 
    glEnableVertexAttribArray( position )

    glBindVertexArray( 0 )



    while not glfw.window_should_close( window ):
         
        glClearColor( 0.2, 0.3, 0.2, 1.0 )
        glClear( GL_COLOR_BUFFER_BIT )

        shaderProgram.use()

        timeVal = glfw.get_time()
        greenValue = 0.5 * math.sin( timeVal ) + 0.5
        u_color = glGetUniformLocation( shaderProgram.id, 'u_color' )
        glUniform4f( u_color, 0.0, greenValue, 0.0, 1.0 )

        glBindVertexArray( VAO )
        glDrawArrays( GL_TRIANGLES, 0, 6 )        
        glBindVertexArray( 0 )

        shaderProgram.release()

        glfw.poll_events()
        glfw.swap_buffers( window )

    glfw.terminate()


if __name__ == '__main__':
    main() 

