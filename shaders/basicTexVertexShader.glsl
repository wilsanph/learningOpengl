#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec2 inTexCoords;

out vec3 outColor;
out vec2 outTexCoords;

uniform float u_offset;

void main()
{
	gl_Position = vec4( position.x + u_offset, -position.y, position.z, 1.0f );
	outColor = color;
	outTexCoords = inTexCoords;
}