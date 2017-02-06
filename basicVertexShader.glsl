#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec2 inTexCoords;

out vec3 outColor;
out vec2 outTexCoords;

uniform mat4 u_transform;

void main()
{
	gl_Position = u_transform * vec4( position.x, position.y, 1.0f, 1.0f );
	outColor = color;
	outTexCoords = inTexCoords;
}