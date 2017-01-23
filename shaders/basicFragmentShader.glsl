#version 330 core

out vec4 color;
uniform vec4 u_color;


void main()
{
	color = vec4( u_color.x, u_color.y, u_color.z, 1.0f );
}
