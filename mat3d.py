
import pyrr
import numpy as np
import math

def rotx( t ) :
	t = math.radians( t )
	return pyrr.Matrix44( [  1.0  ,   	  0.0  		 ,  	0.0  	   , 0.0,
                             0.0  ,   math.cos( t )  ,  math.sin( t )  , 0.0,
                             0.0  ,  -math.sin( t )	 ,  math.cos( t )  , 0.0,
                             0.0  ,   	  0.0  		 ,  	0.0  	   , 1.0 ], dtype = np.float32 )

def roty( t ) :
	t = math.radians( t )
	return pyrr.Matrix44( [  math.cos( t )  ,  	0.0  , -math.sin( t )   , 0.0,
	                             0.0  		,   1.0  ,      0.0			, 0.0,
	                         math.sin( t )  ,  	0.0	 ,  math.cos( t )   , 0.0,
	                             0.0  		,  	0.0  ,  	0.0  	   , 1.0 ], dtype = np.float32 )

def makePerspectiveMatrix( fov, aspectRatio, near, far ) :

	m11 = ( 1.0 / aspectRatio ) * ( 1. / math.tan( math.radians( fov / 2. ) ) )
	m22 = 1.0 / math.tan( math.radians( fov / 2. ) )
	m33 = -( far + near ) / ( far - near )
	m34 = -2 * far * near / ( far - near )
	m43 = -1

	return pyrr.Matrix44( [  m11  ,   0.0  ,  0.0  , 0.0,
                             0.0  ,   m22  ,  0.0  , 0.0,
                             0.0  ,   0.0  ,  m33  , m43,
                             0.0  ,   0.0  ,  m34  , 0.0 ], dtype = np.float32 )
