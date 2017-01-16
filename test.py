

import glfw
from ctypes import c_void_p
from OpenGL.GL import *
import OpenGL.GL.shaders as glShaders
import numpy as np

null = c_void_p(0)

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
    
    vertices = np.array( [  0.5,  0.5, 0.0,
                            0.5, -0.5, 0.0,
                           -0.5, -0.5, 0.0,
                           -0.5,  0.5, 0.0 ], dtype = np.float32 )

    indices = np.array( [ 0, 1, 3,
                          1, 2, 3], dtype = np.uint32 )
    
    vertex_shader = """
    #version 330 core
    in vec4 position;

    void main()
    {
        gl_Position = position;
    }

    """
    
    fragment_shader = """
    #version 330 core

    out vec4 color;

    void main()
    {
        color = vec4( 1.0f, 0.0f, 0.0f, 1.0f );
    }

    """
    
    shaderProgram = glShaders.compileProgram( glShaders.compileShader( vertex_shader, GL_VERTEX_SHADER ),
                                              glShaders.compileShader( fragment_shader, GL_FRAGMENT_SHADER ) )

    # create a Vertex Buffer Object to store the vertices
    VBO = glGenBuffers( 1 )
    # create a Vertex Array Object to store the configuration
    VAO = glGenVertexArrays( 1 )
    # create a Element Buffer Object
    EBO = glGenBuffers( 1 )
    # set ths va0 as the current vao
    glBindVertexArray( VAO )
    
    # bind the vbo, which sets it as the current bound vbo
    glBindBuffer( GL_ARRAY_BUFFER, VBO )
    glBufferData( GL_ARRAY_BUFFER, 4 * len( vertices ), vertices, GL_STATIC_DRAW )
    
    # bind the ebo
    glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, EBO )
    glBufferData( GL_ELEMENT_ARRAY_BUFFER, 4 * len( indices ), indices, GL_STATIC_DRAW )

    # get the position attribute so that we link the vertices to this vertex attribute
    position = glGetAttribLocation( shaderProgram, 'position' )
    # related to the currently bound vbo, link the vertex data
    glVertexAttribPointer( position, 3, GL_FLOAT, GL_FALSE, 0, None ) 
    glEnableVertexAttribArray( position )

    glBindVertexArray( 0 )



    while not glfw.window_should_close( window ):
         
        glClearColor( 0.2, 0.3, 0.2, 1.0 )
        glClear( GL_COLOR_BUFFER_BIT )

        glUseProgram( shaderProgram )
        glBindVertexArray( VAO )
        #glDrawArrays( GL_TRIANGLES, 0, 6 )
        glDrawElements( GL_TRIANGLES, 6, GL_UNSIGNED_INT, None )
        glBindVertexArray( 0 )

        glfw.poll_events()
        glfw.swap_buffers( window )

    glfw.terminate()


if __name__ == '__main__':
    main() 

