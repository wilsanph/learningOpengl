
from OpenGL.GL import *
import OpenGL.GL.shaders as glShaders

class Program():

	def __init__( self, vtShaderSrcPath, frgShaderSrcPath ):

		vtShaderId = self.compileShader( self.loadShader( vtShaderSrcPath ),
										 GL_VERTEX_SHADER )
		frgShaderId = self.compileShader( self.loadShader( frgShaderSrcPath ),
									  	  GL_FRAGMENT_SHADER )

		self.id = glShaders.compileProgram( vtShaderId, frgShaderId )

		glShaders.glDeleteShader( vtShaderId )
		glShaders.glDeleteShader( frgShaderId )

		print 'created shader program with program id: ' , self.id

	def loadShader( self, shaderSrcFile ):
		shaderFile = open( shaderSrcFile, 'r' )
		shaderSrcContent = shaderFile.read()
		return shaderSrcContent.encode()

	def compileShader( self, shaderSrc, shaderType ):
		return glShaders.compileShader( shaderSrc, shaderType )

	def use( self ):
		glUseProgram( self.id )

	def release( self ):
		glUseProgram( 0 )