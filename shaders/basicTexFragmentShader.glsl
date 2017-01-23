#version 330 core

in vec3 outColor;
in vec2 outTexCoords;

out vec4 color;
uniform vec4 u_color;


void main()
{
	color = vec4( u_color.x, u_color.y, u_color.z, 1.0f );
}
