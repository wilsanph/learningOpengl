#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 inTexCoords;

out vec2 outTexCoords;

uniform mat4 u_matModel;
uniform mat4 u_matView;
uniform mat4 u_matProjection;

void main()
{
	gl_Position = u_matProjection * u_matView * u_matModel * vec4( position, 1.0f );
	outTexCoords = inTexCoords;
}