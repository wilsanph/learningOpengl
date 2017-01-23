#version 330 core
in vec4 position;
uniform float u_offset;

void main()
{
	gl_Position = vec4( position.x + u_offset, -position.y, position.z, 1.0f );
}